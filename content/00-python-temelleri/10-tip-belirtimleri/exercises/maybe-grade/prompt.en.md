Some functions do not find what they are looking for. Saying so in the
annotation tells whoever uses it that they have to check.

**What you need to do:**

1. Write a function called `find_grade`:
   - Its parameter is `name`, a string.
   - Inside it there is the dictionary `{"Ada": 90, "Alan": 70}`.
   - If the name is in the dictionary, return its grade; otherwise return
     `None`.
   - The return annotation must express **both** the whole number and the
     `None` possibility.

2. Call the function for each name in `["Ada", "Grace"]`:
   - If the result is `None`, print `name not found`.
   - Otherwise print `name grade`.

**Expected output:**

```
Ada 90
Grace not found
```

Note: when you write `print(person, grade)` Python puts a space in between on
its own.

> "Either a whole number or nothing" is written with a vertical bar. You check
> for `None` with `is None`, not with `== None`.
