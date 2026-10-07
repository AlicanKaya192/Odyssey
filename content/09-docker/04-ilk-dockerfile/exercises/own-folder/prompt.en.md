This Dockerfile works, but `app.py` goes to the image's root folder (`/`)
and gets mixed among Linux's own folders.

**What to do:** before the `COPY` line, add the instruction that makes `/srv`
the working folder. `app.py` prints the folder it is in.

**Expected output:**

```
working in /srv
```
