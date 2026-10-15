Write the function `next_version(current, commits)`. `current` is the current version (`"1.4.2"`), `commits` are the commit messages since the last release.

- If a message's head (the part before `:`) ends with `!`, or the message contains `BREAKING CHANGE`: MAJOR goes up (`2.0.0`).
- Otherwise, if the kind is `feat` (it can have a scope: `feat(api)`): MINOR goes up (`1.5.0`).
- Otherwise, if the kind is `fix`: PATCH goes up (`1.4.3`).
- The biggest bump wins; the parts to the right of the bumped one reset. If there is none, `None`.

**Expected output:**

```
1.4.3
1.5.0
2.0.0
None
```
