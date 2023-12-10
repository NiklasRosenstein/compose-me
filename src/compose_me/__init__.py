import logging
import os
from pathlib import Path
from typing import Any

import jinja2
import nr.proxy
import yaml

from .types import _FilterArg, _FilterDecorator, _FilterFunction

logger = logging.getLogger(__name__)

#: Decorator to register a filter function. This is a proxy so that the filter can be imported from the plugin
#: file using ``from compose_me import filter``.
filter: _FilterFunction = nr.proxy.proxy()


class Chart:
    """
    Represents a compose-me chart. A chart is a directory containing a ``docker-compose.template.yaml`` file and a
    ``values.yaml`` file. Optionally, it can also contain a ``plugin.py`` file that can be used to define custom
    filters and computed values.
    """

    COMPOSE_TEMPLATE_FILE = "docker-compose.template.yaml"
    VALUES_FILE = "values.yaml"
    PLUGIN_FILE = "plugin.py"
    COMPOSE_ME_CONFIG_KEY = "x-compose-me"

    def __init__(self, directory: Path) -> None:
        self.directory = directory

    def get_default_values(self) -> dict[str, Any]:
        return yaml.safe_load((self.directory / self.VALUES_FILE).read_text())  # type: ignore[no-any-return]

    def get_jinja_environment(self, values: dict[str, Any]) -> jinja2.Environment:
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(self.directory))
        computed_values = {}

        if (plugin_file := self.directory / self.PLUGIN_FILE).is_file():

            def _filter() -> _FilterDecorator:
                def decorator(_func: _FilterArg) -> _FilterArg:
                    logger.debug("Registering filter %s from %s", _func.__name__, pretty_path(plugin_file))
                    env.filters[_func.__name__] = _func
                    return _func

                return decorator

            nr.proxy.set_value(filter, _filter)

            logger.info("Loading plugin %s", pretty_path(plugin_file))
            scope: dict[str, Any] = {"__file__": str(plugin_file), "__name__": plugin_file.name}
            exec(compile(plugin_file.read_text(), plugin_file, "exec"), scope)

            if "get_computed_values" in scope:
                logger.debug("Getting computed values from %s", pretty_path(plugin_file))
                computed_values = scope["get_computed_values"](values)
                if not isinstance(computed_values, dict):
                    raise TypeError(
                        f'The return value of get_computed_values() in "{pretty_path(plugin_file)}" must be a dict.'
                        f"Got {type(computed_values).__name__} instead."
                    )

        env.globals["Values"] = values
        env.globals["Computed"] = computed_values

        return env

    def render(self, env: jinja2.Environment, output_directory: Path) -> None:
        """
        Render the chart to the given output directory. Remove any existing files that have been generated into the
        directory before and are not generated anymore (this is stored in the #FILELIST_FILE).
        """

        logger.info("Rendering chart %s to %s", pretty_path(self.directory), pretty_path(output_directory))

        old_filelist = Project(output_directory).get_filelist()
        new_filelist: list[str] = []

        # Render the docker-compse file.
        compose_file = output_directory / Project.COMPOSE_FILE
        logger.info("Rendering %s", pretty_path(compose_file))
        compose_file.write_text(env.get_template(self.COMPOSE_TEMPLATE_FILE).render())
        new_filelist.append(Project.COMPOSE_FILE)

        # Load the compose file to get the list of auxiliary files.
        logger.info("Loading %s", pretty_path(compose_file))
        compose_me_config = yaml.safe_load(compose_file.read_text()).get(self.COMPOSE_ME_CONFIG_KEY, {})
        auxiliary_files: list[str] = compose_me_config.get("templates", [])

        # Render auxiliary files.
        for filename in auxiliary_files:
            # TODO: Prevent referencing files outside of the chart directory.
            dest_path = (output_directory / filename).resolve()
            filename = str(dest_path.relative_to(output_directory))
            logger.info("Rendering %s", pretty_path(dest_path))
            dest_path.write_text(env.get_template(filename).render())
            new_filelist.append(filename)

        # Remove old files that are not generated anymore.
        for filename in set(old_filelist) - set(new_filelist):
            logger.info("Removing no longer generated file %s", pretty_path(filename))
            (output_directory / filename).unlink()

        # Write the new filelist.
        Project(output_directory).set_filelist(new_filelist)


class Project:
    """
    Represents a compose-me managed Docker-Compose project. A project is a directory containing a ``values.yaml`` file
    that contains the reference to the Chart being rendered and overrides for the values. Once the chart is rendered,
    the ``docker-compose.yaml`` file is generated along with any auxiliary files and the ``.filelist.txt`` file is
    updated to keep track of the generated files.
    """

    VALUES_FILE = "values.yaml"
    FILELIST_FILE = ".filelist.txt"
    COMPOSE_FILE = "docker-compose.yaml"
    CHART_REFERENCE_KEY = "chart"

    def __init__(self, directory: Path) -> None:
        self.directory = directory

    def get_filelist(self) -> list[str]:
        if (filelist_file := self.directory / self.FILELIST_FILE).is_file():
            logger.info("Loading filelist from %s", pretty_path(filelist_file))
            return filelist_file.read_text().splitlines()
        else:
            return []

    def set_filelist(self, filelist: list[str]) -> None:
        filelist_file = self.directory / self.FILELIST_FILE
        logger.info("Writing filelist to %s", pretty_path(filelist_file))
        filelist_file.write_text("\n".join(filelist) + "\n")

    def get_values(self) -> dict[str, Any]:
        return yaml.safe_load((self.directory / self.VALUES_FILE).read_text())  # type: ignore[no-any-return]

    def get_chart_reference(self) -> str:
        return self.get_values()[self.CHART_REFERENCE_KEY]  # type: ignore[no-any-return]


def merge_values(a: dict[str, Any], b: dict[str, Any]) -> dict[str, Any]:
    """
    Merge the two given values dictionaries. The values in ``b`` take precedence over the values in ``a``. All but
    dictionaries are merged by overwriting. Dictionaries are merged recursively.
    """

    result = a.copy()
    for key, value in b.items():
        if isinstance(value, dict) and key in result and isinstance(result[key], dict):
            result[key] = merge_values(result[key], value)
        else:
            result[key] = value
    return result


cwd = Path.cwd()


def pretty_path(path: Path) -> Path:
    try:
        new_path = os.path.relpath(path.absolute(), cwd)
        if new_path.startswith(os.sep.join([os.pardir]*2)):
            return path
    except ValueError:
        return path
    return Path(new_path)
