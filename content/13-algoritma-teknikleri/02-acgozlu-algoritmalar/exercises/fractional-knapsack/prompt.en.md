Write the function `fractional_knapsack(items, capacity)`: `items` is a list of
`[value, weight]` pairs; items can be split. It returns the largest total
value that can be carried, **rounded to 2 decimals**.

Sort by value per kilo (`value / weight`) from largest to smallest; take as
much as fits, and from the last item take a piece as large as the space left.

**Expected output:**

```
240.0
12.33
```
