Write the function `parse_title(title)`. If the title follows this rule it should return the list `[kind, scope, breaking, summary]`, otherwise `None`:

- Kind: `feat`, `fix`, `docs`, `test` or `chore`.
- An optional scope in parentheses, lowercase letters and hyphens: `(login)`. If there is none, the scope is `None`.
- An optional `!`: if it is there breaking is `True`, otherwise `False`.
- Then `: ` (a colon and a space) and a summary that does not start with a space.

In a regular expression the groups are taken with `match.groups()`; an optional group that did not match comes as `None`.

**Expected output:**

```
['feat', 'login', False, 'remember me']
['fix', None, True, 'drop the old api']
['docs', None, False, 'explain the setup']
None
None
```
