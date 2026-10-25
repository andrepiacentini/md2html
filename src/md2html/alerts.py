"""GitHub alerts: ``> [!NOTE]``, ``[!TIP]``, ``[!IMPORTANT]``, ``[!WARNING]``, ``[!CAUTION]``.

Mirrors GitHub's rules and HTML: only top-level blockquotes whose first line is the marker
alone (case-insensitive) and that have some content become alerts, rendered as
``<div class="markdown-alert markdown-alert-<kind>">`` with a title paragraph and icon.
"""

from __future__ import annotations

import re

from markdown_it import MarkdownIt
from markdown_it.rules_core import StateCore
from markdown_it.token import Token

# Octicons 19.42.0 (https://github.com/primer/octicons), MIT License,
# Copyright (c) 2026 GitHub Inc.
_ICONS = {
    "note": (
        "info",
        "M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8Zm8-6.5a6.5 6.5 0 1 0 0 13 6.5 6.5 0 0 0 0-13ZM6.5 "
        "7.75A.75.75 0 0 1 7.25 7h1a.75.75 0 0 1 .75.75v2.75h.25a.75.75 0 0 1 0 1.5h-2a.75.75 "
        "0 0 1 0-1.5h.25v-2h-.25a.75.75 0 0 1-.75-.75ZM8 6a1 1 0 1 1 0-2 1 1 0 0 1 0 2Z",
    ),
    "tip": (
        "light-bulb",
        "M8 1.5c-2.363 0-4 1.69-4 3.75 0 .984.424 1.625.984 2.304l.214.253c.223.264.47.556.673"
        ".848.284.411.537.896.621 1.49a.75.75 0 0 1-1.484.211c-.04-.282-.163-.547-.37-.847a8."
        "456 8.456 0 0 0-.542-.68c-.084-.1-.173-.205-.268-.32C3.201 7.75 2.5 6.766 2.5 5.25 2.5"
        " 2.31 4.863 0 8 0s5.5 2.31 5.5 5.25c0 1.516-.701 2.5-1.328 3.259-.095.115-.184.22-.268"
        ".319-.207.245-.383.453-.541.681-.208.3-.33.565-.37.847a.751.751 0 0 1-1.485-.212c.084"
        "-.593.337-1.078.621-1.489.203-.292.45-.584.673-.848.075-.088.147-.173.213-.253.561-.67"
        "9.985-1.32.985-2.304 0-2.06-1.637-3.75-4-3.75ZM5.75 12h4.5a.75.75 0 0 1 0 1.5h-4.5a.7"
        "5.75 0 0 1 0-1.5ZM6 15.25a.75.75 0 0 1 .75-.75h2.5a.75.75 0 0 1 0 1.5h-2.5a.75.75 0 0"
        " 1-.75-.75Z",
    ),
    "important": (
        "report",
        "M0 1.75C0 .784.784 0 1.75 0h12.5C15.216 0 16 .784 16 1.75v9.5A1.75 1.75 0 0 1 14.25 "
        "13H8.06l-2.573 2.573A1.458 1.458 0 0 1 3 14.543V13H1.75A1.75 1.75 0 0 1 0 11.25Zm1.75"
        "-.25a.25.25 0 0 0-.25.25v9.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72"
        "a.749.749 0 0 1 .53-.22h6.5a.25.25 0 0 0 .25-.25v-9.5a.25.25 0 0 0-.25-.25Zm7 2.25v2."
        "5a.75.75 0 0 1-1.5 0v-2.5a.75.75 0 0 1 1.5 0ZM9 9a1 1 0 1 1-2 0 1 1 0 0 1 2 0Z",
    ),
    "warning": (
        "alert",
        "M6.457 1.047c.659-1.234 2.427-1.234 3.086 0l6.082 11.378A1.75 1.75 0 0 1 14.082 15H1."
        "918a1.75 1.75 0 0 1-1.543-2.575Zm1.763.707a.25.25 0 0 0-.44 0L1.698 13.132a.25.25 0 0"
        " 0 .22.368h12.164a.25.25 0 0 0 .22-.368Zm.53 3.996v2.5a.75.75 0 0 1-1.5 0v-2.5a.75.75"
        " 0 0 1 1.5 0ZM9 11a1 1 0 1 1-2 0 1 1 0 0 1 2 0Z",
    ),
    "caution": (
        "stop",
        "M4.47.22A.749.749 0 0 1 5 0h6c.199 0 .389.079.53.22l4.25 4.25c.141.14.22.331.22.53v6a"
        ".749.749 0 0 1-.22.53l-4.25 4.25A.749.749 0 0 1 11 16H5a.749.749 0 0 1-.53-.22L.22 11"
        ".53A.749.749 0 0 1 0 11V5c0-.199.079-.389.22-.53Zm.84 1.28L1.5 5.31v5.38l3.81 3.81h5."
        "38l3.81-3.81V5.31L10.69 1.5ZM8 4a.75.75 0 0 1 .75.75v3.5a.75.75 0 0 1-1.5 0v-3.5A.75."
        "75 0 0 1 8 4Zm0 8a1 1 0 1 1 0-2 1 1 0 0 1 0 2Z",
    ),
}

_MARKER = re.compile(r"\A\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\][ \t]*(?:\n|\Z)", re.IGNORECASE)


def alerts_plugin(md: MarkdownIt) -> None:
    """Register the alert rule; it runs before inline parsing so the marker is never rendered."""
    md.core.ruler.before("inline", "github_alerts", _github_alerts)


def _github_alerts(state: StateCore) -> None:
    tokens = state.tokens
    index = 0
    while index < len(tokens):
        if _is_alert_candidate(tokens, index):
            _convert(tokens, index)
        index += 1


def _is_alert_candidate(tokens: list[Token], index: int) -> bool:
    return (
        tokens[index].type == "blockquote_open"
        and tokens[index].level == 0
        and index + 2 < len(tokens)
        and tokens[index + 1].type == "paragraph_open"
        and tokens[index + 2].type == "inline"
        and _MARKER.match(tokens[index + 2].content) is not None
    )


def _convert(tokens: list[Token], open_index: int) -> None:
    inline = tokens[open_index + 2]
    match = _MARKER.match(inline.content)
    assert match is not None  # checked by _is_alert_candidate
    rest = inline.content[match.end() :]
    close_index = next(
        i
        for i in range(open_index + 1, len(tokens))
        if tokens[i].type == "blockquote_close" and tokens[i].level == 0
    )
    first_paragraph_close = open_index + 3
    has_more_blocks = close_index > first_paragraph_close + 1
    if not rest.strip() and not has_more_blocks:
        return  # GitHub keeps an alert without content as a plain blockquote

    kind = match.group(1).lower()
    tokens[open_index].tag = "div"
    tokens[open_index].attrSet("class", f"markdown-alert markdown-alert-{kind}")
    tokens[close_index].tag = "div"

    if rest.strip():
        inline.content = rest
    else:
        del tokens[open_index + 1 : first_paragraph_close + 1]
    tokens.insert(open_index + 1, _title_token(kind))


def _title_token(kind: str) -> Token:
    icon, path = _ICONS[kind]
    token = Token("html_block", "", 0)
    token.content = (
        f'<p class="markdown-alert-title"><svg class="octicon octicon-{icon}" '
        f'viewBox="0 0 16 16" width="16" height="16" aria-hidden="true">'
        f'<path d="{path}"></path></svg>{kind.capitalize()}</p>\n'
    )
    return token
