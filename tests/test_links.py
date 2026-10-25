from pathlib import Path

import pytest

from md2html.links import LinkResolver


@pytest.fixture
def docs(tmp_path: Path) -> Path:
    (tmp_path / "docs" / "img").mkdir(parents=True)
    (tmp_path / "docs" / "img" / "logo.svg").write_text("<svg xmlns='http://www.w3.org/2000/svg'/>")
    return tmp_path / "docs"


@pytest.mark.parametrize(
    "url",
    [
        "https://example.com/a.png",
        "http://example.com",
        "mailto:someone@example.com",
        "data:image/png;base64,AAAA",
        "//cdn.example.com/x.js",
        "/absolute/from/root.png",
        "#section",
        "",
    ],
)
def test_leaves_non_relative_urls_untouched(docs: Path, url: str) -> None:
    resolver = LinkResolver(source_dir=docs, output_dir=docs.parent / "out")

    assert resolver.resolve(url) == url


def test_relative_url_becomes_file_uri_without_output_dir(docs: Path) -> None:
    resolver = LinkResolver(source_dir=docs)

    assert resolver.resolve("img/logo.svg") == (docs / "img" / "logo.svg").resolve().as_uri()


def test_relative_url_is_relative_to_output_dir(docs: Path) -> None:
    resolver = LinkResolver(source_dir=docs, output_dir=docs.parent / "site")

    assert resolver.resolve("img/logo.svg") == "../docs/img/logo.svg"


def test_unrelated_output_dir_gets_absolute_uri(docs: Path) -> None:
    resolver = LinkResolver(source_dir=docs, output_dir=Path(Path.cwd().anchor))

    assert resolver.resolve("img/logo.svg") == (docs / "img" / "logo.svg").resolve().as_uri()


def test_relative_url_keeps_query_and_fragment(docs: Path) -> None:
    resolver = LinkResolver(source_dir=docs, output_dir=docs)

    assert resolver.resolve("guide.md?raw=1#install") == "guide.md?raw=1#install"


def test_percent_encoded_paths_round_trip(docs: Path) -> None:
    resolver = LinkResolver(source_dir=docs, output_dir=docs.parent)

    assert resolver.resolve("my%20file.png") == "docs/my%20file.png"


def test_embed_images_inlines_existing_files(docs: Path) -> None:
    resolver = LinkResolver(source_dir=docs, embed_images=True)

    assert resolver.resolve_image("img/logo.svg").startswith("data:image/svg+xml;base64,")


def test_embed_images_falls_back_for_missing_files(docs: Path) -> None:
    resolver = LinkResolver(source_dir=docs, output_dir=docs, embed_images=True)

    assert resolver.resolve_image("img/missing.png") == "img/missing.png"


def test_rewrite_html_handles_src_and_href(docs: Path) -> None:
    resolver = LinkResolver(source_dir=docs, output_dir=docs.parent)
    html = (
        '<a href="guide.md"><img src=\'img/logo.svg\' width="80"></a> <a href="https://x.y">x</a>'
    )

    assert resolver.rewrite_html(html) == (
        '<a href="docs/guide.md"><img src=\'docs/img/logo.svg\' width="80"></a>'
        ' <a href="https://x.y">x</a>'
    )
