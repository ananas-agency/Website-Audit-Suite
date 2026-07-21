# -*- coding: utf-8 -*-
"""Measured mobile-friendliness test for the Website Audit Suite (UX & Technical skill).

Renders a URL at real phone viewports (proper mobile emulation) and measures what a static-HTML read
cannot: does the page fit the screen, are elements or images wider than the viewport, are tap targets
big enough, is text legible. Saves a full-page screenshot per width and prints a JSON + Markdown summary.

Engine: **Playwright** (bundles its own Chromium — no browser to install, works on Windows/macOS/Linux).

Setup (one time):
    pip install playwright
    playwright install chromium

Usage:
    python scripts/mobile-audit.py https://example.com/ [--out DIR] [--widths 320,390,414]

If Playwright isn't installed, the UX skill falls back to marking these checks "not measured".
Thresholds: fits = scroll width <= viewport (+2px); tap target min 44x44 CSS px; legible text min 12px.
"""
import json, os, sys
try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print(json.dumps({"error": "Playwright not installed — run: pip install playwright && playwright install chromium"})); sys.exit(3)

TAP_MIN = 44
TEXT_MIN = 12

MEASURE_JS = r"""() => {
  const vw = window.innerWidth, vh = window.innerHeight;
  const de = document.documentElement;
  const scrollW = Math.max(de.scrollWidth, document.body ? document.body.scrollWidth : 0);
  const overflow = scrollW - vw;
  const vpMeta = (document.querySelector('meta[name="viewport"]')||{}).content || null;
  const vis = el => {
    const s = getComputedStyle(el);
    if (s.display==='none'||s.visibility==='hidden'||parseFloat(s.opacity)===0) return false;
    const r = el.getBoundingClientRect();
    return r.width>=6 && r.height>=6;
  };
  const clipped = el => {
    let n = el.parentElement;
    while (n) { const ox = getComputedStyle(n).overflowX;
      if (ox==='hidden'||ox==='clip'||ox==='auto'||ox==='scroll') return true;
      n = n.parentElement; }
    return false;
  };
  const txt = el => (el.textContent||'').trim().replace(/\s+/g,' ').slice(0,60);
  const all = Array.from(document.querySelectorAll('body *'));
  const wide = [], clippedWide = [];
  for (const el of all) {
    if (!vis(el)) continue;
    const r = el.getBoundingClientRect();
    if (r.right > vw + 2 && r.width > 40 && r.left < vw) {
      const rec = {tag: el.tagName.toLowerCase(), cls: (el.className||'').toString().slice(0,40),
                   w: Math.round(r.width), over: Math.round(r.right - vw), text: txt(el)};
      (clipped(el) ? clippedWide : wide).push(rec);
    }
  }
  wide.sort((a,b)=>b.over-a.over); clippedWide.sort((a,b)=>b.over-a.over);
  const imgs = [];
  for (const img of Array.from(document.images)) {
    if (!vis(img)) continue;
    const r = img.getBoundingClientRect();
    if (r.width > vw + 2) imgs.push({src:(img.currentSrc||img.src||'').split('/').pop().slice(0,50),
      w: Math.round(r.width), natW: img.naturalWidth});
  }
  const tapSel = 'a[href],button,input[type=submit],input[type=button],[role=button],select,summary';
  const smallTaps = []; const seenTap = new Set();
  for (const el of Array.from(document.querySelectorAll(tapSel))) {
    if (!vis(el)) continue;
    const t = txt(el);
    if (/^skip to/i.test(t)) continue;
    const r = el.getBoundingClientRect();
    if (r.width < 44 || r.height < 44) {
      const key = el.tagName + Math.round(r.width) + 'x' + Math.round(r.height) + t.slice(0,16);
      if (seenTap.has(key)) continue; seenTap.add(key);
      smallTaps.push({tag:el.tagName.toLowerCase(), w:Math.round(r.width), h:Math.round(r.height), text:t});
    }
  }
  const smallText = []; const seenT = new Set();
  for (const el of all) {
    if (el.children.length>0) continue;
    const t = txt(el); if (!t || t.length<2) continue;
    if (!vis(el)) continue;
    const fs = parseFloat(getComputedStyle(el).fontSize);
    if (fs && fs < 12) {
      const key = el.tagName+fs+t.slice(0,20);
      if (seenT.has(key)) continue; seenT.add(key);
      smallText.push({tag:el.tagName.toLowerCase(), px:+fs.toFixed(1), text:t});
    }
  }
  return {vw, vh, scrollW, overflow, fits: overflow<=2, vpMeta,
          overflowCount: wide.length, overflowing: wide.slice(0,12),
          clippedWideCount: clippedWide.length, clippedWide: clippedWide.slice(0,6),
          oversizedImgCount: imgs.length, oversizedImgs: imgs.slice(0,10),
          smallTapCount: smallTaps.length, smallTaps: smallTaps.slice(0,15),
          smallTextCount: smallText.length, smallText: smallText.slice(0,12)};
}"""

