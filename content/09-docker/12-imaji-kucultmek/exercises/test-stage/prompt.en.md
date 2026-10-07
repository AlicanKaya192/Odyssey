A test stage is the way to run tests in the Dockerfile without putting them
in the image.

**What to do:** between `base` and `runtime`, add a stage called `test`: it
starts from `base` and runs `python -m unittest`.

Odyssey will do two builds: `--target test` (the tests must pass) and the
default build (the last stage, `runtime`).

**Expected output** (`runtime`):

```
2 + 3 = 5
```
