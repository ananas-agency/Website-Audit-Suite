# -*- coding: utf-8 -*-
"""Site-wide quick SEO sweep for the Website Audit Suite (SEO & Content skill).

Two-tier depth: the homepage gets the full 4-dimension audit; secondary pages
(services, products, case studies, articles, about) get a light *static* per-page SEO
check — no rendering — so coverage is broad but cheap. Discovers pages from the homepage
nav and the sitemap, classifies them by type, caps to N per type (default 5), fetches each
and extracts a full per-page SEO row, then prints a compact Markdown table + aggregate
flags. Returns a summary (not page bodies) so it stays token-light.

Usage:
    python scripts/seo-sweep.py https://example.com/ [--per-type 5] [--out DIR]

Pure standard library — no pip installs, no browser. Static HTML only (by design: quick).
"""
import sys, os, re, json, urllib.request, urllib.parse, html as _html
from collections import defaultdict

UA = {"User-Agent": "Mozilla/5.0 (WebsiteAuditSuite SEO-sweep)"}
THIN_WORDS = 300          # below this = thin-content flag
TITLE_MIN, TITLE_MAX = 30, 60
DESC_MIN, DESC_MAX = 70, 160

# URL-path -> page type (priority order; first match wins)
TYPE_PATTERNS = [
    ("services",     r"/(services?|solutions?|offer|implementation|trainings?)(/|$)"),
    ("products",     r"/(products?|shop|store|display-hub|terminal|kiosk|sniphi)(/|$)"),
    ("case-studies", r"/(case-stud(y|ies)|portfolio|work|projects?|realizacj)(/|$)"),
    ("articles",     r"/(articles?|blog|news|insights?|posts?|cat|category)(/|$)"),
    ("about",        r"/(about|our-approach|our-company|company|team|careers?|contact)(/|$)"),
]
SKIP_RE = re.compile(r"\.(?:jpg|jpeg|png|gif|svg|webp|pdf|zip|css|js|xml|ico|mp4|woff2?)(?:\?|$)", re.I)
SKIP_PATH = re.compile(r"/(wp-json|feed|wp-admin|wp-content|tag|author|page/\d+)(/|$)|/(pl|de|fr|es|it|ua|ru)/", re.I)


def fetch(url, timeout=20):
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=timeout) as r:
            body = r.read(1_500_000).decode("utf-8", "ignore")
            return r.status, str(r.url), body
    except urllib.error.HTTPError as e:
        return e.code, url, ""
    except Exception:
        return 0, url, ""


def classify(path):
    for label, pat in TYPE_PATTERNS:
        if re.search(pat, path, re.I):
            return label
    return None


def discover(base):
    host = urllib.parse.urlparse(base).netloc
    urls = set()
    # 1) homepage internal links
    _, _, home = fetch(base)
    for m in re.finditer(r'href=["\'](https?://[^"\'#?]+|/[^"\'#?]*)["\']', home, re.I):
        u = urllib.parse.urljoin(base, m.group(1))
        if urllib.parse.urlparse(u).netloc == host:
            urls.add(u.split("#")[0].rstrip("/") + "/")
    # 2) sitemaps (WordPress/Yoast common paths)
    for sm in ("sitemap_index.xml", "sitemap.xml", "wp-sitemap.xml"):
        st, _, xml = fetch(urllib.parse.urljoin(base, "/" + sm))
        if st != 200 or "<" not in xml:
            continue
        locs = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", xml)
        child_sitemaps = [l for l in locs if l.endswith(".xml")]
        for cs in child_sitemaps[:8]:
            _, _, cxml = fetch(cs)
            for l in re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", cxml):
                if not l.endswith(".xml"):
                    urls.add(l.split("#")[0].rstrip("/") + "/")
        for l in locs:
            if not l.endswith(".xml"):
                urls.add(l.split("#")[0].rstrip("/") + "/")
        break
    # filter + classify + cap
    clean = []
    for u in urls:
        p = urllib.parse.urlparse(u)
        if p.netloc != host or SKIP_RE.search(u) or SKIP_PATH.search(p.path):
            continue
        if p.path in ("", "/"):
            continue
        clean.append(u)
    return sorted(set(clean))


