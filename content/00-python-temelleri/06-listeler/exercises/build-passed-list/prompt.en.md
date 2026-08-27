A list of exam results is given:

```python
scores = [45, 82, 67, 30, 95, 58]
```

Build a **new list** from the results that are 60 **or above**. Call it
`passed`.

Then print both the list and how many passed. Expected output:

```
[82, 67, 95]
3
```

The method is: start with an empty list, loop over the original, and `append`
every item that meets the condition to the new list.

> It says `60 or above`, so you need `>=`. With `>` someone scoring exactly 60
> would be left out. There is no exact 60 in this example, but building the
> right habit matters.
