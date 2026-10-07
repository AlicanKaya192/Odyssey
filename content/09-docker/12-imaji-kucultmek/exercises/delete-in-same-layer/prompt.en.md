This image creates a 30 MB temporary file, takes its checksum and deletes
the file; but because it uses three separate `RUN` lines, the file stays in
the first layer and the image is ~73 MB.

**What to do:** join the three `RUN` lines into **one** `RUN` with `&&` (you
can split the long line with `\`). Odyssey will check that the image is
**smaller than 20 MB**.

**Expected output:**

```
checksum ready
9
```
