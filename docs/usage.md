# Usage guide

```text
md2html [-h] [-o PATH | -s] [--no-open] [--theme {auto,light,dark}]
        [--embed-images] [--title TITLE] [-V] FILE
```

`FILE` is a Markdown file (UTF-8), or `-` to read from standard input.

## Where the HTML goes

| Command | Output file | Typical use |
| --- | --- | --- |
| `md2html notes.md` | A new temporary file, e.g. `/tmp/md2html-notes-x1y2z3.html` | Quick preview |
| `md2html notes.md --save` | `notes.html`, next to `notes.md` | Keep a rendered copy beside the source |
| `md2html notes.md -o out/page.html` | `out/page.html` (parent folders are created) | Choose the exact path |
| `md2html notes.md -o out/` | `out/notes.html` (`out/` must exist) | Render several files into one folder |

In every case the absolute path of the generated file is printed on standard output, and
the page is opened in the default browser unless you pass `--no-open`. Temporary files are
not deleted by `md2html` (the browser needs them after the command ends); your operating
system cleans its temporary directory periodically.

`--save` and `--output` cannot be combined. When reading from stdin, `--save` is not
available (there is no source file to save next to); use `--output`.

## Images and links

Markdown files refer to images and other files with paths relative to themselves, like
`![logo](img/logo.png)` or `[guide](docs/guide.md)`. `md2html` rewrites those paths so they
keep working from wherever the HTML is written:

- **Temporary preview:** relative paths become absolute `file://` URLs pointing at the
  original files.
- **`--save` / `--output`:** relative paths are recalculated relative to the HTML file. If
  the HTML and the Markdown share no directory other than the filesystem root (or are on
  different Windows drives), absolute `file://` URLs are used instead.
- **`--embed-images`:** local images are read and embedded in the page as `data:` URIs, so
  the HTML file can be moved, emailed or archived on its own. Images that cannot be found are
  left as links.

What is rewritten: image sources and link targets in Markdown syntax, and `src`/`href`
attributes inside raw HTML (for example `<img src="logo.png" width="200">`). What is left
untouched: URLs with a scheme (`https:`, `mailto:`, `data:`…), root-relative URLs
(`/img.png`), protocol-relative URLs (`//cdn…`) and in-page anchors (`#section`).

When reading from stdin, relative paths are resolved from the current directory.

## Markdown support

`md2html` aims to render Markdown the way GitHub does:

- CommonMark, plus the GitHub extensions: tables (with column alignment), task lists,
  strikethrough, and autolinked URLs.
- Footnotes (`text[^1]` … `[^1]: note`).
- [Alerts](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax#alerts):
  a top-level blockquote whose first line is `[!NOTE]`, `[!TIP]`, `[!IMPORTANT]`,
  `[!WARNING]` or `[!CAUTION]` (alone on the line) becomes a colored callout with an icon,
  as on GitHub. Nested or empty alerts stay plain blockquotes, as on GitHub.
- Fenced code blocks with syntax highlighting for every language
  [Pygments](https://pygments.org/languages/) knows; unknown languages are shown as plain
  text.
- Raw HTML, including `<details>`, `<kbd>`, `<sub>`/`<sup>` and aligned images.
- Heading anchors: `## Getting started` gets `id="getting-started"`, so `[link](#getting-started)`
  works.
- YAML front matter at the top of the file is hidden.

The page title is the first level-1 heading, then the file name. `--title` overrides both.

## Themes

`--theme auto` (the default) follows the light/dark preference of your operating system.
`--theme light` and `--theme dark` force one. Code highlighting follows the theme. Printing
the page (Ctrl/Cmd+P) always uses a light, borderless layout, which is a quick way to get a
PDF.

## Exit codes

| Code | Meaning |
| --- | --- |
| `0` | Success (also when no browser could be opened; a warning is printed) |
| `1` | The Markdown file could not be read, or the HTML could not be written |
| `2` | Invalid command-line usage |

## Limitations

See the [roadmap](roadmap.md) for features not supported yet, such as math and Mermaid
diagrams.
