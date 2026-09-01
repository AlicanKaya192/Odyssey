A key that is not in a dictionary raises `KeyError`, and an index that is not
in a list raises `IndexError`. Both mean "what you asked for is not there", so
you can answer both the same way.

**What you need to do:**

1. Write a function called `lookup`. It takes two things: `data` and `key`.
2. Try to return the value `data[key]`.
3. If a `KeyError` **or** an `IndexError` comes up, return `"missing"`.
4. Try the function with these four calls and print the results:

```python
lookup({"a": 1}, "a")
lookup({"a": 1}, "b")
lookup([10, 20], 1)
lookup([10, 20], 5)
```

**Expected output:**

```
1
missing
20
missing
```

Note: the same function works with both a dictionary and a list. `data[key]`
is valid for both — a key in a dictionary, an index in a list.

> To catch more than one error with a single `except`, write them in brackets
> separated by a comma: `except (KeyError, IndexError):`
