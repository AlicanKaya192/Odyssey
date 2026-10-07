This Dockerfile works, but even if one letter in `main.py` changes, the
packages are installed from scratch.

**What to do:** fix the order: first copy only `requirements.txt` and install
the packages, then copy the rest of the code.

**Expected output:**

```
ready on Python 3.13
```
