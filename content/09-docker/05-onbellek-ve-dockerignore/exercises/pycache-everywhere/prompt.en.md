There is a `__pycache__` inside the `shapes` folder: an old cache from your
computer that must not enter the image.

**What to do:** write a single pattern in `.dockerignore` that leaves out
`__pycache__` **in every folder**. If you write only `__pycache__`, the
pattern only catches the folder at the root; `shapes/__pycache__` enters the
image.

**Expected output:**

```
area: 49
```
