This time you do the reverse: you build an address from parameters. The
values contain spaces and `&`; glue them by hand and the address breaks.

**What to do:**

1. Build the variable `url` from `forecast_base` and `forecast_params`:
   base + `?` + `urlencode(...)`.
2. Build the variable `search_url` the same way from `search_base` and the
   dictionary `{"q": "fish & chips", "lang": "en"}`.
3. Print both in order.

**Expected output:**

```
https://api.example.com/v1/forecast?city=New+York&units=metric&days=3
https://api.example.com/v1/search?q=fish+%26+chips&lang=en
```

Look at how the space became `+` and how the `&` inside the value became
`%26`. The `&` that separates parameters stays as it is.
