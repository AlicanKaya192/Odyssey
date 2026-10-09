Write the function `eval_postfix(tokens)` **with a stack**: it evaluates the
postfix expression. The tokens are integer strings and the operators `+`,
`-`, `*`.

- `["3", "4", "+", "2", "*"]` → `14`
- `["8", "2", "-"]` → `6`

Push a number with `int(token)`. On an operator take **the right** operand
first: `right = stack.pop()`, then `left = stack.pop()`.

**Expected output:**

```
14
6
14
```
