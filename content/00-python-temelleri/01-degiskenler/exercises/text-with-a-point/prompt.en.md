There is a price, as if read from a file, but as **text**:

```python
value = "12.75"
```

Create three variables:

- `whole`: the whole part of the number, as an **integer** (`12`)
- `doubled`: twice the price, as a **decimal number** (`25.5`)
- `label`: `whole` joined with the text `" pieces"` (`"12 pieces"`)

and print these:

```
12
25.5
12 pieces
```

On your first try you will probably write `int(value)` and get an error.
Why? `int()` can only turn text made of digits into an integer; it cannot
convert text with a dot in it. You need to turn the text into a decimal
number (`float`) first, and then that into an integer.

> Watch out: `int()` does **not round** a decimal number, it cuts it off:
> `int(12.75)` gives `12`, not `13`.
