
from compose_me import filter, global_
from typing import Any
from urllib.parse import urlparse

DOCKER_COMPOSE_VERSION = global_("3.4", name="DOCKER_COMPOSE_VERSION")


@filter
def addOne(value: int) -> int:
    return value + 1


def get_computed_values(values: dict[str, Any]) -> dict[str, Any]:
    return {
        "bindUrl": urlparse(values["bindUrl"].replace("localhost", "127.0.0.1")),
    }
