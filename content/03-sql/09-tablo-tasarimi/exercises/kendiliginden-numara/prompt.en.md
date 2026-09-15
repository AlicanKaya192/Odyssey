Create a table that numbers its own rows and writes `open` when no
status is given; then add two rows.

| Column | Type | Rule |
|---|---|---|
| `id` | `INT` | starts at 1 and counts up by itself, primary key |
| `title` | `NVARCHAR(60)` | cannot be empty |
| `status` | `NVARCHAR(20)` | cannot be empty, `'open'` when not given |

For the two rows give only the title: `Printer is offline` and
`VPN is slow`.

That is the real subject: `id` and `status` are **not written** in the
`INSERT`. The server hands out the number and the default fills in the
status. The check looks at the rows and also at whether the table really
does both jobs itself.
