"""The security step's constants: the disclaimer, the ownership question, the rubric and the directory list (the exposed-file lists live in paths.py).

The disclaimer is the owner-approved text, word for word; `8 Security/security/SKILL.md` carries the same text
(a test keeps them equal). It is shown first in every run, heads `security.md`, and is the first `extra` block
of `security.json`.
"""

DISCLAIMER_HEADING = "Before we start: what this security check does and doesn't do"
# Three paragraphs separated by a blank line; no line breaks inside a paragraph.
DISCLAIMER_BODY = (
    "This is a passive, outside-in check. It reads what your site already shows any visitor: its security "
    "settings, certificate, cookies and public email records. It also looks up a list of well-known addresses "
    "where sensitive files sometimes get left by mistake. It does not attack the site, try passwords, or open or "
    "download anything it finds."
    "\n\n"
    "Only run it on a site you own or have permission to audit."
    "\n\n"
    "It is not a penetration test. It can't see your server's settings or anything behind a login, so a clean "
    "result doesn't prove the site is fully secure. Treat the findings as a to-do list for your developer."
)
DISCLAIMER_EXTRA_TITLE = "What this check does and doesn't do"
OWNERSHIP_QUESTION = "Is this your site, or are you authorised to audit it?"

USER_AGENT = "WebsiteAuditSuite-SecurityCheck/1.0 (+https://ananas-agency.com)"

# (criterion, weight), in report order; the weights sum to 100.
RUBRIC = (
    ("No sensitive files/paths exposed", 20),
    ("HTTPS & TLS (version, cert validity, HSTS)", 18),
    ("Security headers present and strong", 18),
    ("No information disclosure (version/listing/mixed content)", 14),
    ("Cookie flags (Secure/HttpOnly/SameSite)", 12),
    ("Email/domain spoofing protection (SPF/DMARC)", 10),
    ("Forms sent over HTTPS", 8),
)

# Folders checked for an open directory listing ("Index of /").
DIRECTORY_PATHS = ("/wp-content/uploads/", "/uploads/", "/images/")
