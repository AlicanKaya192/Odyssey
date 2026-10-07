The query string of a request came from the server's log. The same name
appears more than once in it (`tag`).

**What to do:**

1. Turn `query` into a dictionary with `parse_qs`.
2. Put the city and the units into the variables `city` and `units` as
   **plain text** (not lists).
3. Put the **list** of tags into the variable `tags`.
4. Print as below; on the last line the tags are joined with a comma and a
   space.

**Expected output:**

```
Ankara
imperial
3 tags: sea, museum, castle
```

`parse_qs` puts every value in a list: for the city you need the first item
with `[0]`, for the tags the whole list.
