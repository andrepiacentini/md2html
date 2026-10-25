from pathlib import Path

from md2html.output import write_html, write_temp_html


def test_write_html_creates_parent_directories(tmp_path: Path) -> None:
    path = write_html("<p>x</p>", tmp_path / "a" / "b" / "page.html")

    assert path.read_text(encoding="utf-8") == "<p>x</p>"
    assert path.is_absolute()


def test_write_temp_html_sanitizes_the_stem() -> None:
    path = write_temp_html("<p>ç</p>", "my notes/../x")
    try:
        assert path.name.startswith("md2html-my-notes-..-x-")
        assert path.suffix == ".html"
        assert path.read_text(encoding="utf-8") == "<p>ç</p>"
    finally:
        path.unlink()
