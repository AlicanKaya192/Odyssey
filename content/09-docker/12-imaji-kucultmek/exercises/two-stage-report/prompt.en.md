`build_report.py` produces an HTML report; showing the report does not need
Python.

**What to do:** a two-stage Dockerfile:

1. A stage called `build` from `python:3.13-slim`: working folder `/src`,
   copy `build_report.py` and run it with `RUN` (the report is written to
   `/out/index.html`).
2. A last stage from `alpine:3.22`: copy `/out` from the `build` stage to
   `/report`; when the container runs, `cat /report/index.html`.

Odyssey will check that the final image is **smaller than 20 MB** and has no
Python inside.
