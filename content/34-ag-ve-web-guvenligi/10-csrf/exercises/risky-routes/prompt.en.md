`routes` are endpoints, each `[method, path, changes_state]`.
`risky_routes(routes)` should return, in list order, the paths of the
endpoints that change state although their method is `GET` or `HEAD`.

**Expected output:**

```
['/delete-account', '/ping']
```
