The `name` column in `employees` holds first and last name together:
`Ada Kilic`, `Bora Yilmaz`... Split them into separate columns.

Columns: `id`, `first_name`, `last_name`. Sort by `id`.

```
id  first_name  last_name
--  ----------  ---------
1   Ada         Kilic
2   Bora        Yilmaz
...
```

The names are of different lengths, so you cannot write a fixed number.
First find **where** the space is, then take the part before it and the
part after it.

The space itself must not appear on either side — the check counts a name
with a leading or trailing space as wrong.
