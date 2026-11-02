`keyspace_years(bits, rate)` should compute how many years it takes
someone making `rate` guesses per second to try every `bits`-bit key. A
year is `365 * 24 * 3600` seconds. Return the result as **text** in the
form `f"{years:.2e}"`.

**Expected output:**

```
40 3.49e-08
64 5.85e-01
128 1.08e+19
```
