Split the first 2000 payments into five-minute (300-second) tumbling
windows; print each window's result when it closes.

**What to do:**

1. The start of a window: `event["ts"] // 300 * 300`.
2. Keep only the open window's start, number of payments and total amount.
3. When the first payment of a new window arrives, print the old one:
   `closed start count total` (total with two decimals).
4. When the stream ends, print the last window that is still open as
   `open start count total`.

**Expected output:**

```
closed 0 207 23060.11
closed 300 212 23432.8
closed 600 215 25068.68
closed 900 208 26918.22
closed 1200 212 24829.54
closed 1500 215 26446.96
closed 1800 225 26956.03
closed 2100 213 25240.26
closed 2400 197 26540.65
open 2700 96 10348.27
```
