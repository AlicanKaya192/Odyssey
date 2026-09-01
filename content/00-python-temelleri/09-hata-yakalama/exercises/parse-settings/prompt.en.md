Configuration files are usually made of `key=value` lines. Some lines can be
broken. In this exercise the **function reports** the broken line, and the
caller catches it and carries on.

**What you need to do:**

1. Write a function called `parse_line`:
   - If the line does **not** contain `=`, raise a `ValueError`. Its message
     must be exactly `bad line: ` followed by the line itself.
   - If it does, split the line in two at the first `=` and return both parts.

2. Process these lines in order:

```python
lines = ["name=Ada", "broken", "city=London"]
```

3. Start with an empty dictionary called `settings`.
   - If the line parses, put the key and the value into the dictionary.
   - If a `ValueError` comes up, print **the error's message** and carry on.

4. Print the `settings` dictionary once the loop finishes.

**Expected output:**

```
bad line: broken
{'name': 'Ada', 'city': 'London'}
```

> To split a string in two, use `line.split("=", 1)`; the second argument
> means "split at most once". That matters when the value itself contains an
> `=`. Code that should run when no error came up can go in an `else` block.
