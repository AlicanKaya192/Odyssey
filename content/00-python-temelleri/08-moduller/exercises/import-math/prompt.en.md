You have the number `42.25`. You are going to find its square root, its value
rounded down and its value rounded up.

You are not working any of these out yourself — they are already there in the
`math` module.

**What to do:**

1. Bring in the `math` module.
2. Create three variables:

| Variable | What goes in it |
|---|---|
| `root` | The square root of the number |
| `floor_value` | The number rounded down |
| `ceil_value` | The number rounded up |

3. Print the three of them **on separate lines**.

**Expected output:**

```
6.5
42
43
```

The square root comes out as `6.5`, not `6` — `math.sqrt` always returns a
decimal number.
