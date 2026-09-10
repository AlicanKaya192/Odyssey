Add a new supplier to the `suppliers` table.

| Column | Value |
|---|---|
| `code` | `S5` |
| `name` | `Baltic Parts` |
| `city` | `Gdansk` |
| `country` | `Poland` |

This is the first write in the section. Up to here you have only written
`SELECT`; this time a row really will appear in the table.

**Write the column list.** It works without one — the values are handed
out by the table's column order — but that form quietly starts writing to
the wrong place the day a column is added to the table.

Do not worry: the row is rolled back when the run finishes. On your next
attempt `suppliers` has four rows again.
