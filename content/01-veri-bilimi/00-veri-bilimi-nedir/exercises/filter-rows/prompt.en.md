Who in Ankara scored 80 or more? Most data work starts with a question like
this.

**What you need to do:**

1. The `records` list is ready in the starter code.
2. Collect the records whose city is `"Ankara"` **and** whose score is 80 or
   more into a list called `selected`.
3. Collect only the names of those records into a list called `names`.
4. Print the `names` list, then print how many records were selected.

**Expected output:**

```
['Ada', 'Mina']
2
```

In pandas this will be a single line:
`data[(data["city"] == "Ankara") & (data["score"] >= 80)]`
