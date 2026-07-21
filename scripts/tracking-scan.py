# -*- coding: utf-8 -*-
"""Measurement-readiness scan for the Website Audit Suite (Conversion / CRO skill).

"Can they even measure the outcomes we prescribe?" Renders the page on a FRESH load (no consent given),
watches the network + cookies + JS globals, and reports the analytics stack, marketing pixels, consent
platform, whether trackers fire before consent (GDPR risk), conversion-tracking signals, and cookies.

Engine: **Playwright** (bundled Chromium — no browser to install; Windows/macOS/Linux).
Setup:  pip install playwright  &&  playwright install chromium
Usage:  python scripts/tracking-scan.py <URL> [--out DIR]   (read-only — no clicks, no submits)
"""
import json, os, sys, re
from urllib.parse import urlparse
try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print(json.dumps({"error": "Playwright not installed — run: pip install playwright && playwright install chromium"})); sys.exit(3)

TRACKERS = [
    ("googletagmanager.com/gtm.js", "tag-manager", "Google Tag Manager"),
    ("googletagmanager.com/gtag",   "analytics",   "Google gtag (GA4)"),
    ("google-analytics.com",        "analytics",   "Google Analytics"),
    ("analytics.google.com",        "analytics",   "Google Analytics"),
    ("plausible.io",                "analytics",   "Plausible"),
    ("matomo",                      "analytics",   "Matomo"),
    ("clarity.ms",                  "session",     "Microsoft Clarity"),
    ("hotjar",                      "session",     "Hotjar"),
    ("mouseflow",                   "session",     "Mouseflow"),
    ("fullstory",                   "session",     "FullStory"),
    ("connect.facebook.net",        "marketing",   "Meta/Facebook pixel"),
    ("facebook.com/tr",             "marketing",   "Meta/Facebook pixel"),
    ("doubleclick.net",             "marketing",   "Google Ads / DoubleClick"),
    ("googleadservices.com",        "marketing",   "Google Ads"),
    ("google.com/ads",              "marketing",   "Google Ads"),
    ("licdn.com",                   "marketing",   "LinkedIn Insight"),
    ("linkedin.com",                "marketing",   "LinkedIn"),
    ("bat.bing.com",                "marketing",   "Microsoft/Bing Ads"),
    ("analytics.tiktok.com",        "marketing",   "TikTok pixel"),
    ("ads-twitter.com",             "marketing",   "X/Twitter Ads"),
    ("criteo",                      "marketing",   "Criteo"),
    ("cookiebot.com",               "consent",     "Cookiebot (CMP)"),
    ("cookielaw.org",               "consent",     "OneTrust (CMP)"),
    ("onetrust",                    "consent",     "OneTrust (CMP)"),
    ("usercentrics",               "consent",     "Usercentrics (CMP)"),
    ("iubenda",                     "consent",     "Iubenda (CMP)"),
    ("cookieyes",                   "consent",     "CookieYes (CMP)"),
    ("consensu.org",                "consent",     "IAB TCF CMP"),
]
GLOBALS_JS = r"""() => {
 const g=window, has=k=>typeof g[k]!=='undefined';
 const cmp=[];
 if(has('Cookiebot')) cmp.push('Cookiebot');
 if(has('OneTrust')||has('Optanon')||has('OptanonActiveGroups')) cmp.push('OneTrust');
 if(has('__tcfapi')) cmp.push('IAB TCF');
 if(has('UC_UI')||has('usercentrics')) cmp.push('Usercentrics');
 if(has('cmplz_categories')||has('complianz')) cmp.push('Complianz');
 if(has('CookieConsent')||has('cookieconsent')) cmp.push('CookieConsent');
 if(has('cookieyes')||has('getCkyConsent')) cmp.push('CookieYes');
 if(has('Iubenda')||has('_iub')) cmp.push('Iubenda');
 if(has('klaro')) cmp.push('Klaro');
 const dl=g.dataLayer||[];
 let consentMode=false, events=[];
 try{ for(const e of dl){ const a=Array.isArray(e)?e:Object.values(e);
   if(a&&a[0]==='consent') consentMode=true;
   if(e&&e.event && !/gtm\.(js|load|dom)/.test(e.event)) events.push(e.event); } }catch(_){}
 return { hasDataLayer:has('dataLayer'), dataLayerLen:(g.dataLayer||[]).length,
   gtag:has('gtag'), ga:has('ga')||has('__ga'), fbq:has('fbq'), consentMode,
   cmp:[...new Set(cmp)], dataLayerEvents:[...new Set(events)].slice(0,12) };
}"""

