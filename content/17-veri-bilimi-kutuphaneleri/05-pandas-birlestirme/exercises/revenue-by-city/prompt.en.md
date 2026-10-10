`revenue_by_city(orders, cities)` should match each order (`[order, customer,
amount]`) to the customer's city (`[customer, city]`) and return the revenue
per city as `{city: total}`. A customer can appear more than once in the city
table; the **first** record counts (`drop_duplicates("customer")`). Pass
`validate="many_to_one"` when merging. In the starter code the revenue
doubles. **Do not write a loop.**

**Expected output:**

```
{'Bursa': 90, 'Izmir': 360}
```
