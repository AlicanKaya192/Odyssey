A full format specifier is written in this order, and every part is
optional:

```
{value:[fill][align][sign][width][,][.digits][type]}
```

## The common ones

| Syntax | Result | What it does |
|---|---|---|
| `f"{3.14159:.2f}"` | `3.14` | Two decimal places |
| `f"{12.5:.2f}"` | `12.50` | Missing digits filled with zeros |
| `f"{1234567:,}"` | `1,234,567` | Thousands separator |
| `f"{1234567.891:,.2f}"` | `1,234,567.89` | Separator and digits together |
| `f"{0.0725:.1%}"` | `7.2%` | Percentage (multiplies by a hundred) |
| `f"{7:03d}"` | `007` | Pad with zeros |
| `f"{4.2:+.1f}"` | `+4.2` | Show the plus sign |
| `f"{'ada':<8}"` | `ada␣␣␣␣␣` | Align left in eight characters |
| `f"{'ada':>8}"` | `␣␣␣␣␣ada` | Align right |
| `f"{'ada':^8}"` | `␣␣ada␣␣␣` | Centre |
| `f"{'ada':.^8}"` | `..ada...` | Centre, padding with dots |
| `f"{255:x}"` | `ff` | Hexadecimal |
| `f"{255:b}"` | `11111111` | Binary |
| `f"{12345.6789:.2e}"` | `1.23e+04` | Scientific notation |
| `f"{count = }"` | `count = 7` | Name and value, for debugging |

The `␣` in the table means a space; the real output has spaces there.

## Types

<figure class="fig anat">
  <div class="anat-row"><span><code>f</code></span><span>Decimal number. Six digits when you give no count.</span></div>
  <div class="anat-row"><span><code>d</code></span><span>Whole number. Cannot be used with a decimal value.</span></div>
  <div class="anat-row"><span><code>%</code></span><span>Percentage: multiplies by a hundred and adds the sign.</span></div>
  <div class="anat-row"><span><code>e</code></span><span>Scientific notation.</span></div>
  <div class="anat-row"><span><code>s</code></span><span>Text. Usually left out because it is the default.</span></div>
</figure>

## Taking the width from a variable

The column width does not have to be fixed in the code:

```python
width = 12
for name in ["Pencil", "Notebook"]:
    print(f"{name:<{width}}|")
```

```
Pencil      |
Notebook    |
```

Nested braces let you work the width out while the program runs. This is
how you find the longest name and line everything up against it.

## Three common mistakes

1. **Mixing up the order.** `{x:.2f,}` does not work; the separator comes
   before the digits: `{x:,.2f}`.
2. **`d` with a decimal number.** `f"{12.5:d}"` raises an error; use `f`
   for a decimal value, or convert it with `int()`.
3. **Applying the percentage twice.** `{rate * 100:.1%}` turns seven per
   cent into seven hundred. `%` already multiplies.
