Write the function `top_products(products, n)`: return the names of the
`n` best-selling products from the `{"name": ..., "sales": ...}`
dictionaries, from the highest sales down. Without sorting the whole list:
`heapq.nlargest(n, products, key=itemgetter("sales"))`.

**Expected output:**

```
['book', 'pen']
```
