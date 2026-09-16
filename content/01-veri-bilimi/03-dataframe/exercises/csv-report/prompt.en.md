This time you use every part of the section **starting from a file**. You
write the code from the very top, imports included.

The data is in `students.csv`; its first lines look like this:

```text
name,city,age,hours,score
Ada,Ankara,21,12,82
Kerem,Izmir,23,6,74
Mina,Ankara,22,14,91
Deniz,Bursa,25,4,68
Efe,Ankara,21,11,88
Sila,Izmir,24,8,76
...
```

**What to do:**

1. Import `pandas` and read the file as `data`.
2. Print the shape of the table.
3. Build a new table with `name` as its index, called `report`, and print
   **Mina's score** through it.
4. Print how many people come from each city, **as a dictionary**.
5. Print the city with the most people.
6. Print how many **missing values** the table has in total.
7. On the last line, print the average score (two decimals) and the highest
   score **side by side**.

**Expected output:**

```
(12, 5)
91
{'Ankara': 4, 'Izmir': 3, 'Bursa': 3, 'Adana': 2}
Ankara
0
77.42 91
```

**Three things at once:**

- **`read_csv` turns the first line into column names** and columns that
  look like numbers into numbers; that is why you can take the mean of
  `score` straight away.
- **A column can be the index.** After `set_index("name")` you call a row by
  its name rather than a number: `loc["Mina", "score"]`.
- **`isna().sum()` counts per column**; for the whole table you add them up
  once more. The result is zero — this file is clean. On real data this is
  the first number to look at.
