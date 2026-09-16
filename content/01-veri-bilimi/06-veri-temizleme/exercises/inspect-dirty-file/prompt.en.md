Before cleaning, you **look**. This file was left dirty on purpose; a
five-line inspection catches most of its problems.

The whole file (`students_raw.csv`):

```text
id,name,city,score
1, Ada ,Ankara,82
2,kerem,izmir ,74
3,MINA,ANKARA,91
3,MINA,ANKARA,91
4,Deniz,bursa,
5,efe ,IZMIR,abc
6,Sila,,76
7,Kaan,Bursa,-1
```

**What to do:**

1. Write the import and read the file as `raw`.
2. Print the shape of the table.
3. Print the column types as a readable list.
4. Print how many **missing cells** there are in total.
5. Print how many rows are **exact duplicates**.
6. Print how many **different spellings** the `city` column has.

**Expected output:**

```
(8, 4)
['int64', 'str', 'str', 'str']
2
1
6
```

**Every number points at a problem:**

- **`score` came out as text.** The column holds `abc`; a single broken
  value turns the whole column into text, so you cannot take its mean. The
  type will need fixing.
- **Two missing cells:** Deniz's score and Sila's city are empty.
  `read_csv` turns an empty cell into `NaN`.
- **One duplicate:** Mina is written twice.
- **More spellings than real cities.** `Ankara`, `ANKARA`, `izmir ` (with a
  trailing space) — to the computer they are all different values. Unless
  fixed before grouping, one city splits into several groups.

There is one more thing you can see but not count: Kaan's score is `-1`.
The type is right and the cell is filled, but the value is impossible.
That is what the outliers heading is for.
