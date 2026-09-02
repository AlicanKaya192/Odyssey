A raw table has arrived with four separate problems. Remember the order
from the cleaning section: **names → text → types.**

**What you need to do:**

1. Take a **copy** so the raw data stays intact.
2. Strip the spaces from the column names and lower-case them.
3. Strip the leading and trailing spaces in the `name` column.
4. Clean the spaces from the `city` column and unify it in title case.
5. Convert the `score` column to numbers.
6. Print, in order: the list of column names, the list of types, the city
   counts **as a dict**, and the mean score (two decimals).

**Expected output:**

```
['name', 'city', 'score']
['str', 'str', 'int64']
{'Ankara': 3, 'Izmir': 2, 'Bursa': 1}
79.83
```

**Note:** before the cleaning, `"ankara"`, `"ANKARA"` and `"Ankara "` counted
as three separate groups. Look at the `value_counts()` output — now the three
are one.

The `score` column arrived as text, so no average could be taken; without
`to_numeric` the last line would raise an error.

The `copy()` habit: when you spot a mistake three steps later, you need to be
able to go back to the raw data.
