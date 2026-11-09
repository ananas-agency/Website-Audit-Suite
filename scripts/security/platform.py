"""Recognise the site's platform from the homepage response already fetched (no extra requests).

Only structural signals count: generator meta, asset paths in src/href, cookie names, header names and
values, form field names. Words in the page text never do. Cookie values are never read.
"""
from __future__ import annotations

import re
from html.parser import HTMLParser
from typing import List

from .checks import Response, values
from .paths import CORE_PATHS, PHP_PLATFORMS, PLATFORM_PATHS


_ASSET_TAGS = ("script", "img", "source", "iframe", "embed", "video", "audio")


class _Signals(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.generators: List[str] = []
        self.urls: List[str] = []       # lowercased src and href values
        self.fields: List[str] = []     # lowercased input name/id values
        self.csrf_param = False

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v or "") for k, v in attrs}
        if tag == "meta":
            name = a.get("name", "").lower()
            if name == "generator":
                self.generators.append(a.get("content", "").strip().lower())
            elif name == "csrf-param" and a.get("content", "").strip() == "authenticity_token":
                self.csrf_param = True
        # asset paths only: a link to a document (<a href>) says nothing about the platform
        attr = "href" if tag == "link" else "src" if tag in _ASSET_TAGS else None
        if attr and a.get(attr):
            self.urls.append(a[attr].lower())
        if tag == "input":
            self.fields.extend(a[k].lower() for k in ("name", "id") if a.get(k))


def _cookie_names(resp: Response) -> List[str]:
    names = []
    for raw in values(resp, "Set-Cookie"):
        first = raw.split(";", 1)[0]
        if "=" in first:
            names.append(first.split("=", 1)[0].strip().lower())
    return names


def detect_platforms(resp: Response) -> List[str]:
    names = [k.lower() for k, _ in resp.headers]
    redirect_by = any("wordpress" in v.lower() for v in values(resp, "X-Redirect-By"))
    if not 200 <= resp.status < 300:   # a redirect or error page tells nothing: probe every list
        return ["php", "wordpress"] if redirect_by else []
    page = _Signals()
    try:
        page.feed(resp.body or "")
        page.close()
    except Exception:  # malformed HTML must never break detection
        pass
    cookies = _cookie_names(resp)

    def header_has(name, *needles):
        return any(n.lower() in v.lower() for v in values(resp, name) for n in needles)

    def header_word(name, word):
        return any(re.search(chr(92) + "b" + re.escape(word) + chr(92) + "b", v, re.I) for v in values(resp, name))

    def header_named(prefix):
        return any(n.startswith(prefix) for n in names)

    def url_has(*needles):
        return any(n in u for u in page.urls for n in needles)

    def gen_has(*prefixes):
        return any(g.startswith(p.lower()) for g in page.generators for p in prefixes)

    found = set()
    if gen_has("WordPress") or url_has("/wp-content/", "/wp-includes/") or header_has("Link", "wp-json"):
        found.add("wordpress")
    if (gen_has("Drupal") or header_has("X-Generator", "Drupal") or header_named("x-drupal-")
            or url_has("/sites/default/files/")):
        found.add("drupal")
    if gen_has("Joomla") or url_has("/media/jui/", "/media/system/js/"):
        found.add("joomla")
    if (header_named("x-magento-") or "mage-cache-sessid" in cookies or "mage-messages" in cookies
            or url_has("/static/version")):
        found.add("magento")
    if "laravel_session" in cookies:
        found.add("laravel")
    if "x-debug-token" in names or "x-debug-token-link" in names:
        found.add("symfony")
    if header_has("X-Powered-By", "Craft CMS") or "craftsessionid" in cookies:
        found.add("craft")
    if found.intersection(PHP_PLATFORMS) or header_has("X-Powered-By", "PHP") or "phpsessid" in cookies:
        found.add("php")
    if (header_word("X-Powered-By", "Express") or header_has("X-Powered-By", "Next.js") or "connect.sid" in cookies
            or url_has("/_next/", "/_nuxt/") or gen_has("Ghost", "Next.js")):
        found.add("node")
    if ("csrftoken" in cookies or "csrfmiddlewaretoken" in page.fields
            or header_has("Server", "WSGIServer", "Werkzeug", "gunicorn", "uvicorn")):
        found.add("python")
    if (page.csrf_param or header_has("Server", "Phusion Passenger")
            or header_has("X-Powered-By", "Phusion Passenger") or "x-runtime" in names):
        found.add("rails")
    if ("jsessionid" in cookies or header_has("Server", "Apache-Coyote", "Tomcat", "Jetty", "WildFly", "JBoss")
            or header_has("X-Powered-By", "Servlet", "JSP", "JSF")):
        found.add("java")
    if (header_has("X-Powered-By", "ASP.NET") or "x-aspnet-version" in names or "x-aspnetmvc-version" in names
            or "asp.net_sessionid" in cookies or any(c.startswith(".aspnetcore.") for c in cookies)
            or header_has("Server", "Microsoft-IIS") or "__viewstate" in page.fields):
        found.add("dotnet")
    if gen_has("Hugo", "Jekyll", "Gatsby", "Eleventy"):
        found.add("static")
    return sorted(found)


def select_paths(platforms: List[str]) -> List[tuple]:
    """The core list plus each recognised platform's list; every list when nothing was recognised."""
    keys = [p for p in platforms if p in PLATFORM_PATHS] or list(PLATFORM_PATHS)
    out, seen = [], set()
    for entry in CORE_PATHS + tuple(e for k in keys for e in PLATFORM_PATHS[k]):
        if entry[0] not in seen:
            seen.add(entry[0])
            out.append(entry)
    return out
