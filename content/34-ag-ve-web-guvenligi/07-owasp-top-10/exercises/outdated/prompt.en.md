`installed` holds the installed versions and `minimum` the lowest safe
versions (in the form `"1.10.0"`). `outdated(installed, minimum)` should
return, in alphabetical order, the names of the components whose
installed version is **less** than the minimum; a component not in
`minimum` is skipped. The starter code compares versions as text.

**Expected output:**

```
['parser']
```
