`copies` are all the copies of the data (the original included): each
is a dictionary with the fields `media`, `offsite`, `offline`.

`backup_problems(copies)` should return the missing items as a list in this
order; an empty list if nothing is missing:

1. `"need-3-copies"`: fewer than 3 copies,
2. `"need-2-media"`: fewer than 2 **different** media (`media`),
3. `"need-offsite"`: no copy somewhere else (`offsite`),
4. `"need-offline"`: no offline (`offline`) copy.

**Expected output:**

```
need-3-copies
need-2-media
need-offsite
need-offline
good: 0 problems
```
