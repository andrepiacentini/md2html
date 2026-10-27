"""Table of contents built from the document's headings (``--toc``).

Lists headings down to level 3, nested by level, linking to the ids set by the anchors
plugin. A leading level-1 heading is the document title: it is left out of the list and
the table of contents is placed right after it; otherwise it goes at the top.
"""

from __future__ import annotations

from dataclasses import dataclass
from html import escape

from markdown_it import MarkdownIt
from markdown_it.rules_core import StateCore
from markdown_it.token import Token

from md2html.tokens import plain_text

MAX_LEVEL = 3


@dataclass(frozen=True)
class _Entry:
    level: int
    anchor: str
    text: str


def toc_plugin(md: MarkdownIt) -> None:
    """Register the table of contents rule; it must run after the anchors plugin."""
    md.core.ruler.push("toc", _table_of_contents)


def _table_of_contents(state: StateCore) -> None:
    tokens = state.tokens
    title_end = _leading_title_end(tokens)
    entries = _entries(tokens, skip_until=title_end)
    if not entries:
        return
    nav = Token("html_block", "", 0)
    nav.content = _render(entries)
    tokens.insert(title_end, nav)


def _leading_title_end(tokens: list[Token]) -> int:
    """Index right after a leading ``<h1>`` (ignoring front matter), or of the first block."""
    start = next((i for i, t in enumerate(tokens) if t.type != "front_matter"), len(tokens))
    if start < len(tokens) and tokens[start].type == "heading_open" and tokens[start].tag == "h1":
        return start + 3  # heading_open, inline, heading_close
    return start


def _entries(tokens: list[Token], *, skip_until: int) -> list[_Entry]:
    entries = []
    for index in range(skip_until, len(tokens)):
        token = tokens[index]
        if token.type != "heading_open" or token.level != 0:
            continue
        level = int(token.tag[1:])
        anchor = token.attrGet("id")
        if level <= MAX_LEVEL and isinstance(anchor, str):
            entries.append(_Entry(level, anchor, plain_text(tokens[index + 1])))
    return entries


def _render(entries: list[_Entry]) -> str:
    lines = [
        '<nav class="toc" aria-label="Table of contents">',
        '<p class="toc-title">Contents</p>',
        "<ul>",
    ]
    open_levels = [entries[0].level]
    for position, entry in enumerate(entries):
        if position > 0:
            if entry.level > open_levels[-1]:
                lines.append("<ul>")
                open_levels.append(entry.level)
            else:
                lines.append("</li>")
                while len(open_levels) > 1 and entry.level < open_levels[-1]:
                    lines += ["</ul>", "</li>"]
                    open_levels.pop()
        lines.append(f'<li><a href="#{escape(entry.anchor)}">{escape(entry.text)}</a>')
    lines.append("</li>")
    lines += ["</ul>", "</li>"] * (len(open_levels) - 1)
    lines += ["</ul>", "</nav>"]
    return "\n".join(lines) + "\n"
