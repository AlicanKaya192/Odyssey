A running program can come across a file that is not there. A good program
does not crash because of it; it falls back to a default.

`settings.txt` has been placed next to your code, but `profile.txt` does
**not** exist.

**What you need to do:**

1. Write a function called `load_settings` that takes a file name.
   - If the file exists: split each line on `key=value` and return a
     dictionary.
   - If the file does **not** exist: catch the `FileNotFoundError` and return
     an **empty dictionary**.
2. Try the function with two files:
   - `load_settings("settings.txt")`
   - `load_settings("profile.txt")`
3. Hold the results in variables called `found` and `missing`, and print them
   in that order.

**Expected output:**

```
{'theme': 'dark', 'lang': 'en'}
{}
```

The program must finish without raising an error. A missing file is not a
problem here; it is an expected situation.

> The error does not come up until the file name reaches the `open` call, so
> the `try` block has to cover the `with` line as well.
