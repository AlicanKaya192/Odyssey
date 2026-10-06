You have a four-digit number:

```python
n = 4827
```

Calculate two things:

- `digit_sum`: the sum of its digits (`4 + 8 + 2 + 7`)
- `reversed_number`: the number with its digits in reverse order, **as a
  number** (`7284`)

```
Sum of digits: 21
Reversed: 7284
```

Rule: no turning the number into text (`str()` is not allowed). Arithmetic
only: `//` and `%`.

Two useful observations:

- `n % 10` gives the **last** digit of the number (`4827 % 10` → `7`).
- `n // 10` **drops** the last digit (`4827 // 10` → `482`).

Combine the two to get each digit out one by one. When you build the
reversed number, think about which place (thousands, hundreds…) each
digit goes to.

> Watch out: even though `reversed_number` shows as `7284`, it must not be
> text; the check looks at its type too.
