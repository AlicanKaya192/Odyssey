`apply_update(profile, body)` should return a **copy** of the profile;
only the fields in `ALLOWED` from the body are written to the copy. The
original `profile` must not change. The starter code writes the whole
body.

**Expected output:**

```
{'name': 'Ada', 'role': 'user', 'bio': 'hi'}
{'name': 'Ada', 'role': 'user'}
```
