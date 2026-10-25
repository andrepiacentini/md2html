# Security policy

## Supported versions

Security fixes are released for the latest minor version of `md2html` only.

## Reporting a vulnerability

Please **do not open a public issue** for security problems. Report them privately through
GitHub: go to the repository's **Security** tab and choose
[**Report a vulnerability**](https://github.com/andrepiacentini/md2html/security/advisories/new).

Include a description of the issue, the steps or Markdown needed to reproduce it, and the
impact you expect. You should receive an answer within 7 days. Once a fix is released, the
advisory is published and you are credited, unless you prefer otherwise.

## Security model

`md2html` is meant to preview Markdown files you trust, the same way you would open them in
an editor:

- **Raw HTML in the Markdown is rendered as-is**, like GitHub does, but without GitHub's
  sanitization. A Markdown file containing `<script>` will run that script when the page is
  opened from your disk. Do not preview untrusted Markdown with `md2html`.
- `md2html` itself never makes network requests, and the generated page loads no remote
  assets of its own. Remote images or links written in the Markdown are loaded by your
  browser as usual.
- `--embed-images` reads the local files referenced by the Markdown, including paths that
  point outside the Markdown file's directory (e.g. `../../image.png`).
