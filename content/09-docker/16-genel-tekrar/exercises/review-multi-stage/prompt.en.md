`report.py` produces a report. Showing the report does not need Python; the
final image should contain only the report file.

**What to do:**

1. A first stage called `build` (`python:3.13-slim`): working folder
   `/src`, copy `report.py` and produce the report with
   `RUN python report.py > report.txt`.
2. A second stage (`alpine:3.22`): copy `/src/report.txt` from the first
   stage as `/report.txt`; `CMD ["cat", "/report.txt"]`.

The final image must be smaller than 20 MB.

**Expected output:**

```
apples    12
pears      7
plums     30
total     49
```
