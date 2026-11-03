`digest` is ready. The signed text is `"app " + version`.
`check_update(version, signature, e, n, installed)` should check the
signature first (`"bad signature"`), then return `"downgrade"` if the
version is not newer than `installed`, and `"install"` if it is. The
starter code compares the versions as text: `"2.10.0"` is smaller than
`"2.9.0"` as text. Split the version at the dots into a list of numbers.

**Expected output:**

```
install
downgrade
bad signature
```
