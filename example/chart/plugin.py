
from typing import Any
from urllib.parse import urlparse


def get_computed_values(values: dict[str, Any]) -> dict[str, Any]:
    return {
        "bindUrl": urlparse(values["bindUrl"].replace("localhost", "127.0.0.1")),
    }
