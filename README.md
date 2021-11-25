# colorteller

[![Test Code with Pip](https://github.com/kausalflow/colorteller-package/actions/workflows/tests.yaml/badge.svg?branch=main)](https://github.com/kausalflow/colorteller-package/actions/workflows/tests.yaml)

Benchmark color palettes.

`pip install colorteller`

## We have a website!

We have built a website for color palette discovery and sharing:

https://colorteller.kausalflow.com


## Documentation

Read the [Documentation](http://kausalflow.github.io/colorteller-package/).

## Use the Command Line Tool

```bash
colorteller benchmark -h "#8de4d3" -h "#344b46" -h "#74ee65" -h "#238910" -h "#a6c363" -h "#509d99" -wbc True -t test_colorteller_cmd
```

- `-h` specifies a color in hex format;
- `-t` specifies the folder to hold all the results (charts, metrics json, etc). It should be a folder.;
- `-wbc` is `True` will create benchmark metric charts;

## Use in Python Code


### Create a ColorTeller Object


```
from colorteller.teller import ColorTeller

hex_strings = ["#8de4d3", "#344b46", "#74ee65", "#238910", "#a6c363", "#509d99"]

ct = teller.ColorTeller(hex_strings=hex_strings)
```

To retrieve the properties of the color palette, please refer to [`colorteller.teller`](references/teller.md).

### Create Benchmarks

```python
from colorteller.teller import ColorTeller
from colorteller.utils import benchmark

hex_strings = ["#8de4d3", "#344b46", "#74ee65", "#238910", "#a6c363", "#509d99"]

ct = teller.ColorTeller(hex_strings=hex_strings)
c = teller.Colors(colorteller=ct)

m = c.metrics(
    methods=[
        benchmark.PerceptualDistanceBenchmark,
        benchmark.LightnessBenchmark
    ]
)
```

### Visualizations

#### Metric Visualizations

```python
from colorteller import teller
from colorteller.utils import benchmark
from colorteller.visualize import BenchmarkCharts, ApplicationCharts

hex_strings = ["#8de4d3", "#344b46", "#74ee65", "#238910", "#a6c363", "#509d99"]

ct = teller.ColorTeller(hex_strings=hex_strings)

c = teller.Colors(colorteller=ct)

m = c.metrics(
    methods=[benchmark.PerceptualDistanceBenchmark, benchmark.LightnessBenchmark]
)

charts = BenchmarkCharts(metrics=m, save_folder=".")

charts.distance_matrix(show=True)
charts.noticable_matrix(show=True)
```

#### Demo Figures Using the Color Palette

```python
from colorteller import teller
from colorteller.utils import benchmark
from colorteller.visualize import BenchmarkCharts, ApplicationCharts

hex_strings = ["#8de4d3", "#344b46", "#74ee65", "#238910", "#a6c363", "#509d99"]

ct = teller.ColorTeller(hex_strings=hex_strings)

c = teller.Colors(colorteller=ct)

ac = ApplicationCharts(colors=c, save_folder=".")

ac.charts(save_to=True)

# One could also create specific charts using the following
# ac.bar_chart(show=True)
# ac.line_chart(show=True)
# ac.scatter_chart(show=True)
# ac.donut_chart(show=True)
```