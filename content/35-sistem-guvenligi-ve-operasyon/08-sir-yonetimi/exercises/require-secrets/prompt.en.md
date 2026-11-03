`require_secrets(env, names)` should return, in alphabetical order, the
secrets in `names` that are **missing or empty** in the environment. The
program checks this list at start-up; if it is not empty, it does not
run.

**Expected output:**

```
['API_TOKEN', 'SIGNING_KEY']
[]
```
