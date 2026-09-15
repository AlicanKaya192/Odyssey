For each employee, write the **chain of command** from the top down to
them as a single piece of text. Separate the names with `' > '` (space,
greater-than, space).

Columns: `id`, `path`. Sort by `path`.

```
id  path
--  -------------------------------------
1   Ada Kilic
2   Ada Kilic > Bora Yilmaz
3   Ada Kilic > Bora Yilmaz > Ceren Aksoy
4   Ada Kilic > Bora Yilmaz > Deniz Kaya
5   Ada Kilic > Emre Sahin
6   Ada Kilic > Emre Sahin > Fulya Demir
```

The same as the level exercise, with text instead of a number. You are
likely to run into an error message — `Types don't match between the
anchor and the recursive part`. The message says what does not match:
the type of the column in the two parts.
