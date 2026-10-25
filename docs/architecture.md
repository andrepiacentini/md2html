# Architecture

`md2html` is a small pipeline. Each step is owned by one module, and only the two edge
modules (`cli` and `output`) perform I/O.

```text
              ┌────────┐   ┌──────────────────────────────────────┐   ┌─────────┐   ┌──────────┐
 FILE / stdin │ cli.py │──▶│ converter.py                          │──▶│ page.py │──▶│output.py │──▶ browser
              │  args  │   │ parse ─▶ rewrite URLs ─▶ render body  │   │ wrap in │   │ write +  │
              └────────┘   │          (links.py)     (highlight.py)│   │ template│   │ open     │
                           └──────────────────────────────────────┘   └─────────┘   └──────────┘
```

## Modules

| Module | Responsibility |
| --- | --- |
| `cli.py` | Parses arguments, reads the input, decides the destination, wires the other modules, maps errors to exit codes. No conversion logic. |
| `converter.py` | Builds the markdown-it parser (`create_parser`), walks the token tree to rewrite URLs, renders the HTML fragment and finds the title. `render_document` is the public entry point. |
| `links.py` | `LinkResolver`: decides whether a URL is local and relative, and rewrites it for the output location (relative path, `file://` URI or `data:` URI). Also rewrites `src`/`href` in raw HTML. |
| `alerts.py` | markdown-it plugin for GitHub alerts (`> [!NOTE]`…): turns qualifying blockquotes into `markdown-alert` callouts before inline parsing. |
| `highlight.py` | Pygments highlighting for fenced code, and the matching light/dark CSS. |
| `page.py` | Fills `assets/page.html` with the title, theme, CSS (`assets/style.css` + Pygments CSS) and body. |
| `output.py` | Writes the page to a chosen path or to a temporary file, and opens it with `webbrowser`. |

## Key design points

**URL rewriting happens on tokens, not on HTML.** markdown-it produces a token tree; we
change the `src` of `image` tokens and the `href` of `link_open` tokens before rendering.
This is exact and immune to HTML-escaping issues. Raw HTML blocks are opaque to the parser,
so for `html_block`/`html_inline` tokens `LinkResolver.rewrite_html` uses a targeted regex
over `src=`/`href=` attributes.

**The output directory drives URL rewriting.** `RenderOptions.output_dir` is `None` for
temporary previews (absolute `file://` URIs, which work from anywhere) and the destination
folder otherwise (relative URLs, so a saved page plus its images can be moved together).

**The page is self-contained.** CSS is inlined from package data loaded with
`importlib.resources`; there is no JavaScript and no remote resource. Theme switching uses
CSS custom properties keyed on `<html data-theme="…">` plus `prefers-color-scheme`.

**Pure core.** `converter`, `links`, `highlight` and `page` are functions of their inputs
(except `--embed-images`, which reads image files), which keeps them easy to test without
mocks.

## Adding a Markdown feature

1. Find (or write) a markdown-it plugin; [mdit-py-plugins](https://mdit-py-plugins.readthedocs.io/)
   covers many.
2. Register it in `create_parser()` in `converter.py`.
3. Add styles to `assets/style.css` if the feature introduces new HTML elements or classes.
4. Add tests in `tests/test_converter.py` and a section in `examples/sample.md`.
5. Document it in `docs/usage.md` and `CHANGELOG.md`.

Adding a new runtime dependency or JavaScript to the page requires an ADR in `docs/adr/`.
