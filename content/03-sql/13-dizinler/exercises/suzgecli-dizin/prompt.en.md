In the `events` table `amount` is only filled in for purchases: it is
empty (`NULL`) on 15,000 of the 20,000 rows. Create an index on `amount`
for queries that search by amount, but let the index hold **only the
rows where `amount` is filled in**.

Measured:

| Index | Space taken by indexes |
|---|---|
| on `amount`, no filter | 408 KB |
| on `amount`, filtered with `amount IS NOT NULL` | **128 KB** |

With the filtered index `WHERE amount > 490` takes 2 reads. Because the
empty rows are not in the index, `WHERE amount IS NULL` cannot use it —
and it has no need to.

The check looks at the index's filter too: the condition has to be on
`amount`.
