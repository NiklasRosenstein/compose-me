# Welcome to the compose-me documentation!

  [Helm]: https://helm.sh/
  [Jinja]: https://jinja.palletsprojects.com/

Compose-me is a tool inspired by [Helm][] to create templates for docker-compose projects. It is particularly useful
for relatively complex applications that requires some customization. Compose-me allows you to create a template
project that can be configured using a small subset of well-defined values.

Charts created for compose-me use the [Jinja][] template engine and will therefore, directory structure aside, look
a little bit different from Helm charts.

## Features

* **Auxiliary files**: Compose-me allows you to include auxiliary files in your chart that will be copied to the
  output directory. This is useful for configuration files, scripts, etc.
* **Python plugins**: Compose-me allows you to embed a Python plugin in your chart that can be used to compute
  values and register Jinja template filters.

## Installation

Install compose-me from PyPI:

    $ pipx install compose-me

Compose-me requires Python 3.10 or newer.
