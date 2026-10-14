Write the function `should_run(branch, files, branches, ignored_dirs)` that decides whether the workflow runs for a push:

- `branch` is the push's branch, `files` the list of changed files.
- `branches` are the allowed branches, `ignored_dirs` the ignored **top folders** (like `"docs"`).
- If the branch is not in `branches`: `False`.
- If at least one changed file's top folder is not an ignored one: `True`, otherwise `False`.

A file's top folder is the first part of its path: `"docs/setup.md"` → `"docs"`. For `"README.md"` at the root, the first part is the file itself.

**Expected output:**

```
False
True
True
False
```
