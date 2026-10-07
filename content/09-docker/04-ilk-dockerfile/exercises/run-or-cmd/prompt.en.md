This Dockerfile runs the program with `RUN`. The program runs once while the
image is built and ends; when the container starts, nothing happens (this
image's default command is interactive Python, which closes at once).

**What to do:** change the last line so the program runs **when the
container runs** (bracketed form).

**Expected output** (what the container prints):

```
the clock is ticking
```
