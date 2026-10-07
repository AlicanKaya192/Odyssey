`writer.py` writes to the file `/app/output.txt`; the image runs as the
`app` user and the program fails with this error:

```text
PermissionError: [Errno 13] Permission denied: '/app/output.txt'
```

`WORKDIR` created the `/app` folder as root.

**What to do:** before the `USER app` line, make `app` the owner of `/app`
(`chown`). Do not go back to root, do not give `777`.

**Expected output:**

```
saved 3 lines as app
```
