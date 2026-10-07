In an out-of-order stream, count per-minute windows with a 30-second
watermark and compare them with the right counts.

**What to do:**

1. The right counts: with `payments(5_000)` (the stream in order), count the
   payments of each minute (`ts // 60 * 60`) in a dictionary.
2. With `payments(5_000, late=True)` the same payments arrive out of order.
   Count the open windows; keep the newest `ts` seen; the watermark is
   `newest - 30`.
3. If a payment arrives whose window the watermark has passed
   (`start + 60 <= newest - 30`), do not count it; increase `dropped`.
4. When the watermark passes a window's end, move the window into the
   `results` dictionary. When the stream ends, move the ones still open too.
5. Print: the number of lost payments, the number of windows counted short
   (those whose count in `results` differs from the right one), and whether
   the total of the counts in `results` plus `dropped` is 5000.

**Expected output:**

```
197
91
True
```
