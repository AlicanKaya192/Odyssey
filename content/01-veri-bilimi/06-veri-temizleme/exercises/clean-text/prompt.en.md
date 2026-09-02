The same city arrives in three different spellings. Group without fixing
that and **the counts get split**.

The column names were cleaned in the starter code; the values are next.

**What you need to do:**

1. Print how many distinct cities there are **before** cleaning.
2. Strip the spaces in the `name` and `city` columns and capitalise the first
   letter of each word.
3. Print the `name` and `city` columns.
4. Print how many distinct cities there are **after** cleaning.

**Expected output:**

```
6
    name    city
0    Ada  Ankara
1  Kerem   Izmir
2   Mina  Ankara
3    Ada  Ankara
4  Deniz   Bursa
5    Efe   Izmir
6   Sila  Ankara
3
```

**The first and last lines are the whole point:** the same data, **six**
cities before and **three** after. To pandas, `"Ankara"`, `"ANKARA"` and
`"Ankara "` were three different values.

Write `groupby("city")` without noticing and Ankara is split into three
groups, none of whose averages is right.

**A way to check:** if `nunique()` is larger than you expect, there are
inconsistent spellings.
