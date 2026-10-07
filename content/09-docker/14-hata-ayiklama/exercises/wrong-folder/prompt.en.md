The container ends with this error:

```text
python: can't open file '/app/app.py': [Errno 2] No such file or directory
```

`docker run --rm --entrypoint ls app -la /app` shows an empty folder.

**What to do:** make `app.py` get copied to where the program looks for it
(the working folder).

**Expected output:**

```
debugged and running
```
