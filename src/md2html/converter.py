"""Markdown to HTML conversion.

The parser follows GitHub Flavored Markdown as closely as markdown-it-py allows:
tables, strikethrough, autolinks, task lists, footnotes and heading anchors.
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

from markdown_it import MarkdownIt
from markdown_it.token import Token
from mdit_py_plugins.anchors import anchors_plugin
from mdit_py_plugins.footnote import footnote_plugin
from mdit_py_plugins.front_matter import front_matter_plugin
from mdit_py_plugins.tasklists import tasklists_plugin

from md2html.highlight import highlight_code
from md2html.links import LinkResolver
from md2html.page import build_page

Theme = Literal["auto", "light", "dark"]


@dataclass(frozen=True)
class RenderOptions:
    """How a Markdown document is turned into an HTML page.

    Args:
        source_dir: Directory the Markdown's relative URLs are relative to.
        output_dir: Directory of the generated HTML; ``None`` means absolute
            ``file://`` URIs (see :class:`md2html.links.LinkResolver`).
        embed_images: Inline local images as ``data:`` URIs.
        theme: Color scheme of the page.
        title: Page title; defaults to the first level-1 heading.
    """

    source_dir: Path = field(default_factory=Path.cwd)
    output_dir: Path | None = None
    embed_images: bool = False
    theme: Theme = "auto"
    title: str | None = None


@dataclass(frozen=True)
class RenderedBody:
    html: str
    title: str | None


def create_parser() -> MarkdownIt:
    """Build the markdown-it parser with the GFM-like feature set."""
    md = MarkdownIt("gfm-like", {"html": True, "highlight": highlight_code})
    md.use(front_matter_plugin)
    md.use(footnote_plugin)
    md.use(tasklists_plugin)
    md.use(anchors_plugin, max_level=6)
    return md


def render_body(markdown: str, resolver: LinkResolver) -> RenderedBody:
    """Render ``markdown`` to an HTML fragment, rewriting its relative URLs."""
    md = create_parser()
    env: dict[str, object] = {}
    tokens = md.parse(markdown, env)
    _rewrite_urls(tokens, resolver)
    html = md.renderer.render(tokens, md.options, env)
    return RenderedBody(html=html, title=_first_h1(tokens))


def render_document(
    markdown: str, options: RenderOptions | None = None, *, fallback_title: str = "Document"
) -> str:
    """Render ``markdown`` as a complete, self-contained HTML page."""
    options = options or RenderOptions()
    resolver = LinkResolver(
        source_dir=options.source_dir,
        output_dir=options.output_dir,
        embed_images=options.embed_images,
    )
    body = render_body(markdown, resolver)
    title = options.title or body.title or fallback_title
    return build_page(body=body.html, title=title, theme=options.theme)


def _walk(tokens: list[Token]) -> Iterator[Token]:
    for token in tokens:
        yield token
        if token.children:
            yield from _walk(token.children)


def _rewrite_urls(tokens: list[Token], resolver: LinkResolver) -> None:
    for token in _walk(tokens):
        if token.type == "image":
            src = token.attrGet("src")
            if isinstance(src, str):
                token.attrSet("src", resolver.resolve_image(src))
        elif token.type == "link_open":
            href = token.attrGet("href")
            if isinstance(href, str):
                token.attrSet("href", resolver.resolve(href))
        elif token.type in ("html_block", "html_inline"):
            token.content = resolver.rewrite_html(token.content)


def _first_h1(tokens: list[Token]) -> str | None:
    for index, token in enumerate(tokens):
        if token.type == "heading_open" and token.tag == "h1":
            inline = tokens[index + 1]
            text = "".join(
                child.content
                for child in inline.children or []
                if child.type in ("text", "code_inline")
            )
            return text.strip() or None
    return None
