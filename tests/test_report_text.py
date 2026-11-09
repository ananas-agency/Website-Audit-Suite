import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from helpers import REPO, load_script  # noqa: E402,F401

sys.path.insert(0, str(REPO / "scripts"))
from report.data import Finding, load_run  # noqa: E402
from report.rules import apply_rules  # noqa: E402
from report.text import HINTS, apply_hints, id_link, md_plain, md_to_html, tag  # noqa: E402


def f_with_title(title, fid="MSG-01"):
    return Finding(key="k", title=title, issue="i", impact_text="t", fix="f",
                   impact=3, effort=1, id=fid)


FIXTURE = REPO / "tests" / "fixtures" / "sample-run"


class ReportTextTests(unittest.TestCase):
    def setUp(self):
        self.run = load_run(FIXTURE)
        self.keymap = apply_rules(self.run)

    def test_html_in_prose_is_escaped(self):
        self.assertIn("&lt;title&gt;", md_to_html('The <title> tag reads "Home"', {}))

    def test_tooltip_escapes_quotes(self):
        self.assertIn('title="MSG-01 — Hero says &quot;Welcome&quot;"',
                      id_link(f_with_title('Hero says "Welcome"')))

    def test_id_link_page_from_prefix(self):
        self.assertTrue(id_link(f_with_title("T", "UX-02")).startswith('<a href="ux-technical.html"'))
        self.assertTrue(id_link(f_with_title("T", "CRO-01")).startswith('<a href="conversion.html"'))

    def test_inline_markdown(self):
        self.assertEqual(md_to_html("**a** *b* `c`", {}), "<b>a</b> <i>b</i> <code>c</code>")

    def test_code_is_not_further_converted(self):
        self.assertEqual(md_to_html("`*x*`", {}), "<code>*x*</code>")

    def test_blank_line(self):
        self.assertEqual(md_to_html("a\n\nb", {}), "a<br><br>b")

    def test_links_only_safe_schemes(self):
        out = md_to_html("[x](https://x.com)", {})
        self.assertIn('href="https://x.com"', out)
        self.assertIn('target="_blank" rel="noopener"', out)
        self.assertIn('href="mailto:a@b.co"', md_to_html("[m](mailto:a@b.co)", {}))
        self.assertNotIn("href", md_to_html("[x](javascript:alert(1))", {}))
        self.assertNotIn("href", md_to_html("[x](ftp://x.com)", {}))

    def test_link_url_with_parentheses(self):
        out = md_to_html("See [x](https://en.wikipedia.org/wiki/A_(b)) now", {})
        self.assertIn('href="https://en.wikipedia.org/wiki/A_(b)"', out)
        self.assertTrue(out.endswith(" now"))

    def test_nul_and_crlf_in_prose(self):
        self.assertEqual(md_to_html("a\x00b `c` \x000\x00", {}), "ab <code>c</code> 0")
        self.assertEqual(md_to_html("a\r\n\r\nb", {}), "a<br><br>b")

    def test_id_link_unknown_prefix_raises(self):
        with self.assertRaisesRegex(ValueError, "XYZ-01"):
            id_link(f_with_title("T", "XYZ-01"))

    def test_key_reference_becomes_id_link(self):
        self.assertIn(">MSG-01</a>", md_to_html("See [[hero]].", self.keymap))
        self.assertEqual(md_plain("See [[hero]].", self.keymap), "See MSG-01.")

    def test_unknown_key_stays_plain(self):
        self.assertEqual(md_to_html("[[nope]]", {}), "[[nope]]")

    def test_plural_acronym_gets_hint(self):
        out = apply_hints("<p>Fix the CTAs and SEOs</p>")
        self.assertRegex(out, r'<abbr title="[^"]*">CTA</abbr>s')
        self.assertRegex(out, r'<abbr title="[^"]*">SEO</abbr>s')

    def test_hints_skip_ids_attributes_and_links(self):
        out = apply_hints('<p>Fix the CTA and CRO-03 <a title="SEO">SEO</a> quick wins</p>')
        self.assertIn('<abbr title="Call to action', out)
        self.assertIn("CRO-03", out)
        self.assertNotIn('<abbr title="Conversion', out)
        self.assertIn('<a title="SEO">SEO</a>', out)
        self.assertIn(">quick win</abbr>s", out)

    def test_hints_skip_code_abbr_title(self):
        out = apply_hints("<title>SEO</title><code>CTA</code><abbr>UX</abbr><p>UX Big Bet</p>")
        self.assertEqual(out.count("<abbr"), 3)  # the existing one + UX + Big Bet
        self.assertIn(">Big Bet</abbr>", out)

    def test_acronyms_are_case_sensitive_whole_words(self):
        self.assertNotIn("<abbr", apply_hints("<p>seo SEOX uxui</p>"))

    def test_tag(self):
        self.assertEqual(tag("quickwin"),
                         '<span class="tag quickwin" title="%s">quick win</span>' % HINTS["quick win"])
        self.assertIn(">fill-in</span>", tag("fillin"))
        self.assertIn(">big bet</span>", tag("bigbet"))
        self.assertIn(">skip</span>", tag("skip"))
        self.assertIn("backlog", tag("skip"))

    def test_hints_leave_tag_span_unchanged(self):
        for q in ("quickwin", "bigbet", "fillin", "skip"):
            self.assertEqual(apply_hints(tag(q)), tag(q))
        out = apply_hints("<p>a quick win here</p>" + tag("quickwin") + "<p>big bet</p>")
        self.assertEqual(out.count("<abbr"), 2)
        self.assertIn(tag("quickwin"), out)

    def test_flex_headings_keep_hinted_label_in_one_item(self):
        h4 = apply_hints('<h4><span class="dot"></span>Quick Wins — do first</h4>')
        self.assertEqual(h4.count("<span>"), 1)
        self.assertRegex(h4, r'</span><span><abbr title="[^"]*">Quick Win</abbr>s — do first</span></h4>')
        h2 = apply_hints('<h2 class="section"><span class="no">4</span> Conversion (CRO) — '
                         '<span class="grade d">D</span> 67/100<a class="openbtn" href="x">Open</a></h2>')
        self.assertRegex(h2, r'</span> <span>Conversion \(<abbr title="[^"]*">CRO</abbr>\) — </span><span class="grade d">')
        plain = '<h2 class="section"><span class="no">1</span> Site Snapshot</h2>'
        self.assertEqual(apply_hints(plain), plain)

    def test_rerating_renumbers_and_references_follow(self):
        keymap = self.keymap
        self.assertIn(">MSG-01</a>", md_to_html("[[hero]]", keymap))
        keymap["hero"].impact = 1
        keymap = apply_rules(self.run)
        self.assertNotEqual(keymap["hero"].id, "MSG-01")
        self.assertIn(f'>{keymap["hero"].id}</a>', md_to_html("[[hero]]", keymap))


if __name__ == "__main__":
    unittest.main()
