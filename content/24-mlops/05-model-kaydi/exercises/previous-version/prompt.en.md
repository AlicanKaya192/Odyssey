The alias history is a list: every element is `[alias, version]`, from oldest to newest. Write the function `previous_version(history, alias)`: for a rollback, return the last **different** version that alias pointed at **before its current version**.

- Look only at that alias's rows.
- The current version is the version on that alias's last row.
- Going backwards, find the first version different from the current one.
- If there is no such version, `None`.

**Expected output:**

```
1
2
None
```
