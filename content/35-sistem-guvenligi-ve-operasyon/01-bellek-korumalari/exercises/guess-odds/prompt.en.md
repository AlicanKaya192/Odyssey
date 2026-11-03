Write two functions:

- `guess_odds(bits)`: the text `"1 in <number>"`; the number is
  `2 ** bits`, with a thousands separator (`f"{n:,}"`):
  `guess_odds(16)` → `"1 in 65,536"`.
- `average_tries(bits)`: the average number of tries, half the possible
  addresses: `2 ** (bits - 1)`.

**Expected output:**

```
8: 1 in 256
  average 128
16: 1 in 65,536
  average 32768
28: 1 in 268,435,456
  average 134217728
```
