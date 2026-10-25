import io
from pathlib import Path

import pytest

from md2html import cli


@pytest.fixture
def opened(monkeypatch: pytest.MonkeyPatch) -> list[Path]:
    """Capture browser calls instead of opening a real browser."""
    calls: list[Path] = []

    def fake_open(path: Path) -> bool:
        calls.append(path)
        return True

    monkeypatch.setattr(cli, "open_in_browser", fake_open)
    return calls


@pytest.fixture
def readme(tmp_path: Path) -> Path:
    source = tmp_path / "project" / "README.md"
    source.parent.mkdir()
    source.write_text("# Project\n\n![shot](img/shot.png)\n", encoding="utf-8")
    return source


def test_default_writes_temp_file_and_opens_browser(
    readme: Path, opened: list[Path], capsys: pytest.CaptureFixture[str]
) -> None:
    assert cli.main([str(readme)]) == cli.EXIT_OK

    path = Path(capsys.readouterr().out.strip())
    assert path.name.startswith("md2html-README-")
    assert opened == [path]
    assert (readme.parent / "img" / "shot.png").as_uri() in path.read_text(encoding="utf-8")
    path.unlink()


def test_save_writes_next_to_source(readme: Path, opened: list[Path]) -> None:
    assert cli.main([str(readme), "--save", "--no-open"]) == cli.EXIT_OK

    html = (readme.parent / "README.html").read_text(encoding="utf-8")
    assert 'src="img/shot.png"' in html
    assert opened == []


def test_output_file_rewrites_urls_relative_to_it(
    readme: Path, tmp_path: Path, opened: list[Path]
) -> None:
    target = tmp_path / "site" / "index.html"

    assert cli.main([str(readme), "-o", str(target), "--no-open"]) == cli.EXIT_OK

    assert 'src="../project/img/shot.png"' in target.read_text(encoding="utf-8")


def test_output_directory_uses_source_name(
    readme: Path, tmp_path: Path, opened: list[Path]
) -> None:
    out_dir = tmp_path / "out"
    out_dir.mkdir()

    assert cli.main([str(readme), "-o", str(out_dir), "--no-open"]) == cli.EXIT_OK

    assert (out_dir / "README.html").is_file()


def test_reads_from_stdin(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, opened: list[Path]
) -> None:
    monkeypatch.setattr("sys.stdin", io.StringIO("# From stdin\n"))
    target = tmp_path / "stdin.html"

    assert cli.main(["-", "-o", str(target), "--no-open"]) == cli.EXIT_OK

    assert "<title>From stdin</title>" in target.read_text(encoding="utf-8")


def test_save_with_stdin_is_a_usage_error(opened: list[Path]) -> None:
    with pytest.raises(SystemExit) as exit_info:
        cli.main(["-", "--save"])

    assert exit_info.value.code == 2


def test_missing_file_is_reported(
    tmp_path: Path, opened: list[Path], capsys: pytest.CaptureFixture[str]
) -> None:
    assert cli.main([str(tmp_path / "nope.md")]) == cli.EXIT_ERROR

    assert "cannot read" in capsys.readouterr().err
    assert opened == []


def test_warns_when_no_browser_is_available(
    readme: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(cli, "open_in_browser", lambda path: False)

    assert cli.main([str(readme), "--save"]) == cli.EXIT_OK

    assert "no browser available" in capsys.readouterr().err
