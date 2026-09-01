Below is a function that works, but does not say what it expects:

```python
def repeat(text, count):
    return text * count
```

In this exercise you will write down what it expects **without changing** how
it behaves.

**What you need to do:**

1. Add annotations to `repeat`:
   - `text` is a string (`str`)
   - `count` is a whole number (`int`)
   - the function returns a string (`str`)

2. Call the function twice and print the result:
   - `repeat("ab", 3)`
   - `repeat("-", 5)`

**Expected output:**

```
ababab
-----
```

Do not touch the body of the function; only the signature line changes.

> Parameters are annotated with `:`, the return type after the parentheses
> with `->`.
