Shop A's unit price changes a few times a year. `prices.csv` holds only
the days it changed (`valid_from`, `price`). Multiply each day's sales by the
price in effect that day and find the revenue.

**What to do:**

1. Read `stores.csv`; take shop A's `date` and `sales` columns and sort by
   date.
2. Read `prices.csv` with `parse_dates=["valid_from"]`.
3. First try an ordinary join (`merge`, `how="left"`) and print the number of
   rows that got a price.
4. Join with `pd.merge_asof` (`left_on="date"`, `right_on="valid_from"`).
   Print the prices on the rows of 14, 15 and 16 March 2024 as a list.
5. Add the column `revenue = sales * price` and print the total revenue,
   rounded to one decimal.
6. Print how many days each price was in effect as a dict:
   `joined["price"].value_counts().sort_index().to_dict()`.

**Expected output:**

```
5
[19.9, 21.5, 21.5]
2562737.2
{19.9: 74, 21.5: 78, 21.9: 71, 22.9: 101, 24.5: 42}
```

The ordinary join matched only the five days on which the price changed.
`merge_asof` looked back for every day and found the latest price record:
14 March is at the old price; from 15 March the new one applies.
