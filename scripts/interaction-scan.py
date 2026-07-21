# -*- coding: utf-8 -*-
"""Interaction + multi-page scan for the Website Audit Suite (CRO / UX).

Goes beyond the homepage and beyond static markup — drives a browser across the key pages to check that
the conversion actually *works*:
 - **CTA reachability** — the primary call to action really points somewhere (a real page / on-page
   target), not a dead "#" or empty link.
 - **Form validation** — the main form's fields, required count, input types, and whether the browser
   would BLOCK an empty submit (client-side validation), via checkValidity() — **never submitting**.

Engine: **Playwright** (bundled Chromium — no browser to install; Windows/macOS/Linux).
Setup:  pip install playwright  &&  playwright install chromium
Usage:  python scripts/interaction-scan.py <homepage-URL> [--pages url1,url2,...] [--out DIR]

Ethics: it may follow a navigation CTA (that's just browsing) but it **never submits a form** —
submitting sends real data to the business. Never auto-submit a live production form.
"""
import json, os, sys, re
from urllib.parse import urljoin, urlparse
try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print(json.dumps({"error": "Playwright not installed — run: pip install playwright && playwright install chromium"})); sys.exit(3)

AUDIT_JS = r"""() => {
 const vis = el => { const s=getComputedStyle(el); if(s.display==='none'||s.visibility==='hidden')return false;
   const r=el.getBoundingClientRect(); return r.width>0&&r.height>0; };
 const ACT=/\b(get in touch|contact|book|buy|add to cart|sign up|get started|request|quote|subscribe|demo|start|call)\b/i;
 let best=null, bestScore=-1;
 for(const el of Array.from(document.querySelectorAll('a[href],button,[role=button]'))){
   if(!vis(el)) continue; const t=(el.textContent||'').trim(); if(!t||!ACT.test(t)) continue;
   const r=el.getBoundingClientRect(); const cls=(el.className||'').toString();
   let sc=0; if(r.top<800)sc+=3; if(/\b(btn|button|cta)\b/.test(cls))sc+=2; if(el.tagName==='BUTTON')sc+=1; sc+=Math.max(0,3-r.top/300);
   if(sc>bestScore){bestScore=sc;best=el;} }
 let cta=null;
 if(best){ const href=best.getAttribute('href')||''; const dead=(best.tagName==='A')&&(!href||href==='#'||/^javascript:/i.test(href));
   cta={text:(best.textContent||'').trim().slice(0,40), tag:best.tagName.toLowerCase(), href:href,
        dest: best.tagName==='A'? (href? new URL(href,location.href).href.replace(location.origin,'') : '(none)') : '(button)',
        dead:dead}; }
 const forms=Array.from(document.querySelectorAll('form')).filter(vis);
 let form=null;
 if(forms.length){ const f=forms.sort((a,b)=>b.querySelectorAll('input,textarea,select').length-a.querySelectorAll('input,textarea,select').length)[0];
   const fields=Array.from(f.querySelectorAll('input,textarea,select')).filter(el=>!['hidden','submit','button'].includes(el.type));
   const req=fields.filter(el=>el.required);
   const types=[...new Set(fields.map(el=>el.type||el.tagName.toLowerCase()))];
   const submit=f.querySelector('[type=submit],button');
   let blocksEmpty=false; try{ blocksEmpty=!f.checkValidity(); }catch(e){}
   form={fields:fields.length, required:req.length, types:types.slice(0,8), novalidate:f.hasAttribute('novalidate'),
         submitLabel:(submit&&(submit.value||submit.textContent||'').trim().slice(0,30))||'(none)',
         blocksEmptySubmit:blocksEmpty}; }
 const links=[...new Set(Array.from(document.querySelectorAll('a[href]')).map(a=>{
   try{return new URL(a.getAttribute('href'),location.href).href;}catch(e){return null;} })
   .filter(h=>h&&/^https?:/i.test(h)))].slice(0,80);
 return {cta, formsOnPage:forms.length, form, links, title:(document.title||'').slice(0,60)};
}"""

