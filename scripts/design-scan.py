# -*- coding: utf-8 -*-
"""Design scan for the Website Audit Suite (Design & Visual skill).

Renders pages and gives the design/UX read the inputs a static crawl can't:
 1. MEASURED design tokens (from computed styles): colour palette, font families, count of distinct
    font sizes, count of distinct BUTTON STYLES (a design-system coherence signal).
 2. Full-page SCREENSHOTS at desktop (1440px) and mobile (390px) for the model's visual read.
 3. With --pages: renders representative INTERIOR TEMPLATES (an article, a service/offering page, a case
    study), screenshots each, compares their tokens (design drift), and MEASURES readability per page:
    body text-alignment, approximate characters-per-line (the 45-75 target), and words-per-visual
    (a "wall of text" signal). This is what lets the audit judge template pages, not just the homepage.

Engine: Playwright (bundled Chromium; no browser to install; Windows/macOS/Linux).
Setup:  pip install playwright  &&  playwright install chromium
Usage:  python scripts/design-scan.py <homepage-URL> [--pages url1,url2,...] [--out DIR]
"""
import json, os, re, sys
from urllib.parse import urlparse
try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print(json.dumps({"error": "Playwright not installed. Run: pip install playwright && playwright install chromium"})); sys.exit(3)

TOKENS_JS = r"""() => {
  const els = Array.from(document.querySelectorAll('body *'));
  const vis = el => { const s=getComputedStyle(el); if(s.display==='none'||s.visibility==='hidden')return false;
    const r=el.getBoundingClientRect(); return r.width>0&&r.height>0; };
  const inc=(m,k)=>{m[k]=(m[k]||0)+1;};
  const colors={},bgs={},fams={},sizes={},weights={},btns={};
  for(const el of els){ if(!vis(el))continue; const s=getComputedStyle(el);
    const hasText=(el.childNodes && Array.from(el.childNodes).some(n=>n.nodeType===3&&n.textContent.trim()));
    if(hasText){ inc(colors,s.color); inc(sizes,Math.round(parseFloat(s.fontSize))+'px'); inc(weights,s.fontWeight);
      inc(fams,(s.fontFamily||'').split(',')[0].replace(/["']/g,'').trim()); }
    if(s.backgroundColor && s.backgroundColor!=='rgba(0, 0, 0, 0)' && s.backgroundColor!=='transparent') inc(bgs,s.backgroundColor);
    const tag=el.tagName.toLowerCase();
    if(tag==='button'||el.getAttribute('role')==='button'||/\b(btn|button|cta)\b/.test(el.className||'')){
      inc(btns,[s.backgroundColor,s.color,s.borderRadius,s.borderWidth+' '+s.borderStyle,s.padding].join(' | ')); }
  }
  const top=(m,n)=>Object.entries(m).sort((a,b)=>b[1]-a[1]).slice(0,n);
  return { distinctTextColors:Object.keys(colors).length, topTextColors:top(colors,10),
           distinctBackgrounds:Object.keys(bgs).length, topBackgrounds:top(bgs,10),
           fontFamilies:top(fams,6), distinctFontSizes:Object.keys(sizes).length, topFontSizes:top(sizes,12),
           fontWeights:Object.keys(weights).sort(), distinctButtonStyles:Object.keys(btns).length,
           buttonStyleKeys:Object.keys(btns) };
}"""

# Readability of the main content: alignment, line length, text-to-visual ratio.
READABILITY_JS = r"""() => {
  const main = document.querySelector('main, article, [role="main"], #content, #main, .content, .entry-content') || document.body;
  const paras = Array.from(main.querySelectorAll('p')).filter(p => (p.innerText||'').trim().length > 40);
  const aligns={}; paras.forEach(p=>{ let a=getComputedStyle(p).textAlign||'start'; if(a==='start')a='left'; aligns[a]=(aligns[a]||0)+1; });
  let cpl=null, fs=null;
  if(paras.length){ const p=paras.slice().sort((a,b)=>(b.innerText||'').length-(a.innerText||'').length)[0];
    const s=getComputedStyle(p); fs=Math.round(parseFloat(s.fontSize));
    const w=p.getBoundingClientRect().width; cpl=Math.round(w/(parseFloat(s.fontSize)*0.5)); }
  const words=((main.innerText||'').match(/\S+/g)||[]).length;
  const visuals=main.querySelectorAll('img, svg, video, picture, figure, canvas, iframe').length;
  const dom=Object.entries(aligns).sort((a,b)=>b[1]-a[1])[0];
  return { paragraphs:paras.length, dominantAlign:(dom?dom[0]:null), aligns:aligns,
           charsPerLine:cpl, bodyFontPx:fs, words:words, visuals:visuals,
           wordsPerVisual:(visuals?Math.round(words/visuals):words) };
}"""

def slug(u):
    p = urlparse(u).path.strip("/").split("/")
    s = re.sub(r"[^a-z0-9]+", "-", (p[-1] if p and p[-1] else (p[-2] if len(p) > 1 else "page")).lower()).strip("-")
    return s[:24] or "page"

