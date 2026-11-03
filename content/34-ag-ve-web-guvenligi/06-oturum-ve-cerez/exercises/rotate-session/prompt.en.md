`sessions` is an ID → user dictionary. `rotate(sessions, old_id,
new_id)` should return a **new** dictionary: the old ID deleted and its
user moved to the new ID. If `old_id` is not in the dictionary, return an
unchanged copy. Do not change the dictionary you are given. The starter
code leaves the old ID behind.

**Expected output:**

```
[('new456', 'ada'), ('x9', 'bob')]
True
```
