A Dockerfile's steps are a list of `[command, files it looks at, seconds]`. Write the function `total_seconds(steps, builds)`: `builds` is the list of builds done one after another, each one the list of files changed in that build. The cache is kept between builds. Return the total time of all builds.

- **In the first build** the cache is empty: all steps run.
- In the later ones: if one of the files a step looks at changed, **that step and every step after it** run; the earlier ones come from the cache (0 seconds).

Two sets overlap: if `set(a) & set(b)` is not empty, they have a common item.

**Expected output:**

```
good order: 132
bad order: 310
```
