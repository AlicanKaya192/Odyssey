`revenue_by_title(sales, products)` should match the sales (`[product_id,
qty]`, `product_id` a number) to the products (`[id, title, price]`, `id`
**text**). First turn `id` into `int`, then merge with
`left_on="product_id", right_on="id"`. Each row's revenue is `qty * price`;
total it by product title and return `{title: revenue}`. **Do not write a
loop.**

**Expected output:**

```
{'cup': 20.0, 'pen': 10.0}
```
