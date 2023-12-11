import logging
import os
from pathlib import Path
from typing import Optional

from typer import Option, Typer

from compose_me import Chart, Project, merge_values

app = Typer()


@app.command()
def _main(verbose: bool = Option(False, "-v"), change_dir: Optional[Path] = Option(None, "-c")) -> None:
    """
    Generate the files for the compose-me project in the current working directory.

    The chart reference must be specified in the ``compose-me.yaml`` file in the ``chart`` key.
    """

    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="[%(asctime)s %(levelname)s %(name)s]: %(message)s" if verbose else "[%(levelname)s] %(message)s",
    )

    if change_dir:
        logging.info("Changing working directory to %s", change_dir)
        os.chdir(change_dir)

    try:
        project = Project(Path.cwd())
        chart_directory = Path(project.get_chart_reference()).resolve()
        chart = Chart(chart_directory)
        values = merge_values(chart.get_default_values(), project.get_values())
        chart.render(chart.get_jinja_environment(values), Path.cwd())
    except FileNotFoundError as e:
        logging.error("Could not find file %s", e.filename, exc_info=verbose)
        exit(1)


if __name__ == "__main__":
    app()
