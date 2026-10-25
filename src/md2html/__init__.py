"""md2html: render Markdown as a faithful, self-contained HTML page."""

from importlib.metadata import PackageNotFoundError, version

from md2html.converter import RenderOptions, render_document

__all__ = ["RenderOptions", "__version__", "render_document"]

try:
    __version__ = version("md2html-cli")
except PackageNotFoundError:  # running from a source tree without installing
    __version__ = "0.0.0"
