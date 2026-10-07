This Dockerfile works today, but because of `latest` it may be built with a
different Python version tomorrow.

**What to do:** change the `FROM` line so it uses the pinned
`python:3.13-slim` image. Odyssey will build and run the image.

**Expected output:**

```
pinned and ready
```
