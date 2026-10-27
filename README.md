# md2html

[![CI](https://github.com/andrepiacentini/md2html/actions/workflows/ci.yml/badge.svg)](https://github.com/andrepiacentini/md2html/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/md2html-cli.svg)](https://pypi.org/project/md2html-cli/)
[![Python](https://img.shields.io/pypi/pyversions/md2html-cli.svg)](https://pypi.org/project/md2html-cli/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

**Read any Markdown file as a clean web page, straight from your terminal.**

```console
$ md2html README.md
/var/folders/…/md2html-README-k2j1x9.html     # …and your browser opens it
```

`md2html` turns a Markdown file into a single, self-contained HTML page that looks like
the Markdown you see on GitHub, and opens it in your default browser. Images and links keep
working, code is highlighted, and nothing is fetched from the internet.

## Features

- **Faithful rendering** — GitHub Flavored Markdown: tables, task lists, strikethrough,
  autolinks, footnotes, alerts (`> [!NOTE]`), emoji shortcodes (`:tada:`), fenced code with
  syntax highlighting, raw HTML and heading permalinks.
- **Images and links that work** — relative paths are resolved from the Markdown file's
  location, wherever the HTML ends up. `--embed-images` produces a single portable file.
- **Temporary or permanent** — preview through a temporary file (default), or keep the
  result with `--save` / `--output`.
- **Self-contained output** — one HTML file with inline CSS; no CDN, no web fonts, no
  JavaScript, works offline.
- **Light and dark themes** — follows your system by default, or force one with `--theme`.

## Installation

`md2html` needs Python 3.11 or later. Install it as an isolated command-line tool:

```console
uv tool install md2html-cli     # with uv (recommended)
pipx install md2html-cli        # or with pipx
```

The command is called `md2html`. To try it without installing:
`uvx --from md2html-cli md2html README.md`.

## Usage

```console
md2html NOTES.md                      # preview in a temporary file
md2html NOTES.md --save               # write NOTES.html next to NOTES.md and open it
md2html NOTES.md -o site/notes.html   # write to a chosen path
md2html NOTES.md -o site/             # write site/NOTES.html
md2html NOTES.md -o notes.html --embed-images --no-open
cat NOTES.md | md2html -              # read from stdin
```

| Option | Description |
| --- | --- |
| `-o, --output PATH` | Write the HTML to `PATH` (a file, or an existing directory). |
| `-s, --save` | Write the HTML next to the Markdown file, with the `.html` extension. |
| `--no-open` | Do not open the browser; just print the path. |
| `--theme {auto,light,dark}` | Color scheme. `auto` follows the system (default). |
| `--embed-images` | Inline local images as `data:` URIs, so the file works on its own. |
| `--title TITLE` | Page title. Defaults to the first level-1 heading, then the file name. |
| `--toc` | Add a table of contents (headings down to level 3) at the top of the page. |
| `-V, --version` | Show the version. |

The path of the generated file is always printed to stdout, so `md2html` composes with
other tools. See the [usage guide](docs/usage.md) for details on how images and links are
resolved.

## Documentation

- [Usage guide](docs/usage.md)
- [Architecture](docs/architecture.md)
- [Development setup](docs/development.md)
- [Architecture decision records](docs/adr/)

## Contributing

Contributions are welcome — bug reports, ideas, documentation and code. Please read
[CONTRIBUTING.md](CONTRIBUTING.md) and our [Code of Conduct](CODE_OF_CONDUCT.md) first.
Security issues: see [SECURITY.md](SECURITY.md).

## License

[MIT](LICENSE) © Andre Piacentini
