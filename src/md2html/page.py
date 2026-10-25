"""Assembly of the final HTML page from the packaged template and stylesheet."""

from __future__ import annotations

from functools import cache
from html import escape
from importlib.resources import files
from string import Template

from md2html.highlight import pygments_css


@cache
def _template() -> Template:
    return Template(files("md2html").joinpath("assets/page.html").read_text(encoding="utf-8"))


@cache
def _css() -> str:
    base = files("md2html").joinpath("assets/style.css").read_text(encoding="utf-8")
    return f"{base}\n{pygments_css()}"


def build_page(*, body: str, title: str, theme: str) -> str:
    """Wrap an HTML fragment in a complete page with inline CSS (no network access)."""
    return _template().substitute(
        title=escape(title),
        theme=escape(theme),
        css=_css(),
        body=body,
    )
