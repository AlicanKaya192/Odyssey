You are writing your first server; a very small one. You have a **menu**:
every endpoint's response sits in a dictionary.

**What to do:**

1. Write a function called `request(path)`. If `path` is on the menu it
   returns its response, otherwise it returns `"404 Not Found"`.
2. Send requests for `"/weather"`, `"/cities"` and `"/news"` and print the
   responses in that order.

**Expected output:**

```
18 degrees, cloudy
Istanbul, Ankara, Izmir
404 Not Found
```

Here the `request` function is the server and the lines that call it are
the client. In a real API the only difference is that the request travels
over the internet.