def text_of(body):
    b = re.sub(r"<(script|style|noscript)[^>]*>.*?</\1>", " ", body, flags=re.S | re.I)
    b = re.sub(r"<[^>]+>", " ", b)
    return _html.unescape(re.sub(r"\s+", " ", b)).strip()


def tag_text(body, tag):
    out = []
    for m in re.finditer(rf"<{tag}\b[^>]*>(.*?)</{tag}>", body, re.S | re.I):
        out.append(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", m.group(1))).strip())
    return [t for t in out if t]


# Minimal required-field rules for the common rich-result types (Google's essentials, simplified).
SCHEMA_REQUIRED = {
    "Organization": ["name"], "LocalBusiness": ["name", "address"], "Product": ["name"],
    "Article": ["headline"], "NewsArticle": ["headline"], "BlogPosting": ["headline"],
    "BreadcrumbList": ["itemListElement"], "FAQPage": ["mainEntity"], "Service": ["name"],
    "Event": ["name", "startDate"], "WebSite": ["name"], "Person": ["name"],
    "VideoObject": ["name", "thumbnailUrl", "uploadDate"],
}


def _iter_nodes(obj):
    """Yield each dict node in a JSON-LD structure, following @graph and arrays."""
    if isinstance(obj, list):
        for x in obj:
            yield from _iter_nodes(x)
    elif isinstance(obj, dict):
        if isinstance(obj.get("@graph"), list):
            for x in obj["@graph"]:
                yield from _iter_nodes(x)
        else:
            yield obj


def validate_schema(body):
    """Parse every JSON-LD block locally and check required fields per @type — no external API."""
    blocks = re.findall(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', body, re.S | re.I)
    invalid, types, issues = 0, [], []
    for b in blocks:
        raw = re.sub(r"^\s*<!\[CDATA\[|\]\]>\s*$", "", b.strip()).strip()
        try:
            data = json.loads(raw)
        except Exception:
            invalid += 1
            continue
        for node in _iter_nodes(data):
            t = node.get("@type")
            if isinstance(t, list):
                t = t[0] if t else None
            if not t:
                continue
            types.append(t)
            req = SCHEMA_REQUIRED.get(t)
            if req:
                miss = [k for k in req if not node.get(k)]
                if miss:
                    issues.append(f"{t} missing {'/'.join(miss)}")
    return {"blocks": len(blocks), "invalid_json": invalid, "types": sorted(set(types))[:8], "issues": issues[:6]}


def analyze(url):
    status, final, body = fetch(url)
    if status != 200 or not body:
        return {"url": url, "status": status, "ok": False}
    def attr(pat):
        m = re.search(pat, body, re.I)
        return _html.unescape(m.group(1)).strip() if m else None
    title = None
    tm = re.search(r"<title[^>]*>(.*?)</title>", body, re.S | re.I)
    if tm:
        title = _html.unescape(re.sub(r"\s+", " ", tm.group(1))).strip()
    desc = attr(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']*)["\']') \
        or attr(r'<meta[^>]+content=["\']([^"\']*)["\'][^>]+name=["\']description["\']')
    canonical = attr(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)["\']')
    robots = (attr(r'<meta[^>]+name=["\']robots["\'][^>]+content=["\']([^"\']*)["\']') or "")
    noindex = "noindex" in robots.lower()
    h1 = tag_text(body, "h1"); h2 = tag_text(body, "h2"); h3 = tag_text(body, "h3")
    words = len(text_of(body).split())
    imgs = re.findall(r"<img\b[^>]*>", body, re.I)
    with_alt = [i for i in imgs if re.search(r'\balt=', i, re.I)]
    empty_alt = [i for i in imgs if re.search(r'\balt=["\']["\']', i)]
    og_title = attr(r'<meta[^>]+property=["\']og:title["\'][^>]+content=["\']([^"\']*)["\']')
    og_image = attr(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']')
    sch = validate_schema(body)
    host = urllib.parse.urlparse(url).netloc
    ilinks = len(set(re.findall(rf'href=["\'](?:https?://{re.escape(host)})?/[^"\'#?]*', body)))
    # keyword-in-title/H1 alignment: do the H1's meaningful words appear in the title?
    def words_of(s): return set(re.findall(r"[a-z0-9]{4,}", (s or "").lower()))
    align = None
    if title and h1:
        shared = words_of(h1[0]) & words_of(title)
        align = "ok" if shared else "mismatch"
    return {"url": final, "status": status, "ok": True,
            "type": classify(urllib.parse.urlparse(final).path),
            "title": title, "title_len": len(title) if title else 0,
            "desc": desc, "desc_len": len(desc) if desc else 0,
            "canonical": bool(canonical), "noindex": noindex,
            "h1_count": len(h1), "h1": h1[0] if h1 else None,
            "h2": len(h2), "h3": len(h3), "words": words,
            "imgs": len(imgs), "imgs_alt": len(with_alt), "empty_alt": len(empty_alt),
            "og_title": og_title, "og_image": bool(og_image),
            "schema": sch["blocks"], "schema_types": sch["types"],
            "schema_invalid": sch["invalid_json"], "schema_issues": sch["issues"],
            "ilinks": ilinks, "kw_align": align}


def flags(row):
    f = []
    if not row.get("ok"):
        return [f"status {row.get('status')}"]
    if not row["title"]: f.append("no title")
    elif not (TITLE_MIN <= row["title_len"] <= TITLE_MAX): f.append(f"title {row['title_len']}c")
    if not row["desc"]: f.append("no meta desc")
    elif not (DESC_MIN <= row["desc_len"] <= DESC_MAX): f.append(f"desc {row['desc_len']}c")
    if row["h1_count"] == 0: f.append("no H1")
    elif row["h1_count"] > 1: f.append(f"{row['h1_count']} H1s")
    if not row["canonical"]: f.append("no canonical")
    if row["noindex"]: f.append("NOINDEX")
    if row["words"] < THIN_WORDS: f.append(f"thin {row['words']}w")
    if row["imgs"] and row["imgs_alt"] < row["imgs"]: f.append(f"{row['imgs']-row['imgs_alt']} img no-alt")
    if row.get("og_title") in (None, "Home", "Homepage"): f.append("og:title weak")
    if not row["schema"]: f.append("no schema")
    elif row.get("schema_invalid"): f.append(f"schema JSON invalid×{row['schema_invalid']}")
    elif row.get("schema_issues"): f.append(f"schema: {row['schema_issues'][0]}")
    if row["kw_align"] == "mismatch": f.append("H1/title mismatch")
    return f or ["clean"]


def main():
    if len(sys.argv) < 2 or sys.argv[1].startswith("--"):
        print("usage: seo-sweep.py <homepage-url> [--per-type N] [--out DIR]"); return 2
    base = sys.argv[1].rstrip("/") + "/"
    per_type, outdir = 5, "."
    for i, a in enumerate(sys.argv):
        if a == "--per-type" and i+1 < len(sys.argv): per_type = int(sys.argv[i+1])
        if a == "--out" and i+1 < len(sys.argv): outdir = sys.argv[i+1]
    os.makedirs(outdir, exist_ok=True)
    try: sys.stdout.reconfigure(encoding="utf-8")
    except Exception: pass

    cand = discover(base)
    buckets = defaultdict(list)
    for u in cand:
        t = classify(urllib.parse.urlparse(u).path)
        if t and len(buckets[t]) < per_type:
            buckets[t].append(u)
    rows = []
    for t in ("services", "products", "case-studies", "articles", "about"):
        for u in buckets.get(t, []):
            r = analyze(u); r["type"] = r.get("type") or t; r["flags"] = flags(r); rows.append(r)

    # validate the homepage's structured data too (the per-type sweep skips the homepage)
    _, _, homebody = fetch(base)
    home_schema = validate_schema(homebody)

    out = {"base": base, "discovered": len(cand), "swept": len(rows),
           "per_type": per_type, "by_type": {t: len(buckets.get(t, [])) for t in buckets},
           "home_schema": home_schema, "rows": rows}
    json.dump(out, open(os.path.join(outdir, "seo-sweep.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    def short(u): return re.sub(r"^https?://[^/]+", "", u) or "/"
    md = [f"# Site-wide quick SEO sweep — {base}",
          f"_Discovered {len(cand)} internal URLs; swept {len(rows)} (≤{per_type}/type). Static per-page SEO; homepage is audited in full separately._", ""]
    md.append("| Page | Type | Title (len) | Desc (len) | H1 | Words | Alt | Schema | Flags |")
    md.append("|------|------|-------------|-----------|----|-------|-----|--------|-------|")
    for r in rows:
        if not r.get("ok"):
            md.append(f"| {short(r['url'])} | {r.get('type','?')} | — | — | — | — | — | — | status {r['status']} |"); continue
        md.append(f"| {short(r['url'])} | {r['type']} | {r['title_len']} | {r['desc_len']} | "
                  f"{r['h1_count']} | {r['words']} | {r['imgs_alt']}/{r['imgs']} | {r['schema']} | {', '.join(r['flags'])} |")
    # aggregate site-wide flags
    titles = [r['title'] for r in rows if r.get('title')]
    dup = sorted({t for t in titles if titles.count(t) > 1})
    agg = []
    miss_desc = [short(r['url']) for r in rows if r.get('ok') and not r['desc']]
    thin = [short(r['url']) for r in rows if r.get('ok') and r['words'] < THIN_WORDS]
    nocanon = [short(r['url']) for r in rows if r.get('ok') and not r['canonical']]
    if dup: agg.append(f"- **Duplicate titles** across pages: {', '.join(dup)}")
    if miss_desc: agg.append(f"- **Missing meta description:** {len(miss_desc)} page(s) — {', '.join(miss_desc[:6])}")
    if thin: agg.append(f"- **Thin content (<{THIN_WORDS}w):** {', '.join(thin[:6])}")
    if nocanon: agg.append(f"- **No canonical tag:** {len(nocanon)} page(s)")
    if agg:
        md += ["", "## Site-wide patterns", *agg]
    # structured-data validation (homepage + any per-page issues found)
    hs = out["home_schema"]
    sd = [f"- **Homepage:** {hs['blocks']} JSON-LD block(s)"
          + (f", types: {', '.join(hs['types'])}" if hs["types"] else "")
          + (f" — **{hs['invalid_json']} invalid JSON**" if hs["invalid_json"] else "")
          + (f" — issues: {'; '.join(hs['issues'])}" if hs["issues"] else "")
          + (" — none found" if not hs["blocks"] else "")]
    page_sd = [f"  - {short(r['url'])}: " + (f"{r['schema_invalid']} invalid JSON" if r.get("schema_invalid")
               else '; '.join(r.get("schema_issues", [])))
               for r in rows if r.get("ok") and (r.get("schema_invalid") or r.get("schema_issues"))]
    if page_sd:
        sd.append("- **Per-page schema issues:**"); sd += page_sd
    md += ["", "## Structured data (validated locally)", *sd]
    text = "\n".join(md) + "\n"
    open(os.path.join(outdir, "seo-sweep.md"), "w", encoding="utf-8").write(text)
    print(text)


if __name__ == "__main__":
    sys.exit(main() or 0)
