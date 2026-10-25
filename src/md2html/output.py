"""Writing the generated page to disk and opening it in the browser."""

from __future__ import annotations

import os
import re
import tempfile
import webbrowser
from pathlib import Path

TEMP_PREFIX = "md2html-"


def write_html(html: str, path: Path) -> Path:
    """Write ``html`` to ``path`` (creating parent directories) and return the absolute path."""
    path = path.expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
    return path


def write_temp_html(html: str, stem: str) -> Path:
    """Write ``html`` to a new file in the system temporary directory.

    The file is not deleted afterwards: the browser opens it asynchronously and the OS
    cleans its temporary directory on its own schedule.
    """
    safe_stem = re.sub(r"[^\w.-]+", "-", stem).strip("-") or "document"
    fd, name = tempfile.mkstemp(prefix=f"{TEMP_PREFIX}{safe_stem}-", suffix=".html")
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        handle.write(html)
    return Path(name).resolve()


def open_in_browser(path: Path) -> bool:
    """Open ``path`` in the default browser; returns ``False`` if no browser is available."""
    return webbrowser.open(path.resolve().as_uri())
