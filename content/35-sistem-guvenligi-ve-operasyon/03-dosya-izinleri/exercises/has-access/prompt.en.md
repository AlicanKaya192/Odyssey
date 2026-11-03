A file is a dict: `owner`, `group`, `mode`. `has_access(file, user,
groups, action)` (`action`: `"r"`, `"w"` or `"x"`) should return whether
access is allowed. Choose **a single class**: the owner bits if the user is
the owner, otherwise the group bits if the file's group is in `groups`,
otherwise the others. The starter code says `True` when it sees the
permission in any of the three classes; that is wrong.

**Expected output:**

```
False
True
True
False
False
```
