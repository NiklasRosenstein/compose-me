# Projects

A project is a chart materialized into a directory with values. This is analogous to what docker-compose calls
"projects" as well. What is different is that a `values.yaml` file is required in the project which specifies the
project's source chart and value overrides. We also track the list of files managed by the chart in a `.filelist.txt`
file.

## Materializing a chart

Create a directory that will serve as the docker-compose project directory. In this directory, create a `values.yaml`
file that specifies the chart source and value overrides. We currently only support a local directory as the chart
source.

The values specified in the project will override default values in the chart. Objects in the YAML are merged
recursively, while all other values are replaced.

__Example__

```yaml
# values.yaml
chart: ../chart
foo: bar
```

In the project directory, run the `compose-me` command to materialize the chart.

```
$ compose-me
[INFO] Loading plugin ../chart/plugin.py
[INFO] Rendering chart ../chart to .
[INFO] Loading filelist from .filelist.txt
[INFO] Rendering docker-compose.yaml
[INFO] Loading docker-compose.yaml
[INFO] Rendering nginx.conf
[INFO] Writing filelist to .filelist.txt
```
