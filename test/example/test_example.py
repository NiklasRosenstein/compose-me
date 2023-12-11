
from typing import Iterator
from compose_me.__main__ import _main
from tempfile import TemporaryDirectory
from pathlib import Path
from pytest import fixture

EXAMPLE_CHART = (Path(__file__).parent.parent.parent / "example" / "chart").absolute()
EXPECTED_OUTPUTS = Path(__file__).parent / "outputs"


@fixture
def tempdir() -> Iterator[Path]:
    with TemporaryDirectory() as tmp:
        yield Path(tmp)


def test_render_example(tempdir: Path) -> None:
    tempdir.joinpath("values.yaml").write_text(f"chart: {EXAMPLE_CHART}\n")
    _main(change_dir=tempdir)

    for file in EXPECTED_OUTPUTS.iterdir():
        has_file = tempdir / file.name
        assert file.read_text() == has_file.read_text(), f"Content of {file.name} is not the same"
