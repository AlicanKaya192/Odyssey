The file `orders.json` has been placed next to your code: a shop's orders,
each order with a list of items inside. Its structure:

- `data["shop"]`: the shop's name
- `data["orders"]`: the list of orders
- each order has `customer` and `items` (the list of items)
- each item has `name`, `price` and `qty` (quantity)

**What to do:**

1. Read the file into a variable called `data` with `json.load`.
2. First print the shop's name.
3. For each order, work out the total of `price * qty` over its items;
   print the customer's name and the total, and put it into a dictionary
   called `totals` (key the customer, value the total).
4. At the very end print the total of all orders.

**Expected output:**

```text
Book Corner
Ada 22
Alan 30
Grace 30
82
```

Two loops, one inside the other: the outer one goes through the orders, the
inner one through that order's items.
