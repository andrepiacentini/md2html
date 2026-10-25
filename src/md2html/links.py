"""Resolution of relative URLs found in a Markdown document.

A Markdown file refers to images and other files relative to its own location. The
generated HTML usually lives elsewhere (a temporary directory, or a path chosen with
``--output``), so those references must be rewritten to keep working.
"""

from __future__ import annotations

import base64
import mimetypes
import os
import re
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit

# src="..." / href="..." inside raw HTML written in the Markdown source.
_HTML_URL_ATTR = re.compile(r"""(\b(?:src|href)\s*=\s*)(["'])(.*?)\2""", re.IGNORECASE)


@dataclass(frozen=True)
class LinkResolver:
    """Rewrites relative URLs so they resolve from the generated HTML file.

    Args:
        source_dir: Directory of the Markdown file; relative URLs are relative to it.
        output_dir: Directory where the HTML will be written. When ``None``, URLs are
            rewritten as absolute ``file://`` URIs (used for temporary previews).
        embed_images: Inline local images as ``data:`` URIs, making the page portable.
    """

    source_dir: Path
    output_dir: Path | None = None
    embed_images: bool = False

    def resolve(self, url: str) -> str:
        """Return ``url`` rewritten to work from the output location."""
        target = self._local_target(url)
        if target is None:
            return url
        path, suffix = target
        if self.output_dir is None or not _share_parent(path, self.output_dir):
            return path.as_uri() + suffix
        relative = os.path.relpath(path, self.output_dir)
        return quote(Path(relative).as_posix()) + suffix

    def resolve_image(self, url: str) -> str:
        """Like :meth:`resolve`, but inlines the file when ``embed_images`` is set."""
        if self.embed_images:
            target = self._local_target(url)
            if target is not None and target[0].is_file():
                return _data_uri(target[0])
        return self.resolve(url)

    def rewrite_html(self, html: str) -> str:
        """Rewrite ``src``/``href`` attributes found in a raw HTML fragment."""

        def replace(match: re.Match[str]) -> str:
            prefix, quote_char, url = match.groups()
            is_src = prefix.lower().lstrip().startswith("src")
            new_url = self.resolve_image(url) if is_src else self.resolve(url)
            return f"{prefix}{quote_char}{new_url}{quote_char}"

        return _HTML_URL_ATTR.sub(replace, html)

    def _local_target(self, url: str) -> tuple[Path, str] | None:
        """Split a relative URL into an absolute path and its ``?query#fragment``.

        Returns ``None`` for URLs that must be left untouched: anything with a scheme
        (``https:``, ``mailto:``, ``data:``), protocol-relative and root-relative URLs,
        and pure fragments (``#section``).
        """
        url = url.strip()
        if not url or url.startswith(("#", "/", "\\")):
            return None
        parts = urlsplit(url)
        if parts.scheme or parts.netloc or not parts.path:
            return None
        suffix = (f"?{parts.query}" if parts.query else "") + (
            f"#{parts.fragment}" if parts.fragment else ""
        )
        path = (self.source_dir / unquote(parts.path)).resolve()
        return path, suffix


def _share_parent(path: Path, directory: Path) -> bool:
    """Whether a relative URL between the two stays readable.

    Paths whose only common ancestor is the filesystem root (or that live on different
    Windows drives) would produce ``../../../..`` chains; absolute URIs are clearer there.
    """
    try:
        common = Path(os.path.commonpath([path, directory.resolve()]))
    except ValueError:  # different drives on Windows
        return False
    return common != Path(common.anchor)


def _data_uri(path: Path) -> str:
    mime, _ = mimetypes.guess_type(path.name)
    payload = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime or 'application/octet-stream'};base64,{payload}"
