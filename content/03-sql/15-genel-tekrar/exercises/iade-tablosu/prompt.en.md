Create a table that holds returns and add two returns.

| Column | Type | Rule |
|---|---|---|
| `id` | `INT` | increasing by itself, primary key |
| `order_id` | `INT` | cannot be empty, linked to the `orders` table |
| `reason` | `NVARCHAR(100)` | cannot be empty |
| `quantity` | `INT` | cannot be empty, greater than 0 |

To add:

| order_id | reason | quantity |
|---|---|---|
| 1005 | `Damaged screen` | 1 |
| 1009 | `Wrong item` | 1 |

The check looks at four things: the columns and their types, the link
from `order_id` to `orders`, the two added rows, and whether the rules
work — adding a return for an order that does not exist (9999) and one
with 0 items must be **refused**.

This schema has no foreign keys at all: when customer 1 was deleted, 3
of their orders were left orphaned (measured). Your table should prevent
that for itself. Sections: table design (09), adding data (08).
