import json
import textwrap
from typing import Any

import yaml

from compose_me import filter, global_


@filter
def toYaml(value: Any) -> str:
    """
    Converts a value to YAML. If the value is `None`, an empty string is returned. The YAML is returned
    without a document end marker.
    """

    if value is None:
        return ""
    result = yaml.safe_dump(value, sort_keys=False)
    if result.endswith("...\n"):
        result = result[:-4]  # Remove YAML document end marker
    return result


@filter
def toJson(value: Any, indent: int = 0) -> str:
    """
    Converts a value to JSON.
    """

    return json.dumps(value, indent=indent)


@filter
def indent(text: str, spaces: int) -> str:
    """
    Indents all lines by the specified number of spaces.
    """

    return textwrap.indent(text, " " * spaces)


@filter
def nindent(text: str, spaces: int) -> str:
    """
    Indents all but the first line by the specified number of spaces.
    """

    if "\n" not in text:
        return text
    first, *rest = text.splitlines(True)
    prefix = " " * spaces
    return first + "\n".join(prefix + line for line in rest)


@global_
def throw(message: str, *args: Any) -> None:
    """
    Throw an exception with the specified message. For use within if blocks.
    """

    raise Exception(message.format(*args))
