from pathlib import Path

from md2html.converter import RenderOptions, render_body, render_document
from md2html.links import LinkResolver


def body(markdown: str, source_dir: Path | None = None) -> str:
    return render_body(markdown, LinkResolver(source_dir=source_dir or Path.cwd())).html


def test_renders_gfm_tables() -> None:
    html = body("| a | b |\n|---|:-:|\n| 1 | 2 |\n")

    assert "<table>" in html
    assert '<th style="text-align:center">b</th>' in html


def test_renders_strikethrough_and_autolinks() -> None:
    html = body("~~old~~ see https://example.com")

    assert "<s>old</s>" in html
    assert '<a href="https://example.com">https://example.com</a>' in html


def test_renders_task_lists() -> None:
    html = body("- [x] done\n- [ ] todo\n")

    assert 'class="task-list-item-checkbox"' in html
    assert 'checked="checked"' in html


def test_renders_footnotes() -> None:
    html = body("Text[^1].\n\n[^1]: The note.\n")

    assert 'class="footnotes"' in html


def test_headings_get_anchor_ids() -> None:
    assert '<h2 id="getting-started">Getting started</h2>' in body("## Getting started")


def test_highlights_known_languages() -> None:
    html = body("```python\nprint('hi')\n```\n")

    assert 'class="language-python"' in html
    assert '<span class="nb">print</span>' in html


def test_escapes_unknown_languages() -> None:
    html = body("```nonexistent-lang\n<b>x</b>\n```\n")

    assert "&lt;b&gt;x&lt;/b&gt;" in html


def test_front_matter_is_not_rendered() -> None:
    html = body("---\ntitle: Hidden\n---\n\n# Visible\n")

    assert "Hidden" not in html


def test_keeps_raw_html() -> None:
    assert '<p align="center">' in body('<p align="center">\n  <b>hi</b>\n</p>\n')


def test_rewrites_markdown_and_html_image_urls(tmp_path: Path) -> None:
    html = body('![logo](img/logo.png)\n\n<img src="img/raw.png">\n', source_dir=tmp_path)

    assert f'src="{(tmp_path / "img" / "logo.png").as_uri()}"' in html
    assert f'src="{(tmp_path / "img" / "raw.png").as_uri()}"' in html


def test_title_comes_from_first_h1() -> None:
    result = render_body("intro\n\n# The `md2html` guide\n\n# Second\n", LinkResolver(Path.cwd()))

    assert result.title == "The md2html guide"


def test_document_is_a_complete_self_contained_page() -> None:
    page = render_document("# Hello", RenderOptions(theme="dark"))

    assert page.startswith("<!doctype html>")
    assert '<html lang="en" data-theme="dark">' in page
    assert "<title>Hello</title>" in page
    assert "<style>" in page
    assert "<link" not in page
    assert "<script" not in page


def test_document_title_option_wins_and_is_escaped() -> None:
    page = render_document("# Hello", RenderOptions(title="A <b> title"))

    assert "<title>A &lt;b&gt; title</title>" in page


def test_document_uses_fallback_title_without_h1() -> None:
    assert "<title>notes</title>" in render_document("text", fallback_title="notes")
