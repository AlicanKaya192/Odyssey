Write the function `image_tags(image, ref, sha)`; it should return the list of full names the image gets, in this order:

- Always `image:` + the first 7 characters of the SHA.
- If `ref` is `"refs/heads/main"`, `image:latest`.
- If `ref` starts with `"refs/tags/v"`: the version after the `v` (`image:2.3.1`). If the version has **no** letters, also the short forms: `image:2.3` and `image:2`. A pre-release (`3.0.0rc1`) gets no short forms.

`any(char.isalpha() for char in version)` tells you whether a text has a letter.

**Expected output:**

```
refs/heads/main
  ghcr.io/ada/shop:9c1e4b7
  ghcr.io/ada/shop:latest
refs/heads/cart
  ghcr.io/ada/shop:9c1e4b7
refs/tags/v2.3.1
  ghcr.io/ada/shop:9c1e4b7
  ghcr.io/ada/shop:2.3.1
  ghcr.io/ada/shop:2.3
  ghcr.io/ada/shop:2
refs/tags/v3.0.0rc1
  ghcr.io/ada/shop:9c1e4b7
  ghcr.io/ada/shop:3.0.0rc1
```
