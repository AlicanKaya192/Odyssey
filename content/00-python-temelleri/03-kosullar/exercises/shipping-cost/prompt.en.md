A courier's price table:

| Weight | Price |
|---|---|
| up to 2 kg (2 included) | 30 |
| over 2 kg, up to 5 kg (5 included) | 45 |
| over 5 kg, up to 10 kg (10 included) | 70 |
| over 10 kg | 70 + 8 for every kg over 10 |

Members get **20% off**, but only when the price is **50 or more**.

```python
weight = 10
is_member = True
```

Calculate the price in the variable `cost` and print it:

```
Cost: 56.0
```

There are two steps: first find the price from the weight, **then** apply
the discount. The discount decision looks at the price found in the first
step.

> Watch out: the limits are exactly as written in the table. `10` kg falls
> in the third row, 70; the difference between `<` and `<=` changes the
> result here. After the discount the price is a decimal number.
