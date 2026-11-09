---
name: security
description: >
  A passive, outside-in security check for a website the user owns or is authorised to audit, run on its own
  for now. Reads what the site already shows any visitor: HTTPS and the certificate, security headers,
  cookie flags, version and directory-listing leaks, mixed content, forms, and the public SPF and DMARC email
  records. With the owner's yes it also looks up a list of well-known addresses where sensitive files get
  left by mistake, recording only the status and size, never the contents. Produces plain-language findings in
  Issue · Impact · Fix format, a rubric result and a short verdict. It is not a penetration test and never
  attacks the site. Trigger: "security check", "is my site secure", "security audit", "check my
  headers", "is my SSL fine", "exposed files", "SPF DMARC check", "security scan of my website".
---

# Security (Ananas-Agency — Website Audit)

## Goal

Find the security weaknesses anyone can see from outside, and turn each into a plain-language **Finding** the
owner can hand to a developer. The scan drafts the findings from a reviewed copy table; your job is to run it
safely, then read every finding in the context of this particular site.

Read [references/rules-security.md](references/rules-security.md) before Step 5. It holds the scope rules, the
rubric and the examples of when to change a rating.

## Conversation flow

### Step 1: Show the disclaimer first

**Show this, word for word, as your first message every time this skill runs, before anything else** (before
any question, tool call or command):

> **Before we start: what this security check does and doesn't do**
>
> This is a passive, outside-in check. It reads what your site already shows any visitor: its security settings, certificate, cookies and public email records. It also looks up a list of well-known addresses where sensitive files sometimes get left by mistake. It does not attack the site, try passwords, or open or download anything it finds.
>
> Only run it on a site you own or have permission to audit.
>
> It is not a penetration test. It can't see your server's settings or anything behind a login, so a clean result doesn't prove the site is fully secure. Treat the findings as a to-do list for your developer.

### Step 2: Ask who owns the site

Straight after the disclaimer, first show this warning:

> Some hosting firewalls block a computer that asks for many missing pages, so this computer may be blocked
> from the site for a while after the file check. If that would be a problem, ask your host to allow your IP
> address first.

Then ask once, and wait for the answer:

> Is this your site, or are you authorised to audit it?

- **Yes:** the scan may also look up the exposed-files list (`--probe-files`).
- **No, or no clear answer:** run the scan without `--probe-files`. The passive checks still run, and the
  report says exposed files weren't checked. Don't refuse the whole step, and don't ask again.

Ask for the site's URL in the same message if the user hasn't given one.

### Step 3: Setup check

If it hasn't run in this session, run `python "${CLAUDE_PLUGIN_ROOT}/scripts/setup-check.py"` (use `python3`
where `python` isn't available). This step only needs Python 3.9+. On `MODE: unsupported` or no `MODE:` line,
stop and help the user install Python (python.org, `winget install Python.Python.3.13` on Windows,
`brew install python` on macOS), then run the check again. The `MODE:` line (extended or basic) makes no
difference to this step.

### Step 4: Run the scan

Pick the run folder `audit-<slug>`. If a folder for the same site already exists, reuse it. Otherwise the
slug is the first label of the site's domain, as everywhere in the suite
([audit-data-format.md](../../audit-data-format.md)) (`https://www.ananas-agency.com` becomes
`audit-ananas-agency`).

After a yes, first tell the user that the file check takes several minutes: about 3 to 12 minutes for a
WordPress site and up to about 20 for a site whose platform isn't recognised, because it waits 2 seconds
between addresses plus however long the server takes to answer. Run it in the background, or with the
longest timeout the shell tool allows. It prints a progress line every 10 addresses.

```
python "${CLAUDE_PLUGIN_ROOT}/scripts/security-scan.py" <URL> --probe-files --out "audit-<slug>"
```

If it times out, never run it again without asking the user: a second run doubles the load that trips
hosting firewalls.

After a no, run the same command without `--probe-files`.

It writes `security-scan.json`, `audit-data/security.json` and a first `security.md` into the run folder.
On **exit 2** the address isn't a valid URL: fix it and run the command once more.
On **exit 3** the scan couldn't reach or read the site, and it says why in one line (for example, the address
redirects to another site): tell the user in one plain sentence and stop. Don't retry in a loop or try other
addresses.

### Step 5: Review the findings in the site's context

Read `audit-<slug>/audit-data/security.json` and the rules file. Look at every finding against what this site
actually is (a static brochure, a shop, a login portal, a domain that sends no email). Then edit the JSON with
the file-editing tool, not a shell heredoc ([audit-data-format.md](../../audit-data-format.md)):

- Reword a line (`issue`, `impact_text`, `fix`) or change `impact` or `effort` only when the site warrants it.
  The examples are in the rules file. Otherwise leave the draft as it is.
- Keep every field the format requires, and keep `measured: true` on scan-backed findings.
- If a finding's `impact` moves across 4 (from high to not high, or the reverse), update that finding's
  rubric row by the same rule the draft uses: `Fail` if any finding in the row has impact 4 or more, even
  when the row wasn't fully checked; otherwise `Partial` if the row wasn't fully checked or has any finding;
  otherwise `Pass`.
- Rewrite `verdict` as one plain sentence about this site. Never say in the `verdict` that the site is
  secure.
- Never add a finding the scan didn't make. Never add a strength.
- Never delete a finding. When a finding is demonstrably wrong for this site, lower its `impact` to 1 and say
  why in the plain-words line (`issue`).
- Never remove or soften a not-checked note in `notes`.
- **Never put a cookie value or the contents of a file in any field.** Names, statuses and sizes only.
- Follow "Write like a human" in [report-format.md](../../report-format.md).

### Step 6: Rebuild and hand off

Run `python "${CLAUDE_PLUGIN_ROOT}/scripts/security-report.py" "audit-<slug>"`. It checks the JSON again and
rewrites `security.md`. On **exit 2** it prints what is wrong: fix each field it names and run it again.

Then give the user the three or four highest-priority findings in a few plain lines (title and the one-line
reason), and the path to `audit-<slug>/security.md`. Say that this step runs on its own for now and isn't
part of the Action Report yet.

## Critical rules

1. **Passive only.** Never request anything the scan doesn't, never test logins, never try payloads. The
   scope rules are in the rules file.
2. **Disclaimer first, question once, probe only after a yes.**
3. **No secrets in the output.** No cookie values, no file contents, no keys, in any field or in chat.
4. **Honest about limits.** A clean result doesn't prove the site is secure. Say so if the user asks "so am
   I safe?".
5. **Plain language.** The reader is a business owner. Explain a term the first time it appears.

---

## License

Copyright (c) 2026 Kostiantyn Ivanov (Ananas-Agency, ananas-agency.com).

Released under the MIT License. Keeping the copyright notice is all that is required, and a credit to the author is warmly appreciated. Full license text: [LICENSE](../../LICENSE)
