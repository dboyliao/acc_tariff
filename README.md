This repo is inspired by the [hxu296/tariff](https://github.com/hxu296/tariff) package.

The key difference between `acc-tariff` and `tariff` is that the import tariff at execution time will accumulate across submodules!

NOTE: This repo is for educational purposes only and is not designed to run in any production environment.

# Install
```bash
$ pip install acc-tariff
```

or `uv`
```bash
$ uv sync
```

# Example

```python
import acc_tariff

acc_tariff.set_tarrif("numpy", 100)
acc_tariff.set_tarrif("numpy.fft", 100000)

import numpy  # 100% slower
import numpy.fft  # 100100% slower
```