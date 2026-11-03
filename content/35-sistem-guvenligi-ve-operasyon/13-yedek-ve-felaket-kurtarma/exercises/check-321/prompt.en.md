Each copy is a dict: `media` and `offsite` (is it outside).
`check_321(copies)` should return the names of the failing rules in this
order: `"copies"` if there are not at least 3 copies, `"media"` if there
are not at least 2 different media, `"offsite"` if there is not at least 1
copy outside. If all hold, an empty list.

**Expected output:**

```
[]
['copies', 'media', 'offsite']
```
