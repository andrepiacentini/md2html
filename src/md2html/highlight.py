"""Syntax highlighting of fenced code blocks with Pygments."""

from __future__ import annotations

from html import escape

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound

LIGHT_STYLE = "default"
DARK_STYLE = "github-dark"

_formatter = HtmlFormatter(nowrap=True)


def highlight_code(code: str, lang: str, _attrs: str = "") -> str:
    """Highlight ``code`` for markdown-it; unknown languages are only escaped."""
    if not lang:
        return escape(code)
    try:
        lexer = get_lexer_by_name(lang, stripall=False)
    except ClassNotFound:
        return escape(code)
    return highlight(code, lexer, _formatter)


def pygments_css() -> str:
    """CSS for highlighted code, following the page theme (light, dark or auto)."""
    light = _style_defs(LIGHT_STYLE, "pre code")
    dark_explicit = _style_defs(DARK_STYLE, ':root[data-theme="dark"] pre code')
    dark_auto = _style_defs(DARK_STYLE, ':root[data-theme="auto"] pre code')
    return f"{light}\n{dark_explicit}\n@media (prefers-color-scheme: dark) {{\n{dark_auto}\n}}\n"


def _style_defs(style: str, selector: str) -> str:
    formatter: HtmlFormatter[str] = HtmlFormatter(style=style)
    return str(formatter.get_style_defs(selector))  # type: ignore[no-untyped-call]
