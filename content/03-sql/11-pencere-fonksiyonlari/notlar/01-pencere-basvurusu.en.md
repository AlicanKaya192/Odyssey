This section's functions on one page. The results were measured on the
eight-table schema of the Intermediate level.

## How it is written

```sql
FUNCTION(...) OVER (
    PARTITION BY group_column    -- optional
    ORDER BY order_column        -- required for ranking functions
    ROWS BETWEEN ... AND ...     -- optional: the frame
)
```

## Ranking functions

| Function | On ties | Stock example (99, 99, 60) |
|---|---|---|
| `ROW_NUMBER()` | different numbers; which tied row comes first is not fixed | 1, 2, 3 |
| `RANK()` | the same number, then it skips | 1, 1, 3 |
| `DENSE_RANK()` | the same number, no skipping | 1, 1, 2 |
| `NTILE(n)` | splits the rows into n groups; extras go to the first ones | 12 rows, n = 5 → 3, 3, 2, 2, 2 |
| `PERCENT_RANK()` | a rank between 0 and 1 | ACC stocks: 0.0 … 1.0 |
| `CUME_DIST()` | the share of rows up to this value | lowest ACC stock: 0.1667 |

## Previous, next, the ends

| Function | What it gives |
|---|---|
| `LAG(x)` | the previous row's value; `NULL` if there is none |
| `LAG(x, 1, 0)` | `0` if there is none |
| `LAG(x, 2)` | two rows back |
| `LEAD(x)` | the next row's value |
| `FIRST_VALUE(x)` | the first value of the frame |
| `LAST_VALUE(x)` | the last value of the frame — **with the default frame, the row itself** |

## Aggregate functions with a window

| Written as | What it gives | Measured |
|---|---|---|
| `SUM(x) OVER ()` | the whole result's total | — |
| `SUM(x) OVER (PARTITION BY g)` | the group's total | — |
| `SUM(x) OVER (ORDER BY t)` | running; **ties go in together** | the three lines of 1001: 1815, 1815, 1815 |
| `SUM(SUM(x)) OVER (...)` | a window on top of a `GROUP BY` result | category total 99165.00 |
| `COUNT(*) OVER (PARTITION BY g)` | the group's number of rows, on every row | customer 1: 3 |
| `AVG(x) OVER (...)` | on a whole-number column, a whole number | 19 (really 19.33) |

## Frames

| Written as | The rows that go in |
|---|---|
| no frame, no `ORDER BY` | the whole group |
| no frame, with `ORDER BY` | from the start up to **this value** (ties together) |
| `ROWS UNBOUNDED PRECEDING` | from the start up to **this row** |
| `ROWS BETWEEN 1 PRECEDING AND CURRENT ROW` | the previous row and this one |
| `ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING` | previous, this, next |
| `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING` | the whole group |
| `RANGE BETWEEN 1 PRECEDING AND CURRENT ROW` | an error — `RANGE` takes no number |

## Where it can be written

| Place | Allowed |
|---|---|
| `SELECT` | yes |
| `ORDER BY` | yes |
| `WHERE` | no |
| `UPDATE ... SET` | no |

To filter, the numbered query goes inside `FROM (...) AS t` and the
`WHERE` is written outside.

## Error messages

| Written as | Message |
|---|---|
| `ROW_NUMBER() OVER ()` | `The function 'ROW_NUMBER' must have an OVER clause with ORDER BY.` |
| `WHERE ROW_NUMBER() OVER (...) <= 3` | `Windowed functions can only appear in the SELECT or ORDER BY clauses.` |
| `... AS rn ... WHERE rn <= 3` (in the same query) | `Invalid column name 'rn'.` |
| `RANGE BETWEEN 1 PRECEDING AND CURRENT ROW` | `RANGE is only supported with UNBOUNDED and CURRENT ROW window frame delimiters.` |

## Patterns

```sql
-- the first of each group
SELECT * FROM (
    SELECT ..., ROW_NUMBER() OVER (PARTITION BY g ORDER BY x DESC, id) AS rn
    FROM t
) AS s
WHERE rn = 1;

-- running total
SUM(x) OVER (ORDER BY t, id ROWS UNBOUNDED PRECEDING)

-- difference from the previous row
x - LAG(x) OVER (PARTITION BY g ORDER BY t)

-- share of the total
100.0 * x / SUM(x) OVER ()
```