def check_links(reqctx, links, base_host, limit=40):
    """HEAD/GET each unique link and record its status — never posts, just reads the status line."""
    checked = []
    for u in links[:limit]:
        st = None
        try:
            r = reqctx.head(u, timeout=12000, max_redirects=5)
            st = r.status
            if st in (403, 405, 501):   # some servers reject HEAD — retry with GET
                r = reqctx.get(u, timeout=12000, max_redirects=5)
                st = r.status
        except Exception:
            try:
                r = reqctx.get(u, timeout=12000, max_redirects=5)
                st = r.status
            except Exception:
                st = None
        try: host = urlparse(u).netloc
        except Exception: host = ""
        checked.append({"url": u, "status": st, "internal": (host == base_host)})
    broken = [c for c in checked if c["status"] is None or c["status"] >= 400]
    return checked, broken

def main():
    if len(sys.argv) < 2 or sys.argv[1].startswith("--"):
        print("usage: interaction-scan.py <homepage-URL> [--pages a,b,c] [--out DIR]"); return 2
    base = sys.argv[1].rstrip("/") + "/"
    outdir = "."; pages = None
    for i, a in enumerate(sys.argv):
        if a == "--out" and i+1 < len(sys.argv): outdir = sys.argv[i+1]
        if a == "--pages" and i+1 < len(sys.argv): pages = [u.strip() for u in sys.argv[i+1].split(",") if u.strip()]
    if not pages:
        pages = [base, urljoin(base, "/contact/")]
    os.makedirs(outdir, exist_ok=True)
    try: sys.stdout.reconfigure(encoding="utf-8")
    except Exception: pass
    results = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        ctx = browser.new_context(viewport={"width": 1280, "height": 900})
        page = ctx.new_page()
        for u in pages[:6]:
            try:
                try: page.goto(u, wait_until="load", timeout=40000)
                except Exception: page.goto(u, timeout=40000)
                page.wait_for_timeout(2500)
                r = page.evaluate(AUDIT_JS)
                results.append({"url": u, **(r or {})})
            except Exception as e:
                results.append({"url": u, "error": str(e)[:80]})
        # aggregate unique links across the visited pages and check their HTTP status
        all_links, seen = [], set()
        for r in results:
            for h in (r.get("links") or []):
                if h not in seen:
                    seen.add(h); all_links.append(h)
        base_host = urlparse(base).netloc
        link_checked, link_broken = check_links(ctx.request, all_links, base_host)
        browser.close()
    out = {"base": base, "pages": results,
           "links": {"checked": len(link_checked), "found": len(all_links), "broken": link_broken}}
    json.dump(out, open(os.path.join(outdir, "interaction.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    def short(u): return re.sub(r"^https?://[^/]+", "", u) or "/"
    md = [f"# Interaction + multi-page scan — {base}", "",
          "_Drives a headless browser across key pages. Checks CTA reachability + form validation — **never submits a form**._", ""]
    for r in results:
        md.append(f"## {short(r['url'])}")
        if r.get("error"): md.append(f"- error: {r['error']}"); md.append(""); continue
        c = r.get("cta")
        if c: md.append(f"- **Primary CTA:** \"{c['text']}\" ({c['tag']}) → {c['dest']}" + ("  ⚠️ **dead link**" if c.get("dead") else ""))
        else: md.append("- **Primary CTA:** none detected above the fold")
        f = r.get("form")
        if f: md.append(f"- **Main form:** {f['fields']} fields ({f['required']} required), types: {', '.join(f['types'])}; "
                        f"validation blocks empty submit: {'yes' if f['blocksEmptySubmit'] else 'NO'}"
                        + (" (novalidate)" if f['novalidate'] else "") + f"; submit: \"{f['submitLabel']}\"")
        else: md.append(f"- **Main form:** none rendered ({r.get('formsOnPage',0)} form tags)")
        md.append("")
    lk = out["links"]
    md.append("## Links (HTTP status — measured, never posts)")
    md.append(f"- Checked **{lk['checked']}** of {lk['found']} unique links found; **{len(lk['broken'])} broken** (4xx/5xx or unreachable)")
    for b in lk["broken"][:12]:
        md.append(f"  - {b['status'] if b['status'] is not None else 'unreachable'} — {short(b['url']) if b['internal'] else b['url'][:70]}")
    md.append("")
    open(os.path.join(outdir, "interaction.md"), "w", encoding="utf-8").write("\n".join(md))
    print("\n".join(md))

if __name__ == "__main__":
    sys.exit(main() or 0)
