We use three of the section's tools at once.

Bring back the products that satisfy **all three**:

- the category is `Accessory` or `Display`,
- the price is between 200 and 2000 (both ends included),
- `supplier_code` is **not empty**.

Columns: `name`, `category`, `price`. Sort from expensive to cheap.

```
name        category   price 
----------  ---------  ------
Microphone  Accessory  1320.0
Webcam      Accessory  1150.0
...
```

The result should be four rows. If you got five you most likely skipped
the last condition: there is a product whose price and category match but
whose supplier is not recorded.
