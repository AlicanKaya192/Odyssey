Add a foreign key that links the `order_items.order_id` column to
`orders.id`.

The table already exists and holds data — do not rebuild it, add the link
with `ALTER TABLE`.

In the previous section you saw that the order matters when deleting
order 1006 together with its items, but that the server allowed the
reverse order as well: the link was not declared. Adding the link changes
that.

The check looks at two things: whether the link goes from the right
column to the right table, and whether the server **refuses** when it
tries to delete order 1006.
