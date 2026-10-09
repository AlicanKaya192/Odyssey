Write the function `reservoir_sample(stream, k, seed)`: it returns an
equal-probability sample of `k` items from the stream; all of them if the
stream is shorter than `k`. The generator is `rng = random.Random(seed)`.

Add the first `k` items; then at item `i` (from 0) `j = rng.randint(0, i)`, and
if `j < k` the new item replaces `sample[j]`. Do not turn the stream into a
list: one pass.

**Expected output:**

```
[37, 55, 2, 97, 77]
[0, 1, 2]
['e', 'b', 'j']
```
