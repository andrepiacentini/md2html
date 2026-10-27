# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this
project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Heading permalinks: a link icon appears next to headings on hover, as on GitHub (#5).
- Emoji shortcodes (`:tada:` → 🎉) with GitHub's names, from the gemoji database (#2).
- `--toc` adds a table of contents built from the headings down to level 3 (#9).
- GitHub alerts: `> [!NOTE]`, `[!TIP]`, `[!IMPORTANT]`, `[!WARNING]` and `[!CAUTION]`
  blockquotes render as colored callouts with icons, matching GitHub's HTML (#1).
- `md2html FILE` command that renders Markdown to a self-contained HTML page and opens it
  in the default browser, through a temporary file by default.
- `--save` and `--output` to keep the generated page; `-` to read from stdin.
- GitHub Flavored Markdown rendering: tables, task lists, strikethrough, autolinks,
  footnotes, raw HTML, heading anchors and front matter (hidden).
- Syntax highlighting of fenced code blocks with Pygments.
- Relative image and link URLs rewritten to work from the output location, including
  inside raw HTML; `--embed-images` to inline local images.
- Light, dark and automatic themes (`--theme`), and `--title`.

[Unreleased]: https://github.com/andrepiacentini/md2html/commits/main
