# Security rules (Skill 8)

How to run and review the Security step. The scan drafts every finding; these rules say what is allowed and
when to change a draft.

## Scope (the rule the whole step lives inside)

The audit is for a site the user owns or is authorised to audit. Every check is passive and non-intrusive.

**In scope (read-only):**
- What the server already sends: response headers, TLS and certificate, cookies, HTML, `robots.txt`,
  `sitemap.xml`, `security.txt`.
- The domain's public DNS (SPF, DMARC).
- With a yes to the ownership question: a small, fixed list of well-known sensitive paths. Only the HTTP
  status, content type and length are recorded, never the contents.

**Out of scope, never:**
- Payloads of any kind (SQL injection, XSS, login bypass), or guessing passwords.
- Large-scale or recursive path guessing.
- Using anything found, or downloading the contents of an exposed file.
- Load or stress testing.
- Any host other than the target site and its own domain.

The disclaimer is shown first on every run, then the ownership question once. Without a yes, the exposed-files
probe doesn't run and its rubric row is `Partial`, with the reason in `notes`.

## Rubric

Every row is rated Pass, Partial or Fail. The builder turns the results into the grade (Pass is the full
weight, Partial half, Fail none). The weights sum to 100.

| Criterion | Weight |
|---|---:|
| No sensitive files/paths exposed | 20 |
| HTTPS & TLS (version, cert validity, HSTS) | 18 |
| Security headers present and strong | 18 |
| No information disclosure (version/listing/mixed content) | 14 |
| Cookie flags (Secure/HttpOnly/SameSite) | 12 |
| Email/domain spoofing protection (SPF/DMARC) | 10 |
| Forms sent over HTTPS | 8 |

The draft's rule for a row: `Fail` if any finding in the row has impact 4 or more, even when the row wasn't
fully checked; otherwise `Partial` if the row wasn't fully checked or has any finding; otherwise `Pass`.
After you change an impact, apply the same rule again to that finding's row.

## When to adjust a draft

Change a rating or a line only when this site gives a reason. The default wording is reviewed, so most
findings should stay as drafted.

- **Missing Content-Security-Policy on a static brochure site.** No forms, no logins, no user content. The
  draft's impact is too high: lower it (for example to 2) and say in the plain-words line that the risk is
  small because the site collects nothing. If the same gap is on a shop or a login page, leave it.
- **Missing DMARC on a domain that sends no email.** If the site's contact details show the business uses
  another domain for mail, or the domain has no mail records at all, lower the impact and say that the
  record still helps stop others faking the domain. If the domain sends newsletters or order emails, raise it
  or leave it high.
- **Missing X-Frame-Options or similar on a page with nothing to click.** Lower it. On a payment or admin
  page, leave it.
- **A server version header on a site behind a managed host.** Leave it, but keep the fix short: ask the host
  to hide it.
- **A cookie flag finding for a cookie that only stores a harmless preference.** Lower it. For a session or
  login cookie, leave it.
- **A `cert-untrusted` finding.** On Windows, Python can lack root certificates that a browser has, so
  confirm a `cert-untrusted` warning in a browser before keeping it HIGH.

**Possible backdoors and admin tools.** Never write that the site was hacked: a matching file name alone
doesn't prove a break-in. Never remove a `possible-backdoor` finding either. The user saying their developer
added the file on purpose isn't enough to lower it, because a deliberate `cmd.php` or `shell.php` that
answers publicly may itself let anyone run commands. Lower it only once the developer confirms the file can't
run commands or manage files, and say why in the plain-words line. If it can, keep the impact at 4 or more,
as for an exposed admin tool (below 4, the Files row can drop from `Fail` to `Partial`). An
`exposed-admin-tools` hit with status `401` means the tool asks for a password first. It still counts, because
a login page anyone can reach invites password guessing.

Raise a rating only for a clear reason, such as the site taking payments or personal details. Never invent a
finding the scan didn't make, and never change `evidence`: it is what was actually measured.

## What never goes in a field

- No cookie values. A name and its flags are fine.
- No file contents. A path, status, content type and length are fine.
- No passwords, keys or tokens, even if one shows up in a page you read.

## Write like a human

The owner reads this, not a developer. Short sentences, plain words, a term explained the first time
(HSTS: a rule telling browsers to always use the secure version of your site). Few em-dashes, no stacked
adjectives, no "not X, it's Y". The full list is in [report-format.md](../../../report-format.md), "Write like
a human".
