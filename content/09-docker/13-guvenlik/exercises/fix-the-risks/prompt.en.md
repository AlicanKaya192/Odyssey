This Dockerfile has three security problems:

1. The base image's version is not pinned (`latest`).
2. A password is baked into the image with `ENV`.
3. The program explicitly runs as root.

**What to do:** fix all three: `python:3.13-slim`, remove the password line
(the password will be given when running), create the `app` user with
`useradd` and switch to it.

**Expected output** (Odyssey runs it without giving the password):

```
user: app
password set: False
```
