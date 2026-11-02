The risk register is a list of dictionaries: `name`, `likelihood`,
`impact`.

Write the function `top_risks(register, n)`: return the `n` risks with the
highest score (likelihood × impact) as `[name, score]` lists. Risks with
equal scores in alphabetical order of their names. If `n` is larger than
the number of risks, return all of them.

**Expected output:**

```
['ransomware', 15]
['laptop lost', 12]
['db leak', 10]
```
