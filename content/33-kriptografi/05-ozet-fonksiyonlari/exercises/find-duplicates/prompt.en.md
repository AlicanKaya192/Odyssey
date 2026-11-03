`items` is name → content (text). `find_duplicates(items)` should
return the groups that share the **same** content (the same SHA-256) and
have more than one name: each group is the alphabetical list of names that
share that content. Groups are in alphabetical order by their first name;
content with a single name is not listed.

**Expected output:**

```
['w', 'y']
['x', 'z']
```
