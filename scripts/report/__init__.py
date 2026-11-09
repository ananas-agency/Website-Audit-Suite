"""Report builder package for the Website Audit Suite (standard library only)."""

# Dimension pages in walk order: (page, finding ID prefix, title, utm campaign).
DIMENSIONS = (
    ("messaging", "MSG", "Messaging & Clarity", "messaging-clarity"),
    ("conversion", "CRO", "Conversion (CRO)", "conversion-cro"),
    ("seo", "SEO", "SEO & Content", "seo-content"),
    ("ux-technical", "UX", "UX & Technical", "ux-technical"),
    ("design", "DSN", "Design & Visual", "design-visual"),
)

# The seven scan files the scanners write into the run folder.
SCAN_FILES = (
    "perf-a11y.json",
    "mobile-metrics.json",
    "design-tokens.json",
    "seo-sweep.json",
    "tracking.json",
    "interaction.json",
    "design-pages.json",
)

# Which scan files can back a measured finding on each page. A page not listed (messaging) is backed by any scan.
SCAN_BACKING = {
    "conversion": ("tracking.json", "interaction.json", "mobile-metrics.json"),
    "seo": ("seo-sweep.json",),
    "ux-technical": ("perf-a11y.json", "mobile-metrics.json", "interaction.json", "design-tokens.json"),
    "design": ("design-tokens.json", "design-pages.json"),
}

# Scan files whose scanner needs no browser, so a Basic run can have them (seo-sweep.py is standard library only).
BROWSERLESS_SCANS = ("seo-sweep.json",)

BENCHMARK_STATUSES = ("met", "gap", "na")
RESULTS = ("Pass", "Partial", "Fail")
KEY_PATTERN = r"^[a-z0-9][a-z0-9-]*$"
# A [[key]] reference as written in prose: no spaces or brackets inside. Used by validation and the renderer.
KEY_REF = r"\[\[([^\[\]\s]+)\]\]"
