`attach_names(orders, customers)` should add the customer names (`[customer,
name]`) to the orders (`[order, customer, amount]`) and return the names as a
list in order sequence. An order whose customer is not found gets the name
`"?"` (`fillna("?")`). The starter code merges with the default `inner`; an
order vanishes.

**Expected output:**

```
['Ada', 'Can', 'Ada', '?']
```
