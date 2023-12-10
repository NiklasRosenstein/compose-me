
<h1 align="center">compose-me</h1>

Compose-Me is Helm's little sister: A templating tool specialized on Docker Compose projects.

## Installation

Install Compose-Me from PyPI:

    $ pipx install compose-me

## Quickstart

Check out the `example` directory for a quickstart. To render the example project, change into the `example/project`
directory and run `compose-me render`. Then you can use `docker-compose` as you are used to.

## How does it work?

  [Jinja]: https://jinja.palletsprojects.com/

Compose-Me twomajor concepts that translate into the file system: Charts and Projects. Similar to Helm, a Chart is a
directory that contains templates to generate a set of files. These files are then used as a docker-compose Project.

### Chart

A folder that contains a `docker-compose.template.yaml` file and optionally other files, as well as a `values.yaml`
file that contains the default values for rendering the templates. Templates are turned into a Project by running the
`compose-me render` command.

The templating engine used is [Jinja][].

Auxiliary files that will be rendered into the project in addition to the `docker-compose.yaml` must be listed in the
`x-compose-me.templates` section of the `docker-compose.yaml` file:

```yaml
x-compose-me:
  templates:
    - ./nginx.conf
```

### Chart plugins

A chart may contain a `compose-me.py` script in the root of your project. This script is executed before rendering the
templates and can be used to define custom filters and functions, as well as generating computed values that can be
referenced in the templates.

__Example__:

```python
from compose_me import filter

@filter()
def add_one(value: int) -> int:
    return value + 1

def get_computed_values(values: dict[str, Any]) -> dict[str, Any]:
    return {
        "computed_value": values["some_value"] + 1
    }
```

### Project

A Project is a directory that contains a `docker-compose.yaml` and auxiliary files. In addition to a normal
docker-compose project, a Compose-Me project stores the project configuration (that is, chart source and overriding
values) in a `compose-me.yaml` file. The project files can be (re-)generated using the `compose-me render` command.
