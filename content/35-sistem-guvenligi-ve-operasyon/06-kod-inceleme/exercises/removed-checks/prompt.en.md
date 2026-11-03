`removed_checks(diff, keywords)` should return, of the **removed** lines
in a diff (starting with `-` but not with `---`), those containing one of
the `keywords`: with the leading `-` dropped and `strip()`-ed, in the
order of the diff. The starter code looks at the added lines.

**Expected output:**

```
check_owner(user, data)
verify_token(user)
```
