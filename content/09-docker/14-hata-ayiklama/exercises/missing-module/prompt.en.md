The image builds but the container fails at once. `docker logs`:

```text
ModuleNotFoundError: No module named 'helpers'
```

**What to do:** copy the file missing from the image too. (To give several
files in one `COPY`, the destination must end with `./`.)

**Expected output:**

```
hi Ada
```
