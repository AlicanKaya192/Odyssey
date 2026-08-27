Python has three separate division operators and all three give something
different. In this exercise you will see all three on the same pair of numbers.

```python
a = 17
b = 5
```

Create three variables:

| Variable | Operator | What it does |
|---|---|---|
| `exact` | `/` | True division, the result has a decimal part |
| `whole` | `//` | The whole part of the division, the decimals are dropped |
| `remainder` | `%` | The remainder |

Print all three, one under the other. Expected output:

```
3.4
3
2
```

> The `/` operator **always** gives a decimal result, even when the answer is a
> whole number: `10 / 2` is `5.0`, not `5`.
