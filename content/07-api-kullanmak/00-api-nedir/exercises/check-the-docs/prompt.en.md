Looking at the documentation and asking "is this request right?" before
sending it catches many errors before the request even leaves. The `docs`
dictionary is an imaginary API's documentation: the **required** and
**optional** information of every endpoint.

**What to do:** write the function `check(path, params)`. `params` is a list
of the names of the information to send. Check in this order:

1. If the endpoint is not in the documentation, return
   `"404 unknown endpoint"`.
2. If one of the required names is missing from `params`, return **the first
   missing one in the documentation's order** as `"missing: days"`.
3. If `params` contains a name that does not appear in the documentation at
   all, return **the first one found** as `"unknown: color"`.
4. If everything is in place, return `"ok"`.

Then check the five requests below and print the results in order.

**Expected output:**

```
/weather ['city'] -> ok
/news [] -> 404 unknown endpoint
/forecast ['city'] -> missing: days
/weather ['city', 'color'] -> unknown: color
/cities [] -> ok
```
