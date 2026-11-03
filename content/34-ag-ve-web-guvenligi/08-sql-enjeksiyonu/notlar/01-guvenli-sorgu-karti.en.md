## The rule

**Every** value goes as a parameter; nothing that comes from the user is
ever pasted into the query text.

## Python patterns (sqlite3)

| Job | Right way |
|---|---|
| One value | `conn.execute("... WHERE owner = ?", (owner,))` |
| Several values | `conn.execute("... WHERE a = ? AND b = ?", (a, b))` |
| Inserting many rows | `conn.executemany("INSERT ... VALUES (?, ?)", rows)` |
| An `IN` list | Make the placeholders with `", ".join("?" * len(items))`, give the values separately |
| Column name | Map to an allow-list dictionary: `SORTABLE.get(sort, "name")` |
| `LIKE` search | Escape `\`, then `%` and `_`; `... LIKE ? ESCAPE '\'` |

## Wrong ways

All of them are the same hole:

- `f"... WHERE owner = '{owner}'"`
- `"... WHERE owner = '" + owner + "'"`
- `"... WHERE owner = '%s'" % owner`
- `"... WHERE owner = '{}'".format(owner)`

## Why is filtering not enough?

The "I will delete the quotes" or "I will write `''` instead of `'`"
approach needs you to know every context, every database's rules and every
character encoding correctly. A parameter leaves this knowledge to the
database driver; it leaves no way to turn the value into code.

## Layers that limit the damage

- The application's database user has the least privilege (the reading part
  only reads, no permission to drop tables).
- The database error message is not shown to the user; it goes into the
  log.
- Input is first turned into the expected type and form (number, date,
  e-mail).
- Passwords are stored hashed; a leaked table holds no plain passwords.
