Whatever version the Python on your computer is, the Python inside the
container is the version the image brings.

**What to do:** write a Dockerfile that starts from the `python:3.13-slim`
image and runs the command `python --version` when it runs.

**Expected output** (the last digit may vary with the image):

```
Python 3.13.x
```
