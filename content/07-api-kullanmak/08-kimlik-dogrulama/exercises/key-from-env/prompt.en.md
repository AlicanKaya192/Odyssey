The key is not written into the code; it is read from an environment
variable. In this exercise the variable is not defined, so the practice
server's public key is used as the default.

**What to do:**

1. Write the function `get_key()`: it reads the `LIBRARY_KEY` environment
   variable with `os.environ.get` and returns `"demo-key-123"` if it is
   missing.
2. Print whether the variable is defined (`"LIBRARY_KEY" in os.environ`).
3. Send a request to `/stats` with the key from `get_key()`; print the code
   and the number of books.

**Expected output:**

```
LIBRARY_KEY defined: False
status: 200
books: 23
```

In a real project there is no default: without a key the program should
stop. The default here is so that the exercise works on every computer.
