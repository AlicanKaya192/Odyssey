Turn the `movie` dictionary into JSON text.

**What to do:**

1. Turn `movie` into a string called `text` with `json.dumps`; print the
   type of `text` and how many characters it has (`len`).
2. Turn the same dictionary into a readable string called `pretty` with
   `indent=2` and print it.

**Expected output:**

```text
<class 'str'>
96
{
  "title": "Arrival",
  "year": 2016,
  "genres": [
    "drama",
    "sci-fi"
  ],
  "seen": false,
  "rating": null
}
```

Look at how `False` and `None` are written in JSON.
