The first stage produces `/out/primes.json` with `make_data.py`. The final
image should have the data file but not the script that produced it.

**What to do:** in the last stage:

1. Copy **only** `/out/primes.json` from the `build` stage to the working
   folder.
2. Copy `show.py`.

Odyssey will check that `make_data.py` is not in the final image.

**Expected output:**

```
15 primes, the largest is 47
```
