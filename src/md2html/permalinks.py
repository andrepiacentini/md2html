"""Heading permalinks: the link icon GitHub shows next to a heading on hover.

Produces GitHub's markup (``<div class="markdown-heading">`` holding the heading and an
``<a class="anchor">``), except that the id stays on the heading itself: GitHub moves it to
the anchor with a ``user-content-`` prefix and resolves ``#links`` with JavaScript, which
this page does not have.
"""

from __future__ import annotations

from html import escape

from markdown_it import MarkdownIt
from markdown_it.rules_core import StateCore
from markdown_it.token import Token

from md2html.tokens import plain_text

# Octicons 19.42.0 "link" (https://github.com/primer/octicons), MIT License,
# Copyright (c) 2026 GitHub Inc.
_LINK_ICON = (
    '<svg class="octicon octicon-link" viewBox="0 0 16 16" width="16" height="16" '
    'aria-hidden="true"><path d="m7.775 3.275 1.25-1.25a3.5 3.5 0 1 1 4.95 4.95l-2.5 2.5a3'
    ".5 3.5 0 0 1-4.95 0 .751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018 1.998 1.998 0 0"
    " 0 2.83 0l2.5-2.5a2.002 2.002 0 0 0-2.83-2.83l-1.25 1.25a.751.751 0 0 1-1.042-.018.751"
    ".751 0 0 1-.018-1.042Zm-4.69 9.64a1.998 1.998 0 0 0 2.83 0l1.25-1.25a.751.751 0 0 1 1."
    "042.018.751.751 0 0 1 .018 1.042l-1.25 1.25a3.5 3.5 0 1 1-4.95-4.95l2.5-2.5a3.5 3.5 0 "
    "0 1 4.95 0 .751.751 0 0 1-.018 1.042.751.751 0 0 1-1.042.018 1.998 1.998 0 0 0-2.83 0l"
    '-2.5 2.5a1.998 1.998 0 0 0 0 2.83Z"></path></svg>'
)


def permalinks_plugin(md: MarkdownIt) -> None:
    """Register the permalink rule; it must run after the anchors plugin sets heading ids."""
    md.core.ruler.push("permalinks", _permalinks)


def _permalinks(state: StateCore) -> None:
    tokens = state.tokens
    index = 0
    while index < len(tokens):
        token = tokens[index]
        anchor = token.attrGet("id") if token.type == "heading_open" else None
        if isinstance(anchor, str):
            label = escape(f"Permalink: {plain_text(tokens[index + 1])}")
            tokens.insert(index, _html('<div class="markdown-heading">', token.level))
            # heading_open, inline and heading_close now sit at index + 1 .. index + 3
            tokens.insert(
                index + 4,
                _html(
                    f'<a class="anchor" aria-label="{label}" href="#{escape(anchor)}">'
                    f"{_LINK_ICON}</a></div>\n",
                    token.level,
                ),
            )
            index += 4
        index += 1


def _html(content: str, level: int) -> Token:
    token = Token("html_block", "", 0)
    token.content = content
    token.level = level
    return token
