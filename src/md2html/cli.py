"""Command-line interface: ``md2html FILE [options]``."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import cast

from md2html import __version__
from md2html.converter import RenderOptions, Theme, render_document
from md2html.output import open_in_browser, write_html, write_temp_html

EXIT_OK = 0
EXIT_ERROR = 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="md2html",
        description=(
            "Render a Markdown file as a self-contained HTML page and open it in the browser. "
            "By default the page goes to a temporary file; use --output or --save to keep it."
        ),
    )
    parser.add_argument("file", metavar="FILE", help="Markdown file to render, or '-' for stdin")

    destination = parser.add_mutually_exclusive_group()
    destination.add_argument(
        "-o",
        "--output",
        metavar="PATH",
        type=Path,
        help="write the HTML to PATH (a file, or an existing directory)",
    )
    destination.add_argument(
        "-s",
        "--save",
        action="store_true",
        help="write the HTML next to FILE, with the .html extension",
    )

    parser.add_argument(
        "--no-open", action="store_true", help="do not open the result in the browser"
    )
    parser.add_argument(
        "--theme",
        choices=["auto", "light", "dark"],
        default="auto",
        help="color scheme of the page (default: auto, follows the system)",
    )
    parser.add_argument(
        "--embed-images",
        action="store_true",
        help="inline local images in the HTML, so the file works on its own",
    )
    parser.add_argument("--title", help="page title (default: first level-1 heading)")
    parser.add_argument("-V", "--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    from_stdin = args.file == "-"

    if from_stdin and args.save:
        parser.error("--save needs a file; use --output when reading from stdin")

    try:
        if from_stdin:
            markdown, source_dir, stem = sys.stdin.read(), Path.cwd(), "stdin"
        else:
            source = Path(args.file).expanduser().resolve()
            markdown, source_dir, stem = (
                source.read_text(encoding="utf-8"),
                source.parent,
                source.stem,
            )
    except (OSError, UnicodeDecodeError) as error:
        print(f"md2html: cannot read {args.file}: {error}", file=sys.stderr)
        return EXIT_ERROR

    destination = _destination(args.output, args.save, source_dir, stem)
    options = RenderOptions(
        source_dir=source_dir,
        output_dir=destination.parent if destination else None,
        embed_images=args.embed_images,
        theme=cast(Theme, args.theme),
        title=args.title,
    )
    html = render_document(markdown, options, fallback_title=stem)

    try:
        path = write_html(html, destination) if destination else write_temp_html(html, stem)
    except OSError as error:
        print(f"md2html: cannot write output: {error}", file=sys.stderr)
        return EXIT_ERROR

    print(path)
    if not args.no_open and not open_in_browser(path):
        print("md2html: no browser available; open the file above manually", file=sys.stderr)
    return EXIT_OK


def _destination(output: Path | None, save: bool, source_dir: Path, stem: str) -> Path | None:
    if save:
        return source_dir / f"{stem}.html"
    if output is None:
        return None
    output = output.expanduser().resolve()
    return output / f"{stem}.html" if output.is_dir() else output


if __name__ == "__main__":
    sys.exit(main())
