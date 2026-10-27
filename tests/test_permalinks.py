"""Heading permalinks: the link icon GitHub shows next to headings on hover."""

from pathlib import Path

import pytest

from md2html.converter import render_body, render_document
from md2html.links import LinkResolver


def body(markdown: str, *, toc: bool = False) -> str:
    return render_body(markdown, LinkResolver(source_dir=Path.cwd()), toc=toc).html


def flat(html: str) -> str:
    return html.replace("\n", "")


def test_heading_is_wrapped_with_a_permalink() -> None:
    html = flat(body("## Install\n"))

    assert html.startswith('<div class="markdown-heading"><h2 id="install">Install</h2>')
    assert '<a class="anchor" aria-label="Permalink: Install" href="#install">' in html
    assert '<svg class="octicon octicon-link"' in html
    assert html.endswith("</svg></a></div>")


@pytest.mark.parametrize("level", range(1, 7))
def test_every_heading_level_gets_a_permalink(level: int) -> None:
    assert 'href="#title"' in body(f"{'#' * level} Title\n")


def test_duplicate_headings_link_to_their_unique_ids() -> None:
    html = body("## Same\n\n## Same\n")

    assert 'href="#same"' in html
    assert 'href="#same-1"' in html


def test_label_uses_escaped_plain_text() -> None:
    html = body('## 1 < 2 & "q" `code`\n')

    assert 'aria-label="Permalink: 1 &lt; 2 &amp; &quot;q&quot; code"' in html


def test_label_shows_emoji() -> None:
    assert 'aria-label="Permalink: 🚀 Launch" href="#-launch"' in body("## :rocket: Launch\n")


def test_table_of_contents_still_follows_the_title() -> None:
    html = flat(body("# Title\n\nIntro.\n\n## Section\n", toc=True))

    title_wrapper_end = html.index("</a></div>")
    assert title_wrapper_end < html.index('<nav class="toc"') < html.index("<p>Intro.</p>")


def test_page_shows_permalinks_on_hover() -> None:
    page = render_document("## Section\n")

    assert ".markdown-heading:hover .anchor" in page
