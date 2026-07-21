# -*- coding: utf-8 -*-
"""Measured performance + accessibility + security scan for the Website Audit Suite (UX & Technical skill).

Renders the page (mobile-emulated, as Google measures) and captures — all locally, no API keys:
 1. PERFORMANCE — lab Core Web Vitals (LCP, CLS, FCP), TTFB, load time, total transferred weight,
    request count, third-party count, heaviest resources, and a lab INP proxy (Total Blocking Time).
 2. ACCESSIBILITY — real WCAG issues via axe-core (Deque, MIT), plus a keyboard focus-order pass.
 3. SECURITY — HTTPS, TLS version, HSTS, key response headers, the redirect chain, and mixed content.

Engine: **Playwright** (bundled Chromium — no browser to install; Windows/macOS/Linux).
Setup:  pip install playwright  &&  playwright install chromium
Usage:  python scripts/perf-a11y-scan.py <URL> [--out DIR]

Honesty: LAB measurement (one emulated run). Lab CWV + a Total-Blocking-Time INP proxy are measured here;
real-world *field* percentiles (which need many real users) are a different thing and are not claimed.
axe-core is loaded from a CDN at run time; if offline, the axe part is skipped and marked so.
"""
import json, os, sys
try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print(json.dumps({"error": "Playwright not installed — run: pip install playwright && playwright install chromium"})); sys.exit(3)

AXE_URLS = ["https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.10.2/axe.min.js",
            "https://cdn.jsdelivr.net/npm/axe-core@4.10.2/axe.min.js"]
CWV = {"lcp": (2500, 4000), "cls": (0.1, 0.25), "fcp": (1800, 3000), "ttfb": (800, 1800), "tbt": (200, 600)}
# Response headers we check for (name -> friendly label)
SEC_HEADERS = {"strict-transport-security": "HSTS", "content-security-policy": "CSP",
               "x-content-type-options": "X-Content-Type-Options", "x-frame-options": "X-Frame-Options",
               "referrer-policy": "Referrer-Policy", "permissions-policy": "Permissions-Policy"}

VITALS_INIT = r"""
window.__v={lcp:0,cls:0,fcp:0,tbt:0};
try{
 new PerformanceObserver(l=>{for(const e of l.getEntries())window.__v.lcp=Math.round(e.startTime);}).observe({type:'largest-contentful-paint',buffered:true});
 let c=0;new PerformanceObserver(l=>{for(const e of l.getEntries())if(!e.hadRecentInput)c+=e.value;window.__v.cls=+c.toFixed(3);}).observe({type:'layout-shift',buffered:true});
 new PerformanceObserver(l=>{for(const e of l.getEntries())if(e.name==='first-contentful-paint')window.__v.fcp=Math.round(e.startTime);}).observe({type:'paint',buffered:true});
 new PerformanceObserver(l=>{for(const e of l.getEntries())if(e.duration>50)window.__v.tbt+=Math.round(e.duration-50);}).observe({type:'longtask',buffered:true});
}catch(e){}
"""
COLLECT_JS = r"""() => {
 const nav=performance.getEntriesByType('navigation')[0]||{}, res=performance.getEntriesByType('resource'), host=location.host;
 let bytes=0,img=0,js=0,css=0,tp=0,mixed=0; const hosts={}, big=[], mixedSamples=[];
 for(const r of res){ const sz=r.transferSize||r.encodedBodySize||0; bytes+=sz;
   if(r.initiatorType==='img')img+=sz; if(r.initiatorType==='script')js+=sz; if(r.initiatorType==='link'||r.initiatorType==='css')css+=sz;
   try{const h=new URL(r.name).host; if(h&&h!==host){tp++;hosts[h]=1;}}catch(e){}
   if(location.protocol==='https:' && r.name.indexOf('http://')===0){ mixed++; if(mixedSamples.length<3) mixedSamples.push(r.name.slice(0,70)); }
   if(sz>=70000) big.push({name:decodeURIComponent(r.name.split('/').pop().split('?')[0]).slice(0,42),kb:Math.round(sz/1024),type:r.initiatorType}); }
 big.sort((a,b)=>b.kb-a.kb);
 let posTab=0; document.querySelectorAll('[tabindex]').forEach(e=>{ if((+e.getAttribute('tabindex'))>0) posTab++; });
 return {vitals:window.__v||{}, ttfb:Math.round(nav.responseStart||0), dcl:Math.round(nav.domContentLoadedEventEnd||0),
  load:Math.round(nav.loadEventEnd||0), requests:res.length, totalKB:Math.round(bytes/1024), imgKB:Math.round(img/1024),
  jsKB:Math.round(js/1024), cssKB:Math.round(css/1024), thirdPartyReqs:tp, thirdPartyHosts:Object.keys(hosts).length,
  biggest:big.slice(0,8), mixedContent:mixed, mixedSamples:mixedSamples, positiveTabindex:posTab};
}"""
AXE_JS = r"""() => axe.run(document,{resultTypes:['violations']}).then(r => r.violations.map(v => ({
  id:v.id, impact:v.impact, help:v.help, tags:v.tags.filter(t=>/wcag/.test(t)), nodes:v.nodes.length })))"""
