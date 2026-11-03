`installed` is package → installed version; each item in `advisories` is
`[package, fixed_version]`. `patch_plan(installed, advisories)` should
return a `"<package>: <installed> -> <fixed>"` line for every installed
package whose version is **older** than the fixed one, in alphabetical
order by package. A package that is not installed is skipped. Compare the
versions as tuples of numbers.

**Expected output:**

```
fetcher: 8.9.0 -> 8.10.0
tlslib: 3.0.9 -> 3.0.13
```
