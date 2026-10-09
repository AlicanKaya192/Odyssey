Write the function `oldest(lines)`: every line is in the form
`"name,age"`. Turn the lines into
`Person = namedtuple("Person", ["name", "age"])` records (the age as `int`)
and return the **name** of the oldest person
(`max(..., key=lambda p: p.age)`).

**Expected output:**

```
Grace
```
