# Contributing to md2html

Thanks for your interest in improving `md2html`! Bug reports, feature ideas, documentation
fixes and code are all welcome. By participating you agree to follow our
[Code of Conduct](CODE_OF_CONDUCT.md).

## Ways to contribute

- **Report a bug** — open an [issue](https://github.com/andrepiacentini/md2html/issues/new/choose)
  with the smallest Markdown snippet that reproduces it, the command you ran and your
  `md2html --version`.
- **Suggest a feature** — open a feature request describing the problem first, then the
  solution you have in mind. For bigger ideas, start a
  [discussion](https://github.com/andrepiacentini/md2html/discussions).
- **Pick an issue** — issues labeled
  [`good first issue`](https://github.com/andrepiacentini/md2html/labels/good%20first%20issue)
  are a good start. Comment on the issue so nobody duplicates the work.
- **Improve the docs** — typos and clarifications can go straight to a pull request.

For anything beyond a small fix, please open (or comment on) an issue before writing code,
so we can agree on the approach.

## Development setup

You need [uv](https://docs.astral.sh/uv/) and Git. uv installs the right Python for you.

```console
git clone https://github.com/<your-user>/md2html.git
cd md2html
make install                  # uv sync: creates .venv with the project and dev tools
uv tool install pre-commit && pre-commit install   # optional, runs checks on commit
make test                     # run the tests
make demo                     # render examples/sample.md in your browser
```

See [docs/development.md](docs/development.md) for the full guide: project layout, tests,
and how releases work.

## Making a change

1. Fork the repository and create a branch from `main`:
   `feat/<issue>-<short-slug>` or `fix/<issue>-<short-slug>`.
2. **Write the test first.** Add a failing test that describes the new behavior (or
   reproduces the bug), then write the code that makes it pass. Tests live in `tests/`,
   one module per source module.
3. Keep the code consistent with the rest of the project — the
   [architecture guide](docs/architecture.md) explains which module owns what.
4. Run `make lint` and `make test`. Both must pass.
5. Update the docs (`README.md`, `docs/`) if you changed options or behavior, and add a line
   to `CHANGELOG.md` under **Unreleased**.
6. Commit using [Conventional Commits](https://www.conventionalcommits.org/):
   `feat: support GitHub alerts`, `fix: keep query string on image URLs`.
7. Open a pull request and fill in the template. Keep PRs focused and small (ideally under
   20 files); split large work into several PRs.

## Pull request review

- CI runs lint, type-checking and the tests on Linux, macOS and Windows with every
  supported Python version. A PR needs a green CI and one maintainer approval.
- Reviewers may ask for changes; that is a normal part of the process, not a rejection.
- PRs are squash-merged, so the PR title becomes the commit message: make it a good
  Conventional Commit.

## Style

- Python 3.11+, fully type-hinted (`mypy --strict`), formatted and linted by Ruff
  (`make format` fixes most issues).
- Everything in English: code, comments, docs and commit messages.
- The generated HTML must stay self-contained: no CDN links, web fonts or remote requests.

## License

By contributing, you agree that your contributions will be licensed under the
[MIT License](LICENSE).
