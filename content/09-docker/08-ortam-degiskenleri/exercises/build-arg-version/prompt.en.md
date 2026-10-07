`ARG` is valid only during the build; if it is needed while running too, it
is passed into `ENV`.

**What to do:**

1. Define an `ARG` called `VERSION` with the default `1.0`.
2. Pass its value to run time with `ENV APP_VERSION=$VERSION`.

Odyssey will build the image twice: with no argument and with
`--build-arg VERSION=2.4`.

**Expected outputs:**

```
version 1.0
version 2.4
```
