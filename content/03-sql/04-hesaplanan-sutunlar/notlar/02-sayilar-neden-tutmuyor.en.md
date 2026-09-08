When a number in a report does not add up, the cause is almost always one
of these five. All of them are **silent**: the query runs, there is no
error, the number is wrong.

## 1. Integer division

The most common one.

```sql
SELECT satilan / toplam * 100 AS yuzde
```

If `satilan` and `toplam` are integers, the division happens **first** and
gives 0 or 1; multiplied by 100 that becomes 0 or 100. Nothing in between
exists.

The fix:

```sql
SELECT satilan * 100.0 / toplam AS yuzde
```

Putting the multiplication first both makes it fractional and preserves
precision.

## 2. NULL contamination

```sql
SELECT price + kargo AS toplam
```

If the shipping cost is empty the total is empty. That row **disappears**
from the report total, or shows up blank.

```sql
SELECT price + ISNULL(kargo, 0) AS toplam
```

## 3. A rounding difference

`ROUND(2.5, 0)` is **3** on SQL Server and **2** in Python.

SQL rounds halves away from zero; Python rounds to even. Someone doing the
same calculation in both places sees differences of a penny and cannot
find the cause.

In accounting these differences accumulate; you have to decide up front
which side does the rounding.

## 4. Joining with `+`

```sql
SELECT name + ' ' + soyad AS tam_ad
```

For people with no surname recorded, `tam_ad` comes out **completely
empty** — the first name disappears too. `CONCAT` does not do this.

## 5. The precision of decimal types

`DECIMAL(10,2)` keeps two digits. Assign a division result to it and the
third digit is gone:

```sql
SELECT CAST(1.0/3 AS DECIMAL(10,2))   -- 0.33
```

It is better to use a wider type for intermediate steps and round **only
at the end**.

`FLOAT` is a different matter entirely: because it is stored in binary,
`0.1 + 0.2` is not exactly `0.3`. Columns holding money use `DECIMAL`,
never `FLOAT`.

---

## A habit for checking

When you write a calculated column, ask three questions:

1. **Is there a division?** If so, are both sides integers?
2. **Can any of the columns be `NULL`?** If so, what do you want to
   happen?
3. **Does one row match when worked out by hand?** Verifying a single row
   with a calculator saves fifteen minutes of searching.
