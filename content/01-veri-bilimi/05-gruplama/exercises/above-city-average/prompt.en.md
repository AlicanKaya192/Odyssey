You will answer "is this student above **their own city's** average?"
with the data from the file.

The data is in `students.csv`:

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

`mean()` cannot answer this: it gives **one row per group**, while you need
the group's average next to every row. That is exactly what `transform` is
for.

**What to do:**

1. Write the import and read the file.
2. Print the city averages, rounded to one decimal, **as a dictionary**.
3. Put each row's own city average next to it in a column called
   `city_mean`, rounded to one decimal.
4. Add an `above` column that is `True` when the score is above that city
   average.
5. Print the names of those above their own city **as a list**, then how
   many there are.

**Expected output:**

```
{'Adana': 82.0, 'Ankara': 85.2, 'Bursa': 70.0, 'Izmir': 71.3}
['Kerem', 'Mina', 'Efe', 'Sila', 'Zeynep', 'Can']
6
```

**The difference:**

- `groupby(...).mean()` → 4 rows (the number of cities). The table shrinks.
- `groupby(...).transform("mean")` → 12 rows. The table keeps its size and
  can take the result as a column.

**Look at Ada:** her score is 82, above the whole class's average (77.42).
Yet she is not on the list, because **her own city's** average is 85.2.
That is what grouping is for.