def summarize_md(out):
    lines = [f"# Mobile-friendliness (measured) — {out['url']}", ""]
    for w, m in out["widths"].items():
        if not m: continue
        fit = "✅ fits the screen" if m["fits"] else f"❌ sideways scroll (+{m['overflow']}px)"
        lines.append(f"## {w}px viewport — {fit}")
        lines.append(f"- Viewport meta: `{m['vpMeta']}`")
        lines.append(f"- Elements overflowing the screen edge (real): **{m['overflowCount']}**"
                     + (f" — worst: `{m['overflowing'][0]['tag']}.{m['overflowing'][0]['cls']}` +{m['overflowing'][0]['over']}px" if m['overflowing'] else ""))
        lines.append(f"- Content clipped by a carousel/overflow container (usually fine): {m['clippedWideCount']}")
        lines.append(f"- Images wider than the screen: **{m['oversizedImgCount']}**")
        lines.append(f"- Tap targets under {TAP_MIN}×{TAP_MIN}px: **{m['smallTapCount']}**"
                     + (f" — e.g. " + "; ".join(f"{t['tag']} {t['w']}×{t['h']} \"{t['text'][:18]}\"" for t in m['smallTaps'][:4]) if m['smallTaps'] else ""))
        lines.append(f"- Text smaller than {TEXT_MIN}px: **{m['smallTextCount']}**")
        lines.append(f"- Screenshot: `{m.get('screenshot','')}`")
        lines.append("")
    return "\n".join(lines)

def main():
    url = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else "https://example.com/"
    outdir = "."; widths = [320, 390, 414]
    for i, a in enumerate(sys.argv):
        if a == "--out" and i+1 < len(sys.argv): outdir = sys.argv[i+1]
        if a == "--widths" and i+1 < len(sys.argv): widths = [int(x) for x in sys.argv[i+1].split(",")]
    os.makedirs(outdir, exist_ok=True)
    try: sys.stdout.reconfigure(encoding="utf-8")
    except Exception: pass
    out = {"url": url, "browser": "playwright-chromium", "widths": {}}
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        for w in widths:
            ctx = browser.new_context(viewport={"width": w, "height": 844}, device_scale_factor=2,
                                      is_mobile=True, has_touch=True)
            page = ctx.new_page()
            try:
                page.goto(url, wait_until="load", timeout=45000)
            except Exception:
                try: page.goto(url, timeout=45000)
                except Exception: pass
            page.wait_for_timeout(3000)
            m = page.evaluate(MEASURE_JS)
            fn = f"mobile-{w}.png"; page.screenshot(path=os.path.join(outdir, fn), full_page=True)
            m["screenshot"] = fn
            out["widths"][w] = m
            ctx.close()
        browser.close()
    open(os.path.join(outdir, "mobile-metrics.json"), "w", encoding="utf-8").write(json.dumps(out, indent=2, ensure_ascii=False))
    open(os.path.join(outdir, "mobile-metrics.md"), "w", encoding="utf-8").write(summarize_md(out))
    print(summarize_md(out))

if __name__ == "__main__":
    sys.exit(main() or 0)
