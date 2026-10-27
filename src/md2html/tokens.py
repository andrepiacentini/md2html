"""Helpers shared by the markdown-it plugins."""

from __future__ import annotations

from markdown_it.token import Token


def plain_text(inline: Token) -> str:
    """Text of an inline token without markup: ``Use **the** `cli` `` → ``Use the cli``."""
    return "".join(
        child.content for child in inline.children or [] if child.type in ("text", "code_inline")
    )
