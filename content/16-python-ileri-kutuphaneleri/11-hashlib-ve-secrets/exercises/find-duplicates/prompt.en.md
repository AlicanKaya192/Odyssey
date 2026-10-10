`duplicates(paths)` should find files with the **same** content: take each
file's SHA-256 digest and group the paths with the same digest. Return only
groups with **more than one** file; each group is a sorted list, and the
groups are sorted by their first element.

**Expected output:**

```
['files/a.txt', 'files/c.txt']
['files/b.txt', 'files/d.txt']
```
