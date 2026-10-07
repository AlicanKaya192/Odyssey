The counter writes to `/data` and the image runs as the `app` user. When an
empty volume is first mounted, it takes the owner of the folder in the image;
if the folder belongs to root, `app` cannot write.

**What to do:** before the `VOLUME` line, create `/data` and make `app` its
owner with a single `RUN`.

Odyssey will run two separate containers with the same volume.

**Expected outputs:**

```
count: 1
count: 2
```