FOCUS_JS = r"""() => { const e=document.activeElement; if(!e||e===document.body||e===document.documentElement) return null;
  const s=getComputedStyle(e);
  const visible = (s.outlineStyle!=='none' && s.outlineWidth!=='0px') || s.boxShadow!=='none';
  return {tag:e.tagName.toLowerCase(), role:e.getAttribute('role')||'',
    text:((e.innerText||e.value||e.getAttribute('aria-label')||'')+'').trim().replace(/\s+/g,' ').slice(0,30),
    focusVisible:visible}; }"""

def rate(metric, val):
    g, n = CWV[metric]; return "good" if val <= g else ("needs-improvement" if val <= n else "poor")

def keyboard_scan(page, max_tabs=20):
    """Tab through the page and record focus order + whether each stop shows a visible focus indicator."""
    seq, no_focus = [], 0
    try:
        page.evaluate("() => { if(document.activeElement && document.activeElement.blur) document.activeElement.blur(); }")
        for _ in range(max_tabs):
            page.keyboard.press("Tab")
            info = page.evaluate(FOCUS_JS)
            if not info:
                continue
            seq.append(info)
            if not info["focusVisible"]:
                no_focus += 1
    except Exception:
        pass
    return {"tabStops": len(seq), "noFocusIndicator": no_focus,
            "firstStops": [f"{x['tag']}:{x['text']}".rstrip(':') for x in seq[:6]]}

def security_scan(resp, page):
    """Read HTTPS/TLS, security headers, the redirect chain and mixed content from the main response."""
    sec = {"https": page.url.startswith("https://"), "finalUrl": page.url}
    if resp is None:
        return sec
    try: sec["status"] = resp.status
    except Exception: pass
    # security headers present/missing
    try:
        headers = {k.lower(): v for k, v in (resp.headers or {}).items()}
        sec["headers"] = {label: (name in headers) for name, label in SEC_HEADERS.items()}
    except Exception:
        sec["headers"] = {}
    # TLS version / issuer
    try:
        det = resp.security_details()
        if det:
            sec["tls"] = det.get("protocol"); sec["tlsIssuer"] = det.get("issuer")
    except Exception:
        pass
    # redirect chain (walk back from the final request)
    try:
        chain, req = [], resp.request
        seen = 0
        while req is not None and req.redirected_from is not None and seen < 10:
            req = req.redirected_from; seen += 1
            r = req.response()
            chain.append({"url": req.url[:80], "status": (r.status if r else None)})
        sec["redirects"] = list(reversed(chain))
    except Exception:
        sec["redirects"] = []
    return sec

