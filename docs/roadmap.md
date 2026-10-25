# Roadmap

Ideas and known gaps, roughly in priority order. Each item should become a GitHub issue
before work starts; comment on the issue to claim it.

## Rendering fidelity

- [ ] **GitHub alerts** — `> [!NOTE]`, `> [!TIP]`, `> [!IMPORTANT]`, `> [!WARNING]`,
      `> [!CAUTION]` rendered as styled callouts.
- [ ] **Emoji shortcodes** — `:tada:` → 🎉.
- [ ] **Math** — `$inline$` and `$$block$$` (needs an ADR: server-side rendering vs. a
      bundled script).
- [ ] **Mermaid diagrams** — ```` ```mermaid ```` blocks (needs an ADR: requires JavaScript).
- [ ] **Heading permalinks** — hover anchor icon next to headings, like GitHub.

## Workflow

- [ ] **Watch mode** — `--watch` re-renders on save and refreshes the browser.
- [ ] **Links between Markdown files** — option to render linked `.md` files too and point
      links to their `.html` versions.
- [ ] **Multiple files** — `md2html docs/*.md -o site/`.
- [ ] **Table of contents** — optional generated TOC (`--toc`).
- [ ] **Custom CSS** — `--css my.css` to add or replace styles.

## Safety

- [ ] **Safe mode** — `--safe` to strip scripts and event handlers from raw HTML when
      previewing untrusted files (see [SECURITY.md](../SECURITY.md)).

## Distribution

- [ ] First release on PyPI (`md2html-cli`).
- [ ] Homebrew formula.
