Create a `parts` table with its rules written into it.

| Column | Type | Rule |
|---|---|---|
| `id` | `INT` | primary key |
| `sku` | `NVARCHAR(20)` | cannot be empty, no two parts alike |
| `price` | `DECIMAL(10,2)` | cannot be empty, **above zero** |

Only create the table; do not add rows.

The check **tries the rules itself**: it adds a valid part, then tries to
add a second part with the same `sku`, a part with a negative price and a
part priced at zero. The first must be accepted and the other three
refused.

When the rule lives in the table rather than in an application's code,
every program that writes to the table has to obey it.
