The `build` job currently starts at the same time as `lint` and `test`; the package is built even if the tests fail.

`build` should start when `lint` and `test` have **both** finished successfully.
