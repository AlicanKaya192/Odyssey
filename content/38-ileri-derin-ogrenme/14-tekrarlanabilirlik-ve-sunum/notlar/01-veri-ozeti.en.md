If an experiment record has the settings and the seed but not the data, it
is incomplete: if someone fixes a row in the CSV file, the same code with the
same seed gives a different result and the record does not show it. The
solution is to record a **summary** of the data (a hash): a short text
computed from the data's bytes that changes when even one byte of the data
changes.

```python
import hashlib
import numpy as np
from dl_data import make_table


def data_hash(array):
    return hashlib.sha256(np.ascontiguousarray(array).tobytes()).hexdigest()


a, _ = make_table(600, seed=7)
b, _ = make_table(600, seed=7)
c, _ = make_table(600, seed=8)
print(len(data_hash(a)), data_hash(a) == data_hash(b), data_hash(a) == data_hash(c))
changed = a.copy()
changed[0, 0] += 0.001
print(data_hash(a) == data_hash(changed))
```

```text
64 True False
False
```

- A SHA-256 hash is 64 hexadecimal characters. The same data gives the same
  hash; data made with a different seed gives a different one.
- Changing a single number in the 600 × 6 table by a thousandth changed the
  hash completely.
- `np.ascontiguousarray`: the order of the bytes in memory can depend on how
  the array was sliced; take an orderly copy first.

The record usually stores the first 12 characters of the hash
(`data_hash(a)[:12]`); that is enough for comparison. The hash recognises only
**the same bytes**: if the same numbers are saved as `float64`, or the order
of the columns changes, the hash changes too. That is a feature: the model
will see that difference as well.

A full record looks roughly like this: settings, seed, data hash, the git
version of the code (`git rev-parse HEAD`), library versions, results, date.
A JSON of a few lines answers, months later, the question "where did this
number come from".
