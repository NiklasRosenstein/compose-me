# Charts

  [Jinja]: https://jinja.palletsprojects.com/

Similar to a Helm chart, a Compose-me chart is a directory containing template files. The main entrypoint is the
`docker-compose.template.yaml` file. This file is a [Jinja][] template that will be rendered into a `docker-compose.yaml`
file in the output directory.

__Example:__

```yaml
# docker-compose.template.yaml
version: '3.4'
services:
  web:
    image: "{{Values.image}}"
    ports:
      - "{{Values.port}}:80"
    volumes:
      - ./nginx.conf:/etc/nginx/default.conf:ro
```

## Values

The `Values` object contains the values defined in the `values.yaml` file. A chart may define its default values in
this file. The values can be overriden by the project.

__Example:__

```yaml
# values.yaml
image: nginx:alpine
port: 80
```

## Auxiliary files

Additional files can be rendered using [Jinja][] templates and copied to the output directory alongside the
`docker-compose.yaml` file. These files must be listed in the `x-compose-me.templates` section.

```yaml
# docker-compose.template.yaml
# ...
x-compose-me:
  templates:
    - ./nginx.conf
```

## Plugins

A chart may contain a `plugin.py` script in the root of your project. This script is executed before rendering the
templates and can be used to define custom Jinja filters, as well as generating computed values that can be referenced
in the templates using the `Computed` object.

Learn more about plugins in [Plugin API](./plugin_api.md).
