Each advisory in `advisories` is `[package, introduced, fixed, id]`.
`affected(installed, advisories)` should return, in alphabetical order, a
`"<package> <version>: <id>"` line for every package whose installed
version lies in `introduced <= version < fixed`. A package that is not
installed is skipped. Compare versions as tuples of numbers.

**Expected output:**

```
pool 0.4.2: ADV-3
web 2.3.1: ADV-1
```
