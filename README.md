# Example

```python
import acc_tariff

acc_tariff.set_tarrif("numpy", 100)
acc_tariff.set_tarrif("numpy.fft", 100000)

import numpy  # 100% slower
import numpy.fft  # 100100% slower
```