Remove order 1006 **completely**: the order itself and the items
belonging to it.

Nine orders and nineteen order items should remain.

You will write two commands. **The order matters: items first, then the
order.**

If the order goes and its items stay, you are left with rows attached to
no order at all. The `1006` in `order_items` now points at something that
does not exist, and nobody ever notices those rows again — because the
only way to find them is to go looking for an order that is not there.

The links in this database are **not declared**, so the server allows the
reverse order too: delete them the wrong way round and you get no error.
In the next section you will learn to declare those links, and see the
server enforce this order by itself.
