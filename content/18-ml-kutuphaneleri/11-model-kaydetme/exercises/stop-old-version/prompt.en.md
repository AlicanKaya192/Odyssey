`stop_old_version(version)` prepares a file that looks saved in version `version`
and loads it. During loading `InconsistentVersionWarning` should be **turned
into an error** (`simplefilter("error", ...)` inside
`warnings.catch_warnings()`), so that the `except` branch runs and returns
`[model_name, old_version]`. In the starter code the warning stays a warning
and loading carries on.

**Expected output:**

```
['LogisticRegression', '1.2.2']
```
