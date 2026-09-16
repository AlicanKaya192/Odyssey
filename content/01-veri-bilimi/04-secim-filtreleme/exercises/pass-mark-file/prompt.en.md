The pass mark has moved to 75: everyone below it gets a 75. You read the
data from a file and change the table **for real**.

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

**What to do:**

1. Write the import and read the file.
2. Build a condition for scores **below 75** and print the names of those
   people **as a list**.
3. With the same condition, set `score` to `75` on those rows.
4. Print how many people now have exactly 75.
5. Print the new average score (two decimals).

**Expected output:**

```
['Kerem', 'Deniz', 'Kaan', 'Ela', 'Can']
5
79.67
```

**The real point of this exercise:** the line below **does nothing.**

```python
data[data["score"] < 75]["score"] = 75
```

The brackets produce an intermediate table, the assignment goes to it, and
that table is thrown away at once. You get no error either — the code runs
and the table is unchanged. The average would stay at 77.42.

The right way is to select and assign **in a single `loc` call**:
`data.loc[condition, "score"] = 75`. The rule: when you change a table, do
not stack two sets of brackets.
