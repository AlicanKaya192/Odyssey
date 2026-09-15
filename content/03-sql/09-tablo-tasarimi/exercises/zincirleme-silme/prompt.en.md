Create an `order_notes` table that keeps notes on orders. When an order
is deleted, its notes should be deleted **automatically**.

| Column | Type | Rule |
|---|---|---|
| `id` | `INT` | counts up by itself, primary key |
| `order_id` | `INT` | cannot be empty, linked to `orders.id` |
| `note` | `NVARCHAR(200)` | cannot be empty |

A note without its order means nothing, so here a cascading delete is
right rather than the link's default behaviour ("do not delete a parent
that has children").

The check also tries the link itself: adding a note to an order that does
not exist must be refused. Then it adds notes to two orders, deletes one
of the orders, and expects only the other order's note to remain.