def main():
    if len(sys.argv) < 2 or sys.argv[1].startswith("--"):
        print("usage: design-scan.py <homepage-URL> [--pages a,b,c] [--out DIR]"); return 2
    url = sys.argv[1]; outdir = "."; extra = []
    for i, a in enumerate(sys.argv):
        if a == "--out" and i+1 < len(sys.argv): outdir = sys.argv[i+1]
        if a == "--pages" and i+1 < len(sys.argv): extra = [u.strip() for u in sys.argv[i+1].split(",") if u.strip() and u.strip() != url]
    os.makedirs(outdir, exist_ok=True)
    try: sys.stdout.reconfigure(encoding="utf-8")
    except Exception: pass
    out = {"url": url, "tokens": None, "screenshots": {}}
    pagerows = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        def render(u, w, h, mobile, shot_name=None, read=False):
            ctx = browser.new_context(viewport={"width": w, "height": h}, device_scale_factor=2 if mobile else 1,
                                      is_mobile=mobile, has_touch=mobile)
            page = ctx.new_page()
            try: page.goto(u, wait_until="load", timeout=45000)
            except Exception:
                try: page.goto(u, timeout=45000)
                except Exception: pass
            page.wait_for_timeout(3000)
            tok = page.evaluate(TOKENS_JS)
            rd = page.evaluate(READABILITY_JS) if read else None
            if shot_name: page.screenshot(path=os.path.join(outdir, shot_name), full_page=True)
            ctx.close()
            return tok, rd
        out["tokens"], home_read = render(url, 1440, 900, False, "design-desktop.png", read=True)
        out["screenshots"]["desktop"] = "design-desktop.png"
        render(url, 390, 844, True, "design-mobile.png")
        out["screenshots"]["mobile"] = "design-mobile.png"
        pagerows.append({"url": url, "type": "homepage", "tokens": out["tokens"], "readability": home_read, "screenshot": "design-desktop.png"})
        # interior templates: screenshot + tokens + readability (cap 3 to bound cost)
        for u in extra[:3]:
            shot = f"page-{slug(u)}.png"
            try:
                tok, rd = render(u, 1440, 900, False, shot, read=True)
                pagerows.append({"url": u, "tokens": tok, "readability": rd, "screenshot": shot})
            except Exception as e:
                pagerows.append({"url": u, "error": str(e)[:80]})
        browser.close()
    json.dump(out, open(os.path.join(outdir, "design-tokens.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    def primary_font(t): fs = t.get("fontFamilies", []); return fs[0][0] if fs else None
    if extra:
        fonts = set(); btnkeys = set(); bgs = set()
        for r in pagerows:
            t = r.get("tokens") or {}
            if primary_font(t): fonts.add(primary_font(t))
            btnkeys |= set(t.get("buttonStyleKeys", []))
            for v, _ in t.get("topBackgrounds", [])[:4]:
                if "0)" not in v: bgs.add(v)
        cons = {"pages": len(pagerows), "primaryFonts": sorted(fonts), "fontsConsistent": len(fonts) <= 1,
                "buttonStylesUnion": len(btnkeys), "paletteUnion": len(bgs),
                "perPage": [{"url": r["url"], "screenshot": r.get("screenshot"),
                             "font": primary_font(r.get("tokens") or {}),
                             "fontSizes": (r.get("tokens") or {}).get("distinctFontSizes"),
                             "buttonStyles": (r.get("tokens") or {}).get("distinctButtonStyles"),
                             "readability": r.get("readability")} for r in pagerows if r.get("tokens")]}
        json.dump({"consistency": cons, "pages": pagerows}, open(os.path.join(outdir, "design-pages.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    t = out["tokens"] or {}
    md = [f"# Design scan: {url}", "",
          f"- **Typeface(s):** {', '.join(f'{n} ({c})' for n,c in t.get('fontFamilies',[]))}",
          f"- **Distinct font sizes:** {t.get('distinctFontSizes','?')}  ·  weights: {', '.join(t.get('fontWeights',[]))}",
          f"- **Distinct colours:** {t.get('distinctTextColors','?')} text / {t.get('distinctBackgrounds','?')} background",
          f"- **Distinct button styles:** {t.get('distinctButtonStyles','?')} (fewer is more consistent)",
          f"- **Screenshots:** {', '.join(out['screenshots'].values())}", ""]
    if extra:
        md.append(f"## Interior templates: visual + readability ({len(pagerows)-1} sampled)")
        md.append("_Open each screenshot for the visual read (layout, text density, structure). The numbers below flag readability at a glance: line length target 45-75 chars; body text should be left/justified, not centred; a very high words-per-visual reads as a wall of text._")
        md.append("")
        md.append("| Page | Screenshot | Body align | Chars/line | Words/visual | Typeface | Font sizes | Button styles |")
        md.append("|------|-----------|-----------|:----------:|:------------:|----------|:----------:|:-------------:|")
        for r in pagerows:
            path = urlparse(r["url"]).path or "/"
            if r.get("error"): md.append(f"| {path} | error | | | | | | |"); continue
            rd = r.get("readability") or {}; tt = r.get("tokens") or {}
            md.append(f"| {path} | `{r.get('screenshot','—')}` | {rd.get('dominantAlign','?')} | {rd.get('charsPerLine','?')} | {rd.get('wordsPerVisual','?')} | "
                      f"{primary_font(tt)} | {tt.get('distinctFontSizes','?')} | {tt.get('distinctButtonStyles','?')} |")
        md.append("")
        md.append(f"- Primary typeface consistent across pages: {'yes' if len(fonts)<=1 else 'NO: '+', '.join(sorted(fonts))}")
        md.append(f"- Button styles across all pages (union): {len(btnkeys)}  ·  palette colours (union): {len(bgs)}")
    open(os.path.join(outdir, "design-scan.md"), "w", encoding="utf-8").write("\n".join(md))
    print("\n".join(md))

if __name__ == "__main__":
    sys.exit(main() or 0)
