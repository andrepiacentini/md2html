"""Regenerate ``src/md2html/assets/emoji.json`` from GitHub's gemoji database.

Usage: ``uv run python scripts/update_emoji.py [GEMOJI_REF]``

GitHub resolves ``:shortcode:`` names with gemoji (https://github.com/github/gemoji), so using
its data keeps md2html's shortcodes identical to GitHub's. Pin ``GEMOJI_REF`` to a commit and
bump it deliberately; the ref is recorded in the generated file.
"""

from __future__ import annotations

import json
import sys
import urllib.request
from pathlib import Path

DEFAULT_REF = "fadaeaf"
SOURCE = "https://raw.githubusercontent.com/github/gemoji/{ref}/db/emoji.json"
TARGET = Path(__file__).resolve().parent.parent / "src" / "md2html" / "assets" / "emoji.json"


def build(entries: list[dict[str, object]], ref: str) -> dict[str, object]:
    """Map every alias to its emoji; custom image-only emoji (no character) are skipped."""
    aliases: dict[str, str] = {}
    for entry in entries:
        emoji = entry.get("emoji")
        names = entry.get("aliases")
        if isinstance(emoji, str) and isinstance(names, list):
            aliases.update(dict.fromkeys(names, emoji))
    return {
        "source": f"https://github.com/github/gemoji/tree/{ref}",
        "license": "MIT License, Copyright (c) 2019 GitHub, Inc.",
        "emoji": dict(sorted(aliases.items())),
    }


def main() -> None:
    ref = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_REF
    with urllib.request.urlopen(SOURCE.format(ref=ref), timeout=30) as response:
        entries = json.load(response)
    data = build(entries, ref)
    TARGET.write_text(json.dumps(data, ensure_ascii=False, indent=0) + "\n", encoding="utf-8")
    print(f"Wrote {len(data['emoji'])} shortcodes from gemoji@{ref} to {TARGET}")  # type: ignore[arg-type]


if __name__ == "__main__":
    main()