def main():
    url = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else "https://example.com/"
    outdir = "."
    for i, a in enumerate(sys.argv):
        if a == "--out" and i+1 < len(sys.argv): outdir = sys.argv[i+1]
    os.makedirs(outdir, exist_ok=True)
    try: sys.stdout.reconfigure(encoding="utf-8")
    except Exception: pass
    out = {"url": url, "perf": None, "a11y": None, "security": None}
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        ctx = browser.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True)
        page = ctx.new_page()
        page.add_init_script(VITALS_INIT)
        resp = None
        try:
            resp = page.goto(url, wait_until="load", timeout=45000)
        except Exception:
            try: resp = page.goto(url, timeout=45000)
            except Exception: pass
        page.wait_for_timeout(4000)
        perf = page.evaluate(COLLECT_JS)
        v = perf.get("vitals", {})
        perf["ratings"] = {"lcp": rate("lcp", v.get("lcp",0) or 99999), "cls": rate("cls", v.get("cls",0)),
                            "fcp": rate("fcp", v.get("fcp",0) or 99999), "ttfb": rate("ttfb", perf.get("ttfb",0) or 99999),
                            "tbt": rate("tbt", v.get("tbt",0))}
        out["perf"] = perf
        # security — read from the main response before it's gone
        out["security"] = security_scan(resp, page)
        # accessibility via axe-core
        injected = False
        for u in AXE_URLS:
            try: page.add_script_tag(url=u); injected = True; break
            except Exception: continue
        if injected:
            try:
                av = page.evaluate(AXE_JS)
                by = {}
                for x in av: by[x["impact"] or "minor"] = by.get(x["impact"] or "minor", 0) + 1
                out["a11y"] = {"engine": "axe-core 4.10", "violations": len(av), "byImpact": by,
                               "top": sorted(av, key=lambda x: x["nodes"], reverse=True)[:10]}
            except Exception as e:
                out["a11y"] = {"error": "axe run failed: " + str(e)[:80]}
        else:
            out["a11y"] = {"error": "axe-core could not be fetched — accessibility not run"}
        # keyboard focus-order pass (local, no CDN)
        out["keyboard"] = keyboard_scan(page)
        browser.close()
    json.dump(out, open(os.path.join(outdir, "perf-a11y.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    pf = out["perf"] or {}; v = pf.get("vitals", {}); r = pf.get("ratings", {}); a = out["a11y"] or {}
    sec = out["security"] or {}; kb = out.get("keyboard", {})
    md = [f"# Performance, accessibility & security (measured, lab) — {url}", "",
          "## Core Web Vitals (lab — mobile-emulated, one run)",
          f"- **LCP** {v.get('lcp','?')} ms — {r.get('lcp','?')}  (2026 target ≤ 2500)",
          f"- **CLS** {v.get('cls','?')} — {r.get('cls','?')}  (≤ 0.1)",
          f"- **FCP** {v.get('fcp','?')} ms — {r.get('fcp','?')}  (≤ 1800)",
          f"- **TTFB** {pf.get('ttfb','?')} ms — {r.get('ttfb','?')}  (≤ 800)",
          f"- **INP proxy — Total Blocking Time** {v.get('tbt','?')} ms — {r.get('tbt','?')}  (lab stand-in for INP; ≤ 200 good, > 600 poor)",
          f"- Load {pf.get('load','?')} ms · {pf.get('requests','?')} requests · **{pf.get('totalKB','?')} KB** transferred "
          f"(img {pf.get('imgKB','?')} KB, JS {pf.get('jsKB','?')} KB) · {pf.get('thirdPartyHosts','?')} third-party hosts", ""]
    if pf.get("biggest"):
        md.append("- Heaviest resources: " + ", ".join(f"{b['name']} ({b['kb']} KB)" for b in pf["biggest"][:5])); md.append("")
    md.append("## Accessibility (axe-core, WCAG)")
    if a.get("violations") is not None:
        md.append(f"- **{a['violations']} violation types** — " + ", ".join(f"{k}: {n}" for k, n in a.get("byImpact", {}).items()))
        for x in a.get("top", []): md.append(f"  - `{x['id']}` ({x['impact']}, {x['nodes']} el) — {x['help']}")
    else:
        md.append(f"- {a.get('error','not run')}")
    md.append(f"- Keyboard: **{kb.get('tabStops',0)} tab stops** reached; **{kb.get('noFocusIndicator',0)}** with no visible focus indicator"
              + (f"; {pf.get('positiveTabindex',0)} positive `tabindex` (anti-pattern)" if pf.get("positiveTabindex") else ""))
    if kb.get("firstStops"):
        md.append("  - First focus order: " + " → ".join(kb["firstStops"]))
    md += ["", "## Security (measured from the response)"]
    md.append(f"- **HTTPS:** {'yes' if sec.get('https') else 'NO'}"
              + (f" · TLS {sec['tls']}" if sec.get("tls") else "")
              + (f" · status {sec['status']}" if sec.get("status") else ""))
    if sec.get("headers"):
        present = [lbl for lbl, ok in sec["headers"].items() if ok]
        missing = [lbl for lbl, ok in sec["headers"].items() if not ok]
        md.append(f"- Security headers present: {', '.join(present) if present else 'none'}")
        md.append(f"- Security headers **missing**: {', '.join(missing) if missing else 'none'}")
    if sec.get("redirects"):
        md.append(f"- Redirect chain ({len(sec['redirects'])} hop(s)): "
                  + " → ".join(f"{h['status']}" for h in sec["redirects"]) + " → 200")
    mc = pf.get("mixedContent", 0)
    md.append(f"- Mixed content (http on https): **{mc}**" + (f" — e.g. {pf['mixedSamples'][0]}" if mc and pf.get("mixedSamples") else ""))
    text = "\n".join(md) + "\n"
    open(os.path.join(outdir, "perf-a11y.md"), "w", encoding="utf-8").write(text)
    print(text)

if __name__ == "__main__":
    sys.exit(main() or 0)
