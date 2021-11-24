# colorteller

[![Test Code with Pip](https://github.com/kausalflow/colorteller-package/actions/workflows/tests.yaml/badge.svg?branch=main)](https://github.com/kausalflow/colorteller-package/actions/workflows/tests.yaml)

Benchmark color palettes.

`pip install colorteller`


## How to Use Command Line Tool

```bash
colorteller benchmark -h "#8de4d3" -h "#344b46" -h "#74ee65" -h "#238910" -h "#a6c363" -h "#509d99" -wbc True -t test_colorteller_cmd
```

- `-h` specifies a color in hex format;
- `-t` specifies the folder to hold all the results (charts, metrics json, etc);
- `-wbc` is `True` will create benchmark metric charts;