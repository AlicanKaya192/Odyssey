In the previous section a file written inside a container disappeared when
the container was removed. A file written **during the build**, however, goes
into the image's layer and exists in **every** container started from the
image.

The `RUN` instruction runs a command during the build and saves the result as
a new layer.

**What to do:**

1. With `RUN`, write `made at build time` to the file `/built.txt`.
2. With `CMD`, run `cat /built.txt` when the container runs.

**Expected output:**

```
made at build time
```
