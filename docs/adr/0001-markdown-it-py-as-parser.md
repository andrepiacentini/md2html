# 1. markdown-it-py as the Markdown parser

- **Status:** accepted
- **Date:** 2026-10-25

## Context

The core promise of `md2html` is rendering Markdown the way people are used to seeing it,
which in practice means the way GitHub renders it: CommonMark plus GitHub Flavored Markdown
(tables, task lists, strikethrough, autolinks) and common extras such as footnotes. We also
need to rewrite image and link URLs reliably, and to stay a lightweight, pure-Python
install on Linux, macOS and Windows.

Options considered:

- **Python-Markdown** — mature, but not CommonMark-compliant; its GFM support comes from
  third-party extensions with behavior that differs from GitHub in edge cases.
- **mistune** — fast, but its CommonMark compliance is partial.
- **cmarkgfm / commonmark bindings** — GitHub's own C implementation, so the most faithful,
  but requires compiled wheels and offers no token tree to rewrite URLs before rendering.
- **markdown-it-py** — a port of markdown-it, 100% CommonMark compliant, with a `gfm-like`
  preset, a plugin ecosystem (`mdit-py-plugins`: footnotes, task lists, anchors, front
  matter…) and a token stream we can modify before rendering. Pure Python. Used by
  MyST/Sphinx and Jupyter tooling.

## Decision

Use **markdown-it-py** with the `gfm-like` preset and plugins from **mdit-py-plugins**.
URLs are rewritten by walking the token tree between parsing and rendering. Syntax
highlighting uses **Pygments** through markdown-it's `highlight` hook, so the page needs no
JavaScript.

## Consequences

- New Markdown features are added as plugins in one place (`create_parser()`).
- Fidelity is high but not identical to GitHub; differences are treated as bugs when a
  plugin or option can fix them, and documented otherwise.
- Raw HTML is opaque to the parser, so URLs inside it need a separate (regex-based)
  rewrite.