def main():
    url = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else "https://example.com/"
    outdir = "."
    for i, a in enumerate(sys.argv):
        if a == "--out" and i+1 < len(sys.argv): outdir = sys.argv[i+1]
    os.makedirs(outdir, exist_ok=True)
    try: sys.stdout.reconfigure(encoding="utf-8")
    except Exception: pass
    host = urlparse(url).netloc
    reqs = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        ctx = browser.new_context()  # fresh, no stored consent
        page = ctx.new_page()
        page.on("request", lambda req: reqs.append(req.url))
        try:
            page.goto(url, wait_until="load", timeout=45000)
        except Exception:
            try: page.goto(url, timeout=45000)
            except Exception: pass
        page.wait_for_timeout(4000)
        gl = page.evaluate(GLOBALS_JS) or {}
        cookies = ctx.cookies()
        browser.close()
    detected = {}; fired = {"analytics": 0, "marketing": 0, "session": 0, "tag-manager": 0, "consent": 0}
    ga4_ids = set(); gtm_ids = set()
    for u in reqs:
        for sub, cat, label in TRACKERS:
            if sub in u:
                detected[label] = detected.get(label, 0) + 1; fired[cat] = fired.get(cat, 0) + 1
        for m in re.findall(r"[?&]tid=(G-[A-Z0-9]+)", u): ga4_ids.add(m)
        for m in re.findall(r"[?&]id=(GTM-[A-Z0-9]+)", u): gtm_ids.add(m)
    def ck_cat(n):
        if n.startswith(("_ga", "_gid", "_gat", "_pk", "_hj")): return "analytics"
        if n.startswith(("_fbp", "_fbc", "_gcl", "fr", "_uet", "li_", "muc", "_ttp")): return "marketing"
        return "other"
    ck = [{"name": c["name"], "domain": c.get("domain", ""), "cat": ck_cat(c["name"]),
           "thirdParty": host.split(":")[0] not in c.get("domain", "")} for c in cookies]
    out = {"url": url, "analytics": {"ga4": sorted(ga4_ids), "gtm": sorted(gtm_ids),
            "hasDataLayer": gl.get("hasDataLayer"), "gtag": gl.get("gtag"), "fbq": gl.get("fbq")},
           "detected": detected, "firedOnLoadByCategory": fired,
           "cmp": gl.get("cmp", []), "consentMode": gl.get("consentMode"),
           "conversionSignals": {"dataLayerEvents": gl.get("dataLayerEvents", []), "fbq": gl.get("fbq")},
           "cookies": {"total": len(ck), "analytics": sum(1 for c in ck if c["cat"] == "analytics"),
                       "marketing": sum(1 for c in ck if c["cat"] == "marketing"),
                       "thirdParty": sum(1 for c in ck if c["thirdParty"]), "names": [c["name"] for c in ck][:20]},
           "consentRisk": bool((fired.get("marketing", 0) > 0) and not gl.get("consentMode"))}
    json.dump(out, open(os.path.join(outdir, "tracking.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    md = [f"# Measurement readiness — {url}", "",
          "## Analytics & tags",
          f"- **GA4:** {', '.join(out['analytics']['ga4']) or 'not detected'}  ·  **GTM:** {', '.join(out['analytics']['gtm']) or 'not detected'}  ·  dataLayer: {out['analytics']['hasDataLayer']}",
          f"- **Detected on load:** " + (", ".join(f"{k} ({v})" for k, v in detected.items()) or "none"),
          "## Consent",
          f"- **CMP:** {', '.join(out['cmp']) or 'none detected'}  ·  **Google Consent Mode:** {'yes' if out['consentMode'] else 'no'}",
          f"- **Marketing trackers firing before consent:** {fired.get('marketing',0)}  ·  analytics: {fired.get('analytics',0)}"
          + ("  ⚠️ potential GDPR consent issue" if out['consentRisk'] else ""),
          "## Conversion tracking",
          f"- dataLayer events: {', '.join(out['conversionSignals']['dataLayerEvents']) or 'none seen (page load only)'}  ·  Meta pixel: {out['conversionSignals']['fbq']}",
          "## Cookies set on first load",
          f"- {out['cookies']['total']} cookies (analytics {out['cookies']['analytics']}, marketing {out['cookies']['marketing']}, third-party {out['cookies']['thirdParty']})", ""]
    open(os.path.join(outdir, "tracking.md"), "w", encoding="utf-8").write("\n".join(md))
    print("\n".join(md))

if __name__ == "__main__":
    sys.exit(main() or 0)
