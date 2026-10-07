The record you want to send contains types JSON does not know: a **set**, a
**tuple** and a dictionary with **number keys**. `json.dumps(record)` fails
because of the set.

**What to do:**

1. Build a new dictionary called `clean` from `record`:
   - `id` stays the same,
   - the `tags` set becomes a **sorted** list (`sorted`),
   - the `coords` tuple becomes a list,
   - the keys of the `scores` dictionary are turned into text (`str`).
2. Turn it into text with `text = json.dumps(clean, sort_keys=True)` and
   print it.
3. Read it back with `back = json.loads(text)` and print the result of
   `back == clean`. It must be `True`: the cleaned record stays the same
   after the round trip.

**Expected output:**

```
{"coords": [38.42, 27.14], "id": 7, "scores": {"2023": 4.5, "2024": 4.8}, "tags": ["classic", "english", "novel"]}
same after round trip: True
```

Had you sent `record` uncleaned, the tuple would come back as a list and the
number keys as text, and `back == record` would be `False`.
