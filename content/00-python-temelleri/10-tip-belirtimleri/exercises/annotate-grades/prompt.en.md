In this exercise you will write down what is inside the containers.

**What you need to do:**

1. Define two variables together with their annotations:
   - `grades` — a dictionary with string keys and whole-number values. Starting
     value: `{"Ada": 90, "Alan": 70}`
   - `passed` — an **empty** list of strings.

2. Write a function called `average`:
   - Its parameter is `values`, a dictionary with string keys and whole-number
     values.
   - It returns a whole number.
   - It works out the average of the values using **floor division**:
     `sum(...) // len(...)`

3. Go through `grades`; add the name to `passed` when the grade is **80 or
   above**.

4. Print the average first, then the `passed` list.

**Expected output:**

```
80
['Ada']
```

> `passed` starts out empty. Nothing in the code tells you what will go into
> it, which is exactly why the annotation is needed here.
