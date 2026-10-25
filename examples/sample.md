---
description: Front matter is parsed and hidden from the page.
---

# md2html sample

A tour of what `md2html` renders. Try it: `md2html examples/sample.md`.

![How it works](assets/diagram.svg)

## Text

Paragraphs with **bold**, *italic*, ~~strikethrough~~, `inline code`, <kbd>Ctrl</kbd>+<kbd>C</kbd>
and an autolink: https://github.com/andrepiacentini/md2html. Jump to the [tables](#tables)
or read the [usage guide](../docs/usage.md).

> Blockquotes keep their left border.
>
> > And they nest.

## Lists

1. First
2. Second
   - Nested bullet
   - Another one

- [x] Task lists
- [ ] with checkboxes

## Tables

| Feature        | Supported | Notes              |
| :------------- | :-------: | -----------------: |
| Tables         |    yes    |     with alignment |
| Footnotes      |    yes    | like this one[^1]  |

## Code

```python
def greet(name: str) -> str:
    """Say hello."""
    return f"Hello, {name}!"
```

```bash
md2html README.md --save --theme dark
```

## Raw HTML

<p align="center">
  <img src="assets/diagram.svg" width="240" alt="Centered image written in raw HTML">
</p>

<details>
<summary>Collapsible section</summary>

Hidden content, revealed on click.

</details>

---

[^1]: Footnotes are collected at the bottom of the page.
