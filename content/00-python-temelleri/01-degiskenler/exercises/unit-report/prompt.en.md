You will use variables, type conversion and f-strings together.

The measurements you have are held as **text** — that is how data arrives in
real life:

```python
raw_height = "180"
raw_weight = "75.5"
name = "Ada"
```

**What you need to do:**

1. Hold the height as a **whole number** in a variable called `height`.
2. Hold the weight as a **decimal number** in a variable called `weight`.
3. Hold the height in metres in a variable called `meters` (divide the
   centimetres by 100).
4. Hold the body mass index in a variable called `bmi`: weight divided by
   metres squared, **rounded to two decimal places**.
5. On one line, print this **using an f-string**:

```
Ada is 1.8 m and 75.5 kg, bmi 23.3
```

**Expected output:**

```
Ada is 1.8 m and 75.5 kg, bmi 23.3
```

Note: do not type any of the numbers yourself; they are all worked out.

> `int("180")` turns text into a whole number and `float("75.5")` into a
> decimal. `round(value, 2)` rounds to two places. Inside an f-string a
> variable goes in curly brackets: `f"{name} is ..."`
