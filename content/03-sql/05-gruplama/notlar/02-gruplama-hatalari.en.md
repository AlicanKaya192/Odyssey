The errors you will meet while grouping and what they mean. The server
states the first three plainly; the last three are **silent** and more
dangerous.

## Column 'X' is invalid in the select list

The full message reads:

```
Column 'products.name' is invalid in the select list because it is not
contained in either an aggregate function or the GROUP BY clause.
```

It is long, but it describes the problem exactly: you asked for the `name`
column without saying which row's name it should be.

The `Accessory` group holds six products. The server cannot tell whose
name to print, and it does not guess.

There are two ways out:

```sql
-- 1. add the column to the grouping (this makes smaller groups)
SELECT category, name, COUNT(*) FROM products GROUP BY category, name;

-- 2. say which one you want
SELECT category, MAX(name), COUNT(*) FROM products GROUP BY category;
```

The two give different results; you have to decide which you meant.

## An aggregate may not appear in the WHERE clause

```sql
WHERE COUNT(*) > 2      -- error
```

`WHERE` runs **before** the groups exist. At that moment the server is
looking at individual rows and there is nothing to count.

The piece that filters groups is `HAVING`:

```sql
GROUP BY category HAVING COUNT(*) > 2
```

## Invalid column name (inside HAVING)

```sql
SELECT category, COUNT(*) AS item_count
FROM products
GROUP BY category
HAVING item_count > 2   -- error: Invalid column name 'item_count'
```

The alias comes into existence while `SELECT` runs, and `HAVING` runs
**before** it.

The condition has to be written out in full: `HAVING COUNT(*) > 2`.

The same alias works inside `ORDER BY` — that runs last. This is the third
time the same rule has come up on this path.

---

## The silent mistakes

With these the query runs, a result comes back, and the number is wrong.

### 1. Confusing WHERE with HAVING

```sql
-- did you mean "count the products that are in stock"...
WHERE stock > 0 GROUP BY category

-- ...or "the categories whose total stock is above zero"?
GROUP BY category HAVING SUM(stock) > 0
```

These ask completely different questions and both of them run. The first
removes rows, the second removes groups.

### 2. Integer division inside AVG

`AVG(stock)` gives **27** while the real average is 27.41. Because the
column is an `INT`, the fraction is thrown away.

### 3. SUM giving NULL on an empty result

With no rows at all, `COUNT` gives zero but `SUM` gives `NULL`. The report
cell comes out blank, and "zero sales" gets confused with "no data".

---

## A habit for checking

When you write a grouping query, ask three questions:

1. **How many groups do I expect?** Is that the number of rows you got? If
   there are more, a column that should not be in the grouping list is.
2. **Do the group counts add up to the number of rows before grouping?**
   Add up the `COUNT(*)` values; with no `WHERE`, the total should equal
   the table's row count.
3. **Is the column I am averaging an integer?** If so, you need `CAST`.

The second question is especially useful: if it does not add up, either a
`WHERE` was forgotten or there is an unexpected `NULL` group.
