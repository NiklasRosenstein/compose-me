---
weight: 10
---

# Plugin API

  [Jinja]: https://jinja.palletsprojects.com/

A `plugin.py` script in a compose-me chart can be used to register custom Jinja filters and globals, as well as to
derive computed values from the project's values.

__Example:__

```py
# plugin.py
from compose_me import filter
from typing import Any
from urllib.parse import urlparse


@filter
def addOne(value: int) -> int:
    return value + 1


def get_computed_values(values: dict[str, Any]) -> dict[str, Any]:
    return {
        "repository": values["image"].split(":")[0],
        "tag": values["image"].split(":")[0],
    }
```

```yaml
# docker-compose.template.yaml
services:
  web:
    image: "{{Computed.repository}}:{{Computed.tag}}"
    ports:
      - "{{Values.port|addOne}}:80"
```


## Registering extensions

Custom filters and global values can be registered to the [Jinja][] template engine using the respective API
provided by the `compose_me` module.

### class `compose_me.filter`

Decorator for functions that are to be registered as filters to the Jinja environment. The decorated function must
exist in the global scope of the plugin scope to be registered.

```py
from compose_me import filter

@filter
def addOne(value: int) -> int:
    return value + 1
```

### class `compose_me.global_`

Decorator for functions or values that are to be registered as global values to the Jinja environment. The decorated
value must exist in the global scope of the plugin scope to be registered.

```py
from compose_me import global_
from typing import NoReturn

@global_
def throw() -> NoReturn:
    raise Exception("no way this failed")

THE_UNIVERSE = global_(42)
```

## Computing values

### func `get_computed_values`

```py
def get_computed_values(values: dict[str, Any]) -> dict[str, Any]: ...
```

If this function is defined in a compose-me chart's `plugin.py`, it will be called with the `Values` object and is
expected to return the `Computed` object.
