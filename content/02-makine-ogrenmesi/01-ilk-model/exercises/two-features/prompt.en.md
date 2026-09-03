The file also has an `age` column — the age of the house. What happens when
you add it to the model?

**What you need to do:**

1. Read the file. This time take **two columns** into `X`: `area` and `age`.
2. Split it the same way (a quarter for testing, `random_state=42`) and
   train the model.
3. Print the two coefficients **side by side** (two decimals): `area`'s
   first, then `age`'s.
4. Print the mean absolute error (two decimals).
5. The single-feature model's error was **18.5**. Print `better` if the new
   model beats that, otherwise `worse`.

**Expected output:**

```
2.77 -3.35
7.13
better
```

**Notice how little the code changed:** only the line where you build `X`.
Splitting, training and measuring are identical. sklearn's design is what
makes this so cheap.

**The sign of each coefficient says something:** as area goes up the price
goes up (+2.77); as age goes up it goes down (-3.35). Nobody told the model
that older houses are cheaper; the numbers came out of the data.

**Two warnings:**

- **A coefficient does not state a cause.** The correct sentence is "houses
  that are older come out cheaper", not "age lowers the price".
- **You cannot say "age matters more" because 3.35 > 2.77.** Area ranges
  from 45 to 165, age from 0 to 30. A coefficient depends on its column's
  unit; two numbers in different units are not comparable. Comparing them
  requires scaling first.
