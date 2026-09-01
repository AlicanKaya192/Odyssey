When it is not known in advance how many arguments a function will take, `*`
is used.

**What you need to do:**

1. Write a function called `total`: it takes **however many** numbers arrive
   and returns their sum. If no arguments are given, it returns `0`.

2. Write a function called `describe`: it takes a `label` string followed by
   any number of extra details **given by name**. It returns a string in this
   form:

```
report: name=Ada, city=London
```

   That is: the `label`, a colon and a space, then `key=value` pairs
   separated by a comma and a space. If there are no extra details, it
   returns just `report:`.

3. Print these in order:
   - `total(1, 2, 3)`
   - `total()`
   - `describe("report", name="Ada", city="London")`
   - `describe("empty")`

**Expected output:**

```
6
0
report: name=Ada, city=London
empty:
```

> `*numbers` collects the incoming arguments into a tuple and `**details`
> collects the named ones into a dictionary. You can use
> `", ".join(parts)` to put the pieces together.
