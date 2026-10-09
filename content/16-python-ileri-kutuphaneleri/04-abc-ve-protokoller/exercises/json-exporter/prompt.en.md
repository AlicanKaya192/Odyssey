`JsonExporter`, which derives from the abstract `Exporter`, cannot be
built: its abstract method was written under the wrong name. Write the
method with the right name (`export`); it turns the rows into text with
`json.dumps(rows)`.

**Expected output:**

```
[{"name": "pen", "price": 1.5}]
```
