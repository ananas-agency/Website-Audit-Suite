"""The security step's copy table: plain-words text and default ratings for every check id.

Code drafts each finding from this table and Claude adjusts the wording or ratings for a specific site.
The four parts map onto the finding JSON:
- `title`: names the problem; a technical term may close it in brackets
- `issue` ("In plain words"): what it is, for a non-technical owner, with no jargon
- `impact_text` ("Why you should care"): the real-world risk to their business or visitors
- `fix` (for the developer): the technical action. The scanner supplies the evidence separately.
Prose follows report-format.md, "Write like a human".
"""
from dataclasses import dataclass
from typing import Optional

from . import RUBRIC


@dataclass(frozen=True)
class Check:
    criterion: Optional[str]  # a RUBRIC criterion, or None when the finding moves no row
    impact: int
    effort: int
    title: str
    issue: str
    impact_text: str
    fix: str


FILES, HTTPS, HEADERS, INFO, COOKIES, EMAIL, FORMS = (name for name, _ in RUBRIC)

CHECKS = {
    # --- No sensitive files/paths exposed ---
    "exposed-secrets": Check(
        FILES, 5, 1,
        title="Private files on your site are open to anyone",
        issue=("Files that should never be public, such as password and settings files or database backups, "
               "can be reached at web addresses anyone can type in. The check only saw that they exist; "
               "it didn't open them."),
        impact_text=("These files often hold the passwords and keys to your database, email or payment accounts. "
                     "Automated bots look for these exact files all the time, so anyone who finds them could "
                     "copy customer data or take over the site."),
        fix=("Delete the listed files from the web root or deny access to them in the server config. Then change "
             "every password, API key and token they contained: assume they have been copied."),
    ),
    "exposed-info-files": Check(
        FILES, 3, 1,
        title="Files that show how your site is built are public",
        issue=("Some behind-the-scenes files are open to anyone, for example a list of the software your site is "
               "built with or a list of its usernames. They usually hold no passwords, but they weren't meant "
               "for visitors."),
        impact_text=("They give an attacker a head start, such as which software versions to target or which "
                     "usernames to try. On their own they rarely cause harm."),
        fix=("Remove the listed files from the web root or deny access to them in the server config. For "
             "`/wp-json/wp/v2/users`, limit the WordPress users endpoint to logged-in users."),
    ),
    "exposed-admin-tools": Check(
        FILES, 4, 1,
        title="A database or admin tool on your site can be reached by anyone",
        issue=("One or more tools for managing your site behind the scenes, such as a database manager, can be "
               "reached at web addresses anyone can type in. Each may ask for a password first, or may open "
               "straight away. The check only saw an answer; it didn't try to log in."),
        impact_text=("Automated bots look for these tools and try common passwords on them, so one weak or reused "
                     "password could let someone in. If a tool opens without a password, anyone who finds it "
                     "could read or change your site's data."),
        fix=("Remove or disable the listed tools if nobody needs them. Otherwise allow them only from known IP "
             "addresses or over a VPN (in the server, firewall or host settings), and keep them updated."),
    ),
    "possible-backdoor": Check(
        FILES, 5, 2,
        title="Your site seems to have a file named like a hacking tool (possible backdoor)",
        issue=("Attackers who get into a site often leave a backdoor, a hidden way back in, and many give it one of "
               "a few well-known file names. Your site answered when the check asked for one or more of those "
               "names. An ordinary file can have the same name, so a match may be harmless. The check didn't look "
               "at what's there, so your developer should."),
        impact_text=("If a match is a backdoor, whoever put it there could change your site or read its data at "
                     "any time. Your developer can usually tell by looking at the file, so have this checked "
                     "soon."),
        fix=("Read the listed files' code on the server (SSH, SFTP or the host's file manager); opening them in a "
             "browser would run them. If a file isn't yours: note its modified date (or keep an offline copy), "
             "remove it, check the access logs around that date, look for other signs of a break-in (changed "
             "files, unknown admin users), and change every password and key the site uses."),
    ),
    "exposed-unclear": Check(
        FILES, 2, 1,
        title="Some private file addresses need a manual check",
        issue=("Your site shows a normal page for any address, even ones that don't exist. So when the check "
               "asked for well-known private files, it couldn't tell whether they're really there."),
        impact_text=("Most likely nothing is exposed and this is just how your site handles missing pages. But if "
                     "one of these addresses does lead to a real file or tool, it could hold passwords or backups, "
                     "or give access to your site, so it deserves a quick look."),
        fix=("Check each listed path on the server rather than in a browser: opening a script (`.php`, `.aspx`, "
             "`.jsp`) would run it. Better, make the server answer missing pages with a real `404` status and "
             "run the check again."),
    ),

    # --- HTTPS & TLS ---
    "no-https": Check(
        HTTPS, 5, 3,
        title="Your site doesn't use a secure connection (no HTTPS)",
        issue=("Your site only opens over an unprotected connection, so everything visitors see and send travels "
               "across the internet without protection."),
        impact_text=("Browsers label the site 'Not secure', which can put people off before they read a word. "
                     "On public Wi-Fi, someone nearby could read or change what a visitor sends, including "
                     "anything typed into your forms."),
        fix=("Install a TLS certificate (free from Let's Encrypt or most hosts), serve the whole site over HTTPS, "
             "and redirect every `http://` URL to `https://` with a 301."),
    ),
    "no-https-redirect": Check(
        HTTPS, 4, 1,
        title="The unprotected version of your site still opens (no HTTPS redirect)",
        issue=("In some browsers, someone who types your address without 'https', or follows an old link, can "
               "land on the unprotected version of your site instead of being moved to the secure one."),
        impact_text=("Those visitors may see 'Not secure' in the address bar, and anything they type into a form "
                     "would travel unprotected."),
        fix=("Redirect every `http://` request to the same path on `https://` with a 301, in the server config "
             "or the host's HTTPS setting."),
    ),
    "old-tls": Check(
        HTTPS, 3, 2,
        title="Your server still accepts outdated encryption (TLS 1.0/1.1)",
        issue=("Your site still accepts secure connections that use old versions of the encryption, which most "
               "major browsers stopped using around 2020."),
        impact_text=("The risk to everyday visitors is low, because their browsers use the newer versions. But the "
                     "old ones have known weaknesses, and if you take card payments, the card industry's "
                     "security rules have banned the oldest of them since 2018."),
        fix=("Disable TLS 1.0 and 1.1 in the server, load balancer or CDN settings, and allow only TLS 1.2 and "
             "1.3. PCI DSS has banned TLS 1.0 since 30 June 2018, and RFC 8996 deprecates both."),
    ),
    "cert-expired": Check(
        HTTPS, 5, 1,
        title="Your security certificate has expired",
        issue="The certificate that proves your site is really yours has passed its end date.",
        impact_text=("Browsers now show visitors a full-page warning that the site may be unsafe. Most people "
                     "leave at that point, so you are likely losing visits and enquiries right now."),
        fix="Renew the certificate now and turn on automatic renewal (most hosts and Let's Encrypt clients do this).",
    ),
    "cert-expiring": Check(
        HTTPS, 4, 1,
        title="Your security certificate expires within 15 days",
        issue=("The certificate that proves your site is really yours has an end date, and it's less than "
               "15 days away."),
        impact_text=("If it isn't renewed in time, visitors will get a full-page warning and most will leave. "
                     "Automatic renewal usually happens well before this point, so check that it's working."),
        fix=("Renew the certificate before the date shown and find out why automatic renewal hasn't run "
             "(for example a failing certbot timer or a broken DNS validation)."),
    ),
    "cert-name-mismatch": Check(
        HTTPS, 5, 2,
        title="Your security certificate is for a different address",
        issue=("The certificate your site shows doesn't match the address visitors use. This often happens when "
               "it covers 'www.yoursite.com' but not 'yoursite.com', or the other way round."),
        impact_text=("Browsers can't confirm visitors have reached the real site, so they show a full-page warning "
                     "that the connection isn't private. Most people turn back at that point."),
        fix=("Issue a certificate that lists every hostname the site answers on (for example both `example.com` "
             "and `www.example.com`) and install it."),
    ),
    "cert-untrusted": Check(
        HTTPS, 5, 2,
        title="Browsers don't trust your security certificate",
        issue=("Your certificate wasn't issued by a company that browsers recognise, or your server leaves out "
               "part of the proof browsers need to check it."),
        impact_text=("Many visitors see a full-page warning that the site may be unsafe, and most of them will "
                     "leave instead of clicking through."),
        fix=("Use a certificate from a public certificate authority (Let's Encrypt is free) and serve the full "
             "chain, including the intermediate certificates."),
    ),
    "no-hsts": Check(
        HTTPS, 3, 1,
        title="Browsers aren't told to always use the secure version (no HSTS)",
        issue=("Your site doesn't tell browsers to stick to the secure connection. So a visitor's browser may "
               "still try the unprotected version first, for example when they type your address without "
               "'https'."),
        impact_text=("On public Wi-Fi, someone nearby could use that moment to show the visitor a tampered page "
                     "instead of yours. It's an uncommon attack, and the fix takes minutes."),
        fix=("Send `Strict-Transport-Security: max-age=31536000` on every HTTPS response; add "
             "`includeSubDomains`, then `preload`, once every subdomain serves HTTPS."),
    ),
    "hsts-weak": Check(
        HTTPS, 2, 1,
        title="The 'always use the secure version' rule is only partly set (weak HSTS)",
        issue=("Your site does tell browsers to stick to the secure connection, but the instruction lasts less "
               "than six months, or doesn't cover other addresses on your domain such as shop.yourdomain.com."),
        impact_text=("The protection works for most visits. The gaps are for people who haven't visited in a "
                     "while, or for the other addresses on your domain."),
        fix=("Set `max-age` to at least `15552000` (one year, `31536000`, is usual) and add `includeSubDomains` "
             "once every subdomain serves HTTPS."),
    ),

    # --- Security headers present and strong ---
    "no-csp": Check(
        HEADERS, 3, 3,
        title="Nothing limits what code can run on your pages (no CSP)",
        issue=("Your site doesn't give browsers a list of the places its code is allowed to come from, so a "
               "browser will run any code that ends up on a page."),
        impact_text=("If an attacker ever slips their own code onto your site, for example through a plugin flaw "
                     "or a hacked third-party tool, nothing limits what it can load or where it sends data. It "
                     "could read what visitors type into forms or send them to another site."),
        fix=("Add a `Content-Security-Policy` header. Start in `Content-Security-Policy-Report-Only` mode to see "
             "what the site loads, then enforce a policy built on `default-src 'self'` plus the third-party "
             "domains you use."),
    ),
    "weak-csp": Check(
        HEADERS, 2, 3,
        title="Your rules on what code can run have loopholes (weak CSP)",
        issue=("Your site does list where its code may come from, but the list has broad exceptions, such as "
               "allowing code written straight into the page, code built on the fly, or code loaded from "
               "anywhere."),
        impact_text=("These exceptions are exactly the gaps injected code relies on, so the rules may not stop "
                     "harmful code that gets onto a page."),
        fix=("Remove `'unsafe-inline'`, `'unsafe-eval'` and wildcard (`*`) sources from `script-src` and "
             "`default-src`. Use nonces or hashes for inline scripts that must stay."),
    ),
    "no-frame-protection": Check(
        HEADERS, 3, 1,
        title="Other sites can show your pages inside theirs (no clickjacking protection)",
        issue=("Nothing stops another website from loading your pages inside one of its own, where it can hide "
               "or cover them."),
        impact_text=("A scam page could hide your real site behind a decoy and trick visitors into clicking your "
                     "buttons without knowing, such as 'confirm' or 'delete'. Modern browsers make this harder "
                     "than it used to be, and it matters mainly if your site has logins or payments."),
        fix=("Send `Content-Security-Policy: frame-ancestors 'self'`, plus `X-Frame-Options: SAMEORIGIN` for "
             "older browsers."),
    ),
    "no-nosniff": Check(
        HEADERS, 2, 1,
        title="Browsers are left to guess what your files are (no X-Content-Type-Options)",
        issue=("Your site doesn't stop browsers from second-guessing what kind of file they've been sent, so a "
               "browser might treat an uploaded text file as code."),
        impact_text=("This matters mainly if people can upload files to your site: a disguised upload could then "
                     "run in a visitor's browser. For most sites the risk is small, and the fix is one line."),
        fix="Send `X-Content-Type-Options: nosniff` on every response.",
    ),
    "no-referrer-policy": Check(
        HEADERS, 1, 1,
        title="No rule for what other sites learn when visitors click away (no Referrer-Policy)",
        issue=("When a visitor clicks a link from your site to another one, their browser tells that site where "
               "they came from. Your site doesn't set a rule for how much of that address to share."),
        impact_text=("Modern browsers share only your domain by default, so this only matters in older browsers, "
                     "and only if your page addresses contain private details, such as a search term or a "
                     "password reset link."),
        fix="Send `Referrer-Policy: strict-origin-when-cross-origin` (or stricter).",
    ),
    "unsafe-referrer-policy": Check(
        HEADERS, 2, 1,
        title="Your site shares visitors' full page addresses with other sites (unsafe Referrer-Policy)",
        issue=("Your site tells browsers to pass the full address of the page a visitor was on to every site "
               "they click through to, even from a secure page to an unprotected one."),
        impact_text=("If those addresses ever include private details, such as an order number or a password reset "
                     "link, other sites receive them too."),
        fix="Set `Referrer-Policy: strict-origin-when-cross-origin` (or `no-referrer`) instead of `unsafe-url`.",
    ),
    "no-permissions-policy": Check(
        HEADERS, 1, 1,
        title="Your site doesn't switch off browser features it doesn't use (no Permissions-Policy)",
        issue=("Your site doesn't tell browsers which features, such as the camera, microphone or location, its "
               "pages may use."),
        impact_text=("Browsers still ask visitors before using any of these, so the risk is low. Switching them "
                     "off is extra protection in case third-party code on your pages, such as ads or widgets, "
                     "asks for something it shouldn't."),
        fix=("Send a `Permissions-Policy` header that turns off unused features, e.g. "
             "`camera=(), microphone=(), geolocation=()`."),
    ),
    "no-cross-origin-policies": Check(
        HEADERS, 1, 2,
        title="Your pages don't ask to be kept apart from other sites (no cross-origin policies)",
        issue=("Your site doesn't use the newer browser settings that keep its pages and files apart from other "
               "websites open in the same browser."),
        impact_text=("These settings guard against rare, advanced attacks that try to read information across "
                     "browser tabs. Few sites need them urgently, so treat this as a later improvement."),
        fix=("Send `Cross-Origin-Opener-Policy: same-origin` (use `same-origin-allow-popups` if the site opens "
             "login or payment pop-ups), and `Cross-Origin-Resource-Policy: same-site` on files other sites "
             "don't need to embed. Add `Cross-Origin-Embedder-Policy: require-corp` only after testing, because "
             "it can block third-party embeds."),
    ),
    "outdated-xss-header": Check(
        HEADERS, 1, 1,
        title="Your site sends an outdated browser instruction (X-XSS-Protection)",
        issue=("Your site still sends an old instruction for a browser safety filter that modern browsers have "
               "removed."),
        impact_text=("Modern browsers ignore it, and in some older ones the filter itself could be misused against "
                     "your pages. Removing it is low-priority tidy-up."),
        fix=("Remove the `X-XSS-Protection` header (or set it to `0`) and rely on a `Content-Security-Policy` "
             "instead."),
    ),

    # --- No information disclosure ---
    "server-version": Check(
        INFO, 2, 1,
        title="Your server announces its software version",
        issue="Your server tells every visitor's browser the name and exact version of the software it runs.",
        impact_text=("If that version has a known security hole, attackers can spot it at a glance and know what "
                     "to try. Hiding the number won't fix old software, but it makes your site a less obvious "
                     "target."),
        fix=("Hide version numbers in the `Server`, `X-Powered-By` and `X-AspNet-Version` headers (e.g. "
             "`server_tokens off;` in nginx, `expose_php = Off` in PHP), and keep that software updated."),
    ),
    "generator-version": Check(
        INFO, 2, 1,
        title="Your pages name your website software and its version",
        issue=("Hidden in each page's code is a line naming the software your site is built with and its exact "
               "version, such as a WordPress version number."),
        impact_text=("Attackers search for that line to find sites running versions with known holes. If you're up "
                     "to date it does little harm, but it points them your way the moment you fall behind."),
        fix=("Remove the `<meta name=\"generator\">` tag (in WordPress, "
             "`remove_action('wp_head', 'wp_generator');`) and keep the platform updated."),
    ),
    "directory-listing": Check(
        INFO, 4, 1,
        title="Anyone can browse some of your folders (directory listing)",
        issue=("Some folders on your site show a list of every file inside them to anyone who visits that "
               "address, like an open filing cabinet."),
        impact_text=("Any file in those folders, including ones you never linked to, such as invoices or files sent "
                     "through your forms, can be found and downloaded by anyone, and search engines may list them."),
        fix=("Turn off directory listings: `Options -Indexes` in Apache, `autoindex off;` in nginx, or an empty "
             "`index.html` in each listed folder."),
    ),
    "mixed-content": Check(
        INFO, 3, 2,
        title="Your secure pages load some files insecurely (mixed content)",
        issue=("Your pages use the secure connection, but some images or other files on them still load over the "
               "old, unprotected one."),
        impact_text=("Browsers block or upgrade most of these files, which can break parts of the page. Older "
                     "browsers may load them anyway, and someone on the same network could swap them for "
                     "something harmful."),
        fix=("Change the listed `http://` URLs to `https://` in the templates and content, and add "
             "`Content-Security-Policy: upgrade-insecure-requests` as a safety net."),
    ),
    "robots-names-sensitive-areas": Check(
        INFO, 2, 1,
        title="A public file for search engines points to sensitive areas (robots.txt)",
        issue=("Your site has a public file that asks search engines to skip certain pages, and it names areas "
               "such as your admin or login pages, a test copy of the site, or backups."),
        impact_text=("Anyone can read that file, and it only asks search engines to stay away. If it names areas "
                     "that aren't already common knowledge, it works as a signpost to the places you'd least like "
                     "strangers to find."),
        fix=("Remove sensitive paths from `robots.txt`. Protect those areas with a login or an IP allow-list, and "
             "use `noindex` on the pages to keep them out of search results."),
    ),
    "sitemap-lists-sensitive-urls": Check(
        INFO, 2, 1,
        title="Your sitemap lists pages that should stay out of sight (sitemap.xml)",
        issue=("The list of pages your site hands to search engines includes addresses for areas such as admin "
               "or login pages, a test copy of the site, or backups."),
        impact_text=("Search engines may show those pages in their results, and anyone can read the list. That "
                     "makes private areas easier to find and target."),
        fix=("Remove the listed URLs from `sitemap.xml` (most sitemap plugins have an exclude setting) and add "
             "`noindex` to those pages."),
    ),

    # --- Cookie flags ---
    "cookie-no-secure": Check(
        COOKIES, 3, 1,
        title="Some cookies can travel over an unprotected connection (no Secure flag)",
        issue=("Some cookies your site sets aren't marked as secure-only, so a browser will also send them over "
               "an unprotected connection."),
        impact_text=("If one of them keeps a visitor logged in, someone on the same public Wi-Fi could copy it and "
                     "use the account as that visitor."),
        fix="Add the `Secure` attribute to the listed cookies, in the app, framework or CMS cookie settings.",
    ),
    "cookie-no-httponly": Check(
        COOKIES, 3, 1,
        title="Some cookies can be read by code on your pages (no HttpOnly flag)",
        issue=("Some cookies your site sets can be read by any code running on your pages, not only by your "
               "server."),
        impact_text=("If harmful code ever gets onto a page, it could read a login cookie and take over that "
                     "visitor's account. Cookies used only by analytics or chat tools carry less risk."),
        fix=("Add `HttpOnly` to the listed cookies unless front-end code really needs to read them. Session and "
             "login cookies always need it."),
    ),
    "cookie-no-samesite": Check(
        COOKIES, 2, 1,
        title="Some cookies don't say whether to go along with requests from other sites (no SameSite setting)",
        issue=("Some cookies don't say whether they should be sent along when another website links to or sends "
               "a form to your site, so each browser decides for itself."),
        impact_text=("Chrome and Edge fill in a safe default, so the risk is limited. In some other browsers, "
                     "another site could make a logged-in visitor do things on your site without knowing, unless "
                     "your site guards against it in other ways."),
        fix=("Set `SameSite=Lax` on the listed cookies (`Strict` only for cookies that guard sensitive actions; "
             "`None` only with `Secure`, for genuine cross-site use)."),
    ),
    "cookie-broad-domain": Check(
        COOKIES, 2, 1,
        title="Some cookies are shared with every address on your domain (broad cookie scope)",
        issue=("Some cookies are set to be shared with every address on your domain, such as blog.yourdomain.com "
               "or shop.yourdomain.com, not only with this site."),
        impact_text=("If any of those other sites is run by an outside company or gets hacked, it could read or "
                     "overwrite these cookies, which matters most if any of them keep people logged in."),
        fix=("Remove the `Domain` attribute from the listed cookies so they stay on this host, or narrow it to the "
             "one hostname that needs them."),
    ),

    # --- Email/domain spoofing protection ---
    "no-spf": Check(
        EMAIL, 4, 1,
        title="Your domain doesn't list who may send its email (no SPF)",
        issue=("There's no published list of the services allowed to send email from your domain, so inboxes "
               "have one less way to check whether a message really came from you."),
        impact_text=("Your genuine emails are more likely to land in spam, and if your domain has no other email "
                     "protection, fake emails in your name are easier to pass off."),
        fix=("Publish a TXT record on the domain listing every service that sends your mail, e.g. "
             "`v=spf1 include:<your email provider> ~all` (or `v=spf1 -all` if the domain sends no email)."),
    ),
    "weak-spf": Check(
        EMAIL, 3, 1,
        title="Your list of approved email senders doesn't shut anyone out (weak SPF)",
        issue=("Your domain does publish a list of services allowed to send its email, but the list ends by "
               "approving mail from anyone else, or by saying nothing about it."),
        impact_text=("The list does nothing to flag a scammer's email sent in your name, and if it approves anyone, "
                     "it can even help fake emails pass your other email checks."),
        fix=("End the SPF record with `~all` or `-all` instead of `+all`/`?all`, after checking every real sender "
             "is listed."),
    ),
    "no-dmarc": Check(
        EMAIL, 5, 1,
        title="Anyone can send email pretending to be your domain (no DMARC)",
        issue=("There's no published rule telling Gmail, Outlook and others how to spot fake emails sent in "
               "your name."),
        impact_text=("A scammer could email your clients from something that looks like your domain, and their "
                     "inbox has no clean way to reject it — your reputation and your clients at risk."),
        fix="Publish DMARC (start `p=none`).",
    ),
    "dmarc-monitor-only": Check(
        EMAIL, 3, 2,
        title="Your email protection watches for fake emails but doesn't stop them (DMARC p=none)",
        issue=("Your domain has a rule for spotting fake emails in your name, but it is set to watch only, so "
               "inboxes may still deliver them."),
        impact_text=("Fake emails that look like yours can still reach your clients. Watching only is the right "
                     "first step, and the next is to block them once you're sure your real email passes."),
        fix=("Add a `rua=` address if there is none, read the aggregate reports, make sure SPF or DKIM passes and "
             "aligns for every real sender, then raise the policy to `p=quarantine` and later `p=reject`."),
    ),

    # --- Forms sent over HTTPS ---
    "form-over-http": Check(
        FORMS, 5, 2,
        title="A form on your homepage sends its data unprotected",
        issue=("When someone fills in a form on your homepage, what they type is sent over an unprotected "
               "connection."),
        impact_text=("Contact details and messages could be read or changed by someone on the same network, such "
                     "as public Wi-Fi. Browsers may also warn visitors before the form sends, which can "
                     "cost you enquiries."),
        fix=("Point the form's `action` at an `https://` URL (or a relative one) and serve the page itself over "
             "HTTPS."),
    ),
    "password-over-http": Check(
        FORMS, 5, 2,
        title="Your homepage asks for a password without a secure connection",
        issue=("Your homepage has a password box but doesn't use the secure connection, so passwords typed there "
               "are sent without protection."),
        impact_text=("Anyone on the same network, such as public Wi-Fi, could capture those passwords, and many "
                     "people reuse them elsewhere. Browsers also mark the page 'Not secure' when someone types a "
                     "password there."),
        fix="Serve the page and the form's `action` over HTTPS only, and redirect HTTP to HTTPS.",
    ),

    # --- Moves no rubric row ---
    "no-security-txt": Check(
        None, 1, 1,
        title="There's no standard contact for reporting security problems (no security.txt)",
        issue=("Your site doesn't publish the standard file that tells people who find a security problem how to "
               "report it to you."),
        impact_text=("Someone who spots a weakness may not know who to tell, so you could hear about it late or "
                     "not at all. It's a small, optional extra."),
        fix="Publish `/.well-known/security.txt` with at least a `Contact:` and an `Expires:` line (RFC 9116).",
    ),
}

# Strength id -> a "What's working" line.
STRENGTHS = {
    "https-valid": "Your site loads over a secure connection with a valid certificate.",
    "hsts-set": "Browsers are told to always use the secure version of your site.",
    "csp-set": "Your pages tell browsers where their code is allowed to come from.",
    "no-exposed-files": "None of the well-known private file addresses the check tried were open.",
    "email-protected": "Your domain tells inboxes to reject fake emails sent in your name, or send them to spam.",
    "security-txt": "Your site tells security researchers how to report a problem to you.",
    "cookies-flagged": "The cookies your homepage sets carry the recommended safety settings.",
    "no-version-leaks": "Your homepage doesn't advertise your software versions in the usual places.",
}
