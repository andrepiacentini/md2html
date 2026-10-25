# Roadmap

Ideas and known gaps, roughly in priority order. Each item has a GitHub issue; comment on
it to claim the work. Issues labeled
[`good first issue`](https://github.com/andrepiacentini/md2html/labels/good%20first%20issue)
are a good place to start.

## Rendering fidelity

- [x] **GitHub alerts** ([#1](https://github.com/andrepiacentini/md2html/issues/1)) — `> [!NOTE]`, `> [!TIP]`, `> [!IMPORTANT]`, `> [!WARNING]`,
      `> [!CAUTION]` rendered as styled callouts.
- [ ] **Emoji shortcodes** ([#2](https://github.com/andrepiacentini/md2html/issues/2)) — `:tada:` → 🎉.
- [ ] **Math** ([#3](https://github.com/andrepiacentini/md2html/issues/3)) — `$inline$` and `$$block$$` (needs an ADR: server-side rendering vs. a
      bundled script).
- [ ] **Mermaid diagrams** ([#4](https://github.com/andrepiacentini/md2html/issues/4)) — ```` ```mermaid ```` blocks (needs an ADR: requires JavaScript).
- [ ] **Heading permalinks** ([#5](https://github.com/andrepiacentini/md2html/issues/5)) — hover anchor icon next to headings, like GitHub.

## Workflow

- [ ] **Watch mode** ([#6](https://github.com/andrepiacentini/md2html/issues/6)) — `--watch` re-renders on save and refreshes the browser.
- [ ] **Links between Markdown files** ([#7](https://github.com/andrepiacentini/md2html/issues/7)) — option to render linked `.md` files too and point
      links to their `.html` versions.
- [ ] **Multiple files** ([#8](https://github.com/andrepiacentini/md2html/issues/8)) — `md2html docs/*.md -o site/`.
- [ ] **Table of contents** ([#9](https://github.com/andrepiacentini/md2html/issues/9)) — optional generated TOC (`--toc`).
- [ ] **Custom CSS** ([#10](https://github.com/andrepiacentini/md2html/issues/10)) — `--css my.css` to add or replace styles.

## Safety

- [ ] **Safe mode** ([#11](https://github.com/andrepiacentini/md2html/issues/11)) — `--safe` to strip scripts and event handlers from raw HTML when
      previewing untrusted files (see [SECURITY.md](../SECURITY.md)).

## Distribution

- [ ] First release on PyPI (`md2html-cli`).
- [ ] Homebrew formula ([#12](https://github.com/andrepiacentini/md2html/issues/12)).
