The students' details are in dictionaries with number keys and in a set.
Turn them into a report that JSON can carry without breaking it.

**What to do:**

1. First see the problem: turn `names` into JSON and read it back
   (`json.loads(json.dumps(names))`), and print it.
2. Build a dictionary called `report`:
   - `"tags"`: the **sorted list** of the set (`sorted(tags)`),
   - `"students"`: a list of `{"id": ..., "name": ..., "average": ...}`
     dictionaries, one per student (in id order; the mean with **integer
     division**).
3. Write `report` to the file `report.json` with `indent=2` and read it back
   as `back`.
4. Print: `back["tags"]`, each student's id, name and mean (on one line) and
   the type of the first student's `id`.

**Expected output:**

```text
{'1': 'Ada', '2': 'Alan', '3': 'Grace'}
['files', 'json', 'python']
1 Ada 87
2 Alan 82
3 Grace 90
<class 'int'>
```

When a number is a **key** it turns into text; when it is a **value** it
stays a number.
