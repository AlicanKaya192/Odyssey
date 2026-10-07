An hour of an API's response codes is in the `codes` list. You will
summarise the server's health.

**What to do:**

1. Count how many responses of each class there are in a dictionary called
   `counts`. The keys are `"2xx"`, `"3xx"`, `"4xx"`, `"5xx"`; a class that
   never appears is there with `0`.
2. Print the classes in that order as `2xx: 11`.
3. Print the error rate (4xx + 5xx as a percentage of the total) with one
   decimal as `error rate: 40.0%`.
4. Print the most frequent **error** code and its name from `HTTPStatus`.

**Expected output:**

```
2xx: 11
3xx: 1
4xx: 6
5xx: 2
error rate: 40.0%
most common error: 404 Not Found
```

To print the percentage with one decimal use `f"{rate:.1f}%"`.
