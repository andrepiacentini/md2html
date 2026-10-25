# Instructions for AI agents

Working rules for AI coding agents (Claude Code, Codex, Copilot and similar) in this
repository. Human contributors follow the same rules, described in
[CONTRIBUTING.md](CONTRIBUTING.md); this file adds what an agent needs to know. The agent
proposes and implements; a human reviews every change before it is merged.

## Project at a glance

`md2html` is a Python CLI that renders a Markdown file as a self-contained HTML page and
opens it in the browser. Read [docs/architecture.md](docs/architecture.md) before changing
code: it explains the pipeline (parse → rewrite URLs → render → wrap in page → write/open)
and which module owns each step.

```text
src/md2html/
  cli.py         argument parsing and orchestration (no conversion logic)
  converter.py   markdown-it parser setup, URL rewriting walk, title detection
  alerts.py      markdown-it plugin: GitHub alerts (> [!NOTE]…)
  links.py       LinkResolver: relative URL → URL valid from the output location
  highlight.py   Pygments code highlighting and its CSS
  page.py        final page from assets/page.html + assets/style.css
  output.py      writing files (temporary or permanent) and opening the browser
tests/           pytest, one test module per source module
docs/            user and contributor documentation, ADRs in docs/adr/
```

## Commands

| Task | Command |
| --- | --- |
| Install / sync the environment | `make install` (`uv sync`) |
| Lint, format check, type-check | `make lint` |
| Auto-fix and format | `make format` |
| Tests | `make test` |
| Try it on the sample | `make demo` or `uv run md2html examples/sample.md` |

Use `uv` for everything; never `pip install` into the environment. Add dependencies with
`uv add <pkg>` (runtime) or `uv add --group dev <pkg>` (tooling), and commit `uv.lock`.

## Workflow

- Each change starts from a GitHub issue and lives in its own branch, created from an
  up-to-date `main`: `feat/<issue>-<short-slug>`, `fix/<issue>-<short-slug>` or
  `docs/<issue>-<short-slug>`.
- **Test-driven development.** Every new or changed behavior starts with a test.
  1. **Red:** write the tests for the requested behavior and run them, confirming they fail
     for the right reason (not an import error or a typo).
  2. **Green:** write only the code needed to make them pass.
  3. **Refactor** with the tests green.
  - A bug fix starts with a test that reproduces the bug.
  - Tests never touch the network or open a real browser: use `tmp_path` for files and
    monkeypatch `md2html.cli.open_in_browser` (see the `opened` fixture in
    `tests/test_cli.py`).
  - Changes with no behavior to test (docs, CSS only) say so in the PR.
- Commits follow [Conventional Commits](https://www.conventionalcommits.org/) (`feat:`,
  `fix:`, `docs:`, `test:`, `refactor:`, `chore:`, `ci:`), in English, with `Closes #<issue>`
  in the commit that completes the issue.
- **Small PRs: at most 20 changed files**, so a review fits in one sitting. `uv.lock` does
  not count. Bigger work is split into sequential PRs, each complete and green; the
  intermediate ones use `Refs #<issue>`, only the last one `Closes #<issue>`.
- Before committing, `make lint` and `make test` pass and pre-commit reports nothing.
- User-visible changes get a line in `CHANGELOG.md` under **Unreleased**.
- Without explicit authorization the agent does **not** push, open PRs, create tags or
  publish releases: it stops at a local commit and waits.

## User commands

### "push it" / "open the PR"

1. Commit any pending changes of the current issue.
2. Check the branch changes at most 20 files against `main` (excluding `uv.lock`); split
   it first if it does not.
3. Push the branch to `origin` and open a PR to `main` using the PR template: what changes,
   how to test, what was verified (list the tests written first and show they failed
   before the implementation), and `Closes #<issue>`.
4. **Stop and wait for the review.** Do not start the next issue or merge.

### "the PR was merged" / "merged"

1. Check out `main` and `git pull`.
2. Delete the branch locally and, if it still exists, on `origin`.
3. Confirm the issue was closed.

## Code

### Language

Everything in the repository is in **English**: identifiers, comments, docstrings, docs,
commit messages, PR descriptions and CLI messages. This keeps the project open to
contributors anywhere.

### Design

- **Single responsibility.** Keep the module boundaries above: `cli.py` only parses
  arguments and wires the other modules; conversion rules live in `converter.py` and
  `links.py`; I/O lives in `output.py`. A module that starts doing two jobs is split.
- **Open for extension.** New Markdown features enter as markdown-it plugins registered
  in `create_parser()`, not as string post-processing of the rendered HTML.
- **Pure core, I/O at the edges.** `converter`, `links`, `highlight` and `page` take values
  and return strings; only `cli` and `output` touch stdin, the filesystem and the browser.
  The one exception, `--embed-images` reading image files, stays inside `LinkResolver`.
- **No speculative abstraction.** Add a Protocol or a class hierarchy only when a second
  real implementation (or a test fake) needs it. Prefer functions and frozen dataclasses.
- Full type hints; `mypy --strict` must pass. Public functions get a docstring.

### Product rules

- **Fidelity first.** The reference for "correct" rendering is how GitHub renders the same
  Markdown. When in doubt, compare with GitHub and add a test.
- **Self-contained output.** The generated page must work offline: inline CSS, no CDN, no
  web fonts, no external requests, and no JavaScript unless an ADR justifies it.
- **Images and links must keep working** wherever the HTML is written. Any change to URL
  handling goes through `LinkResolver` and is covered in `tests/test_links.py`.
- **Cross-platform.** The CLI runs on Linux, macOS and Windows (CI tests all three). Use
  `pathlib`, `Path.as_uri()` and `encoding="utf-8"` explicitly; never build paths or
  `file://` URLs by string concatenation.
- Significant decisions (new dependency, new output format, JavaScript in the page) get an
  ADR in `docs/adr/`, following the existing numbering.

## Security

- The tool renders raw HTML embedded in Markdown, by design (GitHub does too). Do not add
  features that fetch remote content or execute code at conversion time.
- Never commit secrets. Releases use PyPI Trusted Publishing; no tokens live in the repo.
