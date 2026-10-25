"""GitHub alerts (``> [!NOTE]``…), matching the HTML GitHub produces."""

from pathlib import Path

import pytest

from md2html.converter import render_body, render_document
from md2html.links import LinkResolver


def body(markdown: str) -> str:
    return render_body(markdown, LinkResolver(source_dir=Path.cwd())).html


@pytest.mark.parametrize(
    ("marker", "kind", "title"),
    [
        ("NOTE", "note", "Note"),
        ("TIP", "tip", "Tip"),
        ("IMPORTANT", "important", "Important"),
        ("WARNING", "warning", "Warning"),
        ("CAUTION", "caution", "Caution"),
    ],
)
def test_renders_each_alert_type(marker: str, kind: str, title: str) -> None:
    html = body(f"> [!{marker}]\n> Body text.\n")

    assert f'<div class="markdown-alert markdown-alert-{kind}">' in html
    assert '<p class="markdown-alert-title"><svg class="octicon' in html
    assert f"</svg>{title}</p>" in html
    assert "<p>Body text.</p>" in html
    assert "<blockquote>" not in html
    assert f"[!{marker}]" not in html


def test_marker_is_case_insensitive() -> None:
    assert 'class="markdown-alert markdown-alert-tip"' in body("> [!tip]\n> Hint.\n")


def test_trailing_spaces_after_marker_are_allowed() -> None:
    assert "markdown-alert-caution" in body("> [!CAUTION]   \n> Careful.\n")


def test_content_keeps_markdown_formatting() -> None:
    html = body("> [!NOTE]\n> Use **bold** and `code`.\n>\n> - a list\n")

    assert "<p>Use <strong>bold</strong> and <code>code</code>.</p>" in html
    assert "<li>a list</li>" in html


def test_marker_on_its_own_paragraph_leaves_no_empty_paragraph() -> None:
    html = body("> [!WARNING]\n>\n> Second paragraph.\n")

    assert "markdown-alert-warning" in html
    assert "<p></p>" not in html
    assert "<p>Second paragraph.</p>" in html


@pytest.mark.parametrize(
    "markdown",
    [
        pytest.param("> Just a quote.\n", id="plain quote"),
        pytest.param("> [!TIP] same line\n", id="text on the marker line"),
        pytest.param("> [!DANGER]\n> Unknown type.\n", id="unknown type"),
        pytest.param("> [!NOTE]\n", id="no content"),
        pytest.param("> > [!NOTE]\n> > nested\n", id="nested quote"),
        pytest.param("- item\n\n  > [!TIP]\n  > in list\n", id="inside a list"),
    ],
)
def test_other_blockquotes_stay_blockquotes(markdown: str) -> None:
    html = body(markdown)

    assert "<blockquote>" in html
    assert "markdown-alert" not in html


def test_page_styles_every_alert_type() -> None:
    page = render_document("> [!NOTE]\n> x\n")

    for kind in ("note", "tip", "important", "warning", "caution"):
        assert f".markdown-alert-{kind}" in page
