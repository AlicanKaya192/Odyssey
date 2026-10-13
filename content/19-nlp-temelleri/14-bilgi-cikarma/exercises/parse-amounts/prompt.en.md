`parse_amounts(text)` should find the amounts starting with `$` and return them
as numbers (`float`, 2 places). An amount may or may not have a thousands
separator (`1,200`) and cents (`.49`).

**Expected output:**

```
[1200.0, 5.0, 12.49]
[]
```
