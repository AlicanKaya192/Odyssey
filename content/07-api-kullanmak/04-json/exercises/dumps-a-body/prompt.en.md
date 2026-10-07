You are going to add a new book to an API (`POST /books`). The data for the
body is a Python dictionary for now; you need to turn it into JSON text.

**What to do:**

1. Turn `book` into a string called `text` with `json.dumps` and print it.
2. Print the same dictionary once more in readable form with `indent=2`.

**Expected output:**

```
{"title": "Emma", "author": "Austen", "available": true, "note": null}
{
  "title": "Emma",
  "author": "Austen",
  "available": true,
  "note": null
}
```

Look at how `True` became `true`, `None` became `null` and the quotes are
double.
