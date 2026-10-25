# Development guide

## Requirements

- [uv](https://docs.astral.sh/uv/getting-started/installation/) (manages Python, the
  virtual environment and dependencies)
- Git and `make` (on Windows, run the commands from the Makefile directly, e.g.
  `uv run pytest`)

## Setup

```console
make install            # uv sync: .venv with md2html (editable) and the dev tools
uv tool install pre-commit
pre-commit install      # run lint and format checks on every commit
```

`.python-version` pins the Python used for local development; CI also tests every other
supported version.

## Everyday commands

| Command | What it does |
| --- | --- |
| `make test` | Run the tests (`pytest`) |
| `make coverage` | Tests with a coverage report |
| `make lint` | `ruff check`, `ruff format --check` and `mypy --strict` |
| `make format` | Auto-fix lint issues and format the code |
| `make demo` | Render `examples/sample.md` and open it |
| `make build` | Build the wheel and sdist into `dist/` |
| `uv run md2html FILE` | Run the CLI from the working tree |

## Tests

- Tests live in `tests/`, one module per source module (`test_links.py` for `links.py`…).
- Use `tmp_path` for files. Never open a real browser: the `opened` fixture in
  `tests/test_cli.py` replaces `open_in_browser` and records the calls.
- Tests must pass on Linux, macOS and Windows: build expected paths with `pathlib`
  (`path.as_uri()`), never by hand.
- We practice TDD: write the failing test first, then the code. Bug fixes start with a test
  that reproduces the bug.

## Visual checks

Rendering changes (CSS, new Markdown features) should be checked in a browser, in both
themes:

```console
uv run md2html examples/sample.md --theme light
uv run md2html examples/sample.md --theme dark
```

Compare with how GitHub renders the same file. Attach before/after screenshots to the PR.

## Dependencies

- Runtime: `uv add <package>`; dev tools: `uv add --group dev <package>`. Always commit
  `uv.lock`.
- Keep runtime dependencies few and pure Python. A new runtime dependency needs an ADR.
- Dependabot opens monthly grouped updates for Python packages and GitHub Actions.

## Releasing

Releases are published to PyPI by `.github/workflows/release.yml` when a `v*` tag is pushed,
using [Trusted Publishing](https://docs.pypi.org/trusted-publishers/) (no API token).

One-time setup (maintainer):

1. On PyPI, add a pending trusted publisher for project `md2html-cli`: owner
   `andrepiacentini`, repository `md2html`, workflow `release.yml`, environment `pypi`.
2. On GitHub, create the `pypi` environment (Settings → Environments), optionally requiring
   a reviewer.

Each release:

1. Bump the version: `uv version --bump minor` (or `patch` / `major`).
2. In `CHANGELOG.md`, rename **Unreleased** to the new version with today's date and add a
   fresh empty **Unreleased** section.
3. Commit (`chore: release v0.2.0`), merge to `main`, then tag and push:
   `git tag v0.2.0 && git push origin v0.2.0`.
4. The workflow checks the tag matches the version, builds, publishes to PyPI and creates
   the GitHub release with generated notes.
