In the lesson we used `zlib.crc32` for MinHash instead of Python's built-in
`hash()` function. The reason: Python computes the hash of a string
**differently in every run**. Let us run the same line in two separate
Python processes:

```python
import os
import subprocess
import sys
import zlib

env = {k: v for k, v in os.environ.items() if k != "PYTHONHASHSEED"}
code = 'print(hash("strap"))'
runs = [subprocess.run([sys.executable, "-c", code], capture_output=True,
                       text=True, env=env).stdout.strip() for _ in range(2)]
print(runs[0] == runs[1])
print(zlib.crc32(b"strap"), zlib.crc32(b"strap"))
```

```text
False
3885747501 3885747501
```

- The two processes gave different numbers for "strap". Python does this on
  purpose: if hashes were predictable, a malicious user could send thousands
  of keys that fall into the same bucket of a dictionary and slow the program
  down. A random seed prevents this.
- Within one process `hash()` is consistent; that is why dictionaries and
  sets work without problems. But if you **save** signatures and compare them
  another day, on another computer, the numbers must be the same everywhere.
- `zlib.crc32` gives the same number on every machine, in every run. Real
  systems use faster hashes with better distributions, such as MurmurHash or
  xxHash; the idea is the same.

You can fix Python's seed with the `PYTHONHASHSEED` environment variable, but
it affects every dictionary in the process and is very easy to forget. If
you need a lasting number, use a stable hash function.
