You will write the first four checks to run when you open a new data
file.

The whole file (`survey.csv`):

```text
city,age,hours,score
Ankara,24,12,88
Izmir,31,5,62
Ankara,28,9,82
Bursa,45,,45
Izmir,22,14,91
Ankara,38,7,70
Bursa,52,3,51
Izmir,27,11,
Ankara,33,6,66
Izmir,29,13,89
```

**What to do:**

1. Write the import and read the file.
2. Print the **shape** of the table.
3. Print the column **types** as a readable list.
4. Print the total number of **empty cells**.
5. Print **how many different values** the `city` column has.

**Expected output:**

```
(10, 4)
['str', 'int64', 'float64', 'float64']
2
3
```

**Why these four:**

- **The shape** tells you the scale. Ten rows and a hundred thousand rows
  are different things.
- **The types** tell you whether cleaning is needed. Something interesting
  happens here: `hours` and `score` are whole numbers in the file, yet they
  came out as `float64`. The empty cells are the reason: `NaN` is a decimal
  number, a whole-number column cannot hold it, so pandas turns the whole
  column into decimals.
- **Empty cells** decide which results you can trust.
- **How many categories** there are: with 3 you can group; with 10,000 the
  column is an identifier.
