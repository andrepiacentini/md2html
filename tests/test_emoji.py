"""Emoji shortcodes (``:tada:`` → 🎉), following GitHub's rules.

The expected outputs were checked against GitHub's Markdown API (``gh api markdown``).
"""

from pathlib import Path

import pytest

from md2html.converter import render_body, render_document
from md2html.links import LinkResolver


def body(markdown: str) -> str:
    return render_body(markdown, LinkResolver(source_dir=Path.cwd())).html


@pytest.mark.parametrize(
    ("markdown", "expected"),
    [
        pytest.param(":tada:", "<p>🎉</p>", id="alone"),
        pytest.param(":+1: :thumbsup:", "<p>👍 👍</p>", id="aliases"),
        pytest.param("(:tada:) :tada:.", "<p>(🎉) 🎉.</p>", id="punctuation"),
        pytest.param(":tada:b", "<p>🎉b</p>", id="letter after"),
        pytest.param(":smile::smile:", "<p>😄😄</p>", id="adjacent"),
        pytest.param(":smile::", "<p>😄:</p>", id="extra colon after"),
        pytest.param("*:tada:*", "<p><em>🎉</em></p>", id="emphasis"),
        pytest.param(
            "[:rocket:](https://x.y)", '<p><a href="https://x.y">🚀</a></p>', id="link text"
        ),
        pytest.param("<b>:fire:</b>", "<p><b>🔥</b></p>", id="raw inline html"),
    ],
)
def test_converts_shortcodes(markdown: str, expected: str) -> None:
    assert body(markdown).strip() == expected


@pytest.mark.parametrize(
    "markdown",
    [
        pytest.param(":TADA:", id="case-sensitive"),
        pytest.param(":not_an_emoji:", id="unknown name"),
        pytest.param(":octocat:", id="custom GitHub image emoji"),
        pytest.param("a:tada:b", id="letter before"),
        pytest.param("a:tada:", id="letter before, end of text"),
        pytest.param("::smile:", id="colon before"),
        pytest.param("12:30:45", id="clock time"),
    ],
)
def test_leaves_other_text_alone(markdown: str) -> None:
    assert body(markdown).strip() == f"<p>{markdown}</p>"


def test_code_is_not_converted() -> None:
    html = body("`:tada:`\n\n```\n:tada:\n```\n")

    assert "🎉" not in html
    assert "<code>:tada:</code>" in html


def test_image_alt_text_is_not_converted() -> None:
    assert 'alt=":x:"' in body("![:x:](i.png)")


def test_headings_and_tables_are_converted() -> None:
    html = body("## :rocket: Launch\n\n| :fire: |\n| --- |\n| :x: |\n")

    assert "🚀 Launch</h2>" in html
    assert "<th>🔥</th>" in html
    assert "<td>❌</td>" in html


def test_heading_anchor_comes_from_the_emoji_not_its_name() -> None:
    assert '<h2 id="-launch">' in body("## :rocket: Launch\n")


def test_page_title_shows_the_emoji() -> None:
    assert "<title>🚀 Launch</title>" in render_document("# :rocket: Launch\n")
