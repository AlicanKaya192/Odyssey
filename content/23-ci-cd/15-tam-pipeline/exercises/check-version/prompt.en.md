Write the function `check_version(tag, pyproject)`. `tag` is the tag name (`"v0.3.0"`), `pyproject` is the text of the `pyproject.toml` file.

- If the tag does not start with `v`: return something like `"tag 0.3.0 must start with v"`.
- Read the version from the text: `tomllib.loads(pyproject)["project"]["version"]`.
- If the tag is not `"v" + version`: something like `"tag v0.3.1 does not match version 0.3.0"`.
- If it matches: `"ok"`.

**Expected output:**

```
ok
tag v0.3.1 does not match version 0.3.0
tag 0.3.0 must start with v
```
