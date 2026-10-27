"""Optional table of contents (``--toc``)."""

from pathlib import Path

from md2html.converter import RenderOptions, render_body, render_document
from md2html.links import LinkResolver

DOC = """\
# Project

Intro.

## Install

### With uv

#### Deep detail

## Usage
"""


def body(markdown: str, *, toc: bool = True) -> str:
    return render_body(markdown, LinkResolver(source_dir=Path.cwd()), toc=toc).html


def flat(html: str) -> str:
    return html.replace("\n", "")


def nav(html: str) -> str:
    """Only the table of contents, so heading permalinks do not count as entries."""
    return html[html.index('<nav class="toc"') : html.index("</nav>")]


def test_no_table_of_contents_by_default() -> None:
    assert "toc" not in body(DOC, toc=False)


def test_lists_level_2_and_3_headings_nested() -> None:
    assert flat(
        '<nav class="toc" aria-label="Table of contents">'
        '<p class="toc-title">Contents</p>'
        "<ul>"
        '<li><a href="#install">Install</a>'
        '<ul><li><a href="#with-uv">With uv</a></li></ul>'
        "</li>"
        '<li><a href="#usage">Usage</a></li>'
        "</ul>"
        "</nav>"
    ) in flat(body(DOC))


def test_deeper_headings_are_left_out() -> None:
    toc = nav(body(DOC))

    assert 'href="#with-uv"' in toc
    assert 'href="#deep-detail"' not in toc


def test_goes_right_after_the_leading_title() -> None:
    html = body(DOC)

    assert html.index("</h1>") < html.index('<nav class="toc"') < html.index("<p>Intro.</p>")
    assert 'href="#project"' not in nav(html)


def test_goes_at_the_top_without_a_leading_title() -> None:
    assert body("Intro.\n\n## Section\n").startswith('<nav class="toc"')


def test_title_detection_skips_front_matter() -> None:
    html = body("---\nx: 1\n---\n# Title\n\n## Section\n")

    assert html.index("</h1>") < html.index('<nav class="toc"')


def test_later_level_1_headings_are_listed() -> None:
    assert 'href="#part-two"' in body("# Title\n\n## A\n\n# Part two\n")


def test_no_table_of_contents_without_headings() -> None:
    assert "toc" not in body("# Only a title\n\nText.\n")


def test_heading_text_is_escaped() -> None:
    assert ">1 &lt; 2 &amp; 3</a>" in body("## 1 < 2 & 3\n")


def test_level_jumps_keep_every_entry() -> None:
    html = body("### Starts deep\n\n## Back up\n\n### Child\n")

    for anchor in ("#starts-deep", "#back-up", "#child"):
        assert f'href="{anchor}"' in html
    assert flat(html).count("<ul>") == flat(html).count("</ul>")


def test_document_option_and_styles() -> None:
    page = render_document(DOC, RenderOptions(toc=True))

    assert '<nav class="toc"' in page
    assert ".toc {" in page
