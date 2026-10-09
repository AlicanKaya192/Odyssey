Write the function `numeric_grad(w)`: compute the gradient of the ready `f`
at `w` with a **central difference**: for each `i`,
`(f(w + ε eᵢ) − f(w − ε eᵢ)) / 2ε`, `ε = 1e-6`. Return the result as a list of
`round(..., 4)` values.

**Expected output:**

```
[-6.0, 4.0]
[-1.0, 3.0]
```
