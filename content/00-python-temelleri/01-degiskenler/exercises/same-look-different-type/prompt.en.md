You have two variables:

```python
x = "5"
y = 5
```

One is text, the other a number. Using only `x` and `y` (and `int()` /
`str()` where needed), create five variables:

| Variable | Value | Type | How |
|---|---|---|---|
| `r1` | `"55"` | text | with `x` only |
| `r2` | `10` | number | with `y` only |
| `r3` | `"555"` | text | with `x` only |
| `r4` | `10` | number | `x` and `y` together |
| `r5` | `"55"` | text | `y` and `x` together |

Then print each of them with its type (`print(r1, type(r1))`):

```
55 <class 'str'>
10 <class 'int'>
555 <class 'str'>
10 <class 'int'>
55 <class 'str'>
```

`r1` and `r5` look the same on screen, and so do `r2` and `r4`. But they
are made in different ways. That is the point: `+` adds numbers, joins
texts end to end, and does not combine text with a number at all.

> Watch out: do not type the results yourself (like `r1 = "55"`). Make
> each one by doing something with `x` and `y`.
