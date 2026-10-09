Write the function `parentheses(n)`: it returns every **valid** string that
can be written with `n` pairs of parentheses. At each step try `(` first, then
`)`; generated in this order, the result comes out sorted by itself.

Pruning rules:

- `(` only if the number of opens is below `n`
- `)` only if the number of closes is below the opens

- `parentheses(2)` → `['(())', '()()']`

**Expected output:**

```
((()))
(()())
(())()
()(())
()()()
16796
```
