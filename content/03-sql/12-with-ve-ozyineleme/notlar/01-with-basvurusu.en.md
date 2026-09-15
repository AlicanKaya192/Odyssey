This section's syntax and rules on one page. The results were measured
on the eight-table schema of the Intermediate level.

## How it is written

```sql
-- a single CTE
WITH name AS (
    SELECT ...
)
SELECT ... FROM name;

-- more than one: with commas, each sees the ones before it
WITH a AS (SELECT ...),
     b AS (SELECT ... FROM a)
SELECT ... FROM b;

-- naming the columns
WITH x (product, cost) AS (
    SELECT name, price FROM products
)
SELECT product, cost FROM x;

-- recursive
WITH r AS (
    SELECT ...                  -- the start: runs once
    UNION ALL
    SELECT ... FROM ... JOIN r  -- the part that refers to itself
)
SELECT ... FROM r
OPTION (MAXRECURSION 200);      -- optional, at the end of the statement
```

## Rules

| Rule | Measured |
|---|---|
| The statement before `WITH` ends with `;` | otherwise one of two syntax errors |
| A CTE is valid only in the statement right after it | `Invalid object name` in a second statement |
| A CTE can use another CTE only if it was defined **before** it | `Invalid object name 'b'` |
| Each name once within the same `WITH` | `Duplicate common table expression name` |
| `ORDER BY` inside a CTE only with `TOP` / `OFFSET` | error 1033 otherwise |
| No `WITH` inside a CTE | a syntax error |
| A CTE can go before `SELECT`, `DELETE`, `UPDATE` | the change goes to the underlying table |

## Rules for a recursive CTE

| Rule | Measured |
|---|---|
| The two parts joined with `UNION ALL` | `UNION` → error 252 |
| Column types the same in both parts | otherwise `Types don't match between the anchor and the recursive part` |
| No aggregation in the self-referring part | `MAX`, `GROUP BY`, `HAVING` → error 467 |
| No outer join in the self-referring part | `LEFT JOIN` → error 462 |
| The default limit is 100 steps | 101 rows passed, 102 stopped |
| `OPTION (MAXRECURSION n)` | `0` means no limit; 32767 at most; cannot go inside the CTE |

## Error messages

| Situation | Message |
|---|---|
| `WITH` without a semicolon after `SET` | `Incorrect syntax near the keyword 'with'. ... the previous statement must be terminated with a semicolon.` |
| `WITH` without a semicolon after `SELECT` | `Incorrect syntax near 'x'. If this is intended to be a common table expression, you need to explicitly terminate the previous statement with a semi-colon.` |
| `ORDER BY` inside a CTE | `The ORDER BY clause is invalid in views, inline functions, derived tables, subqueries, and common table expressions, unless TOP, OFFSET or FOR XML is also specified.` |
| recursion with `UNION` | `Recursive common table expression 'chain' does not contain a top-level UNION ALL operator.` |
| type mismatch | `Types don't match between the anchor and the recursive part in column "path" of recursive query "chain".` |
| the limit was hit | `The statement terminated. The maximum recursion 100 has been exhausted before statement completion.` |
| the limit is too large | `The value 40000 specified for the MAXRECURSION option exceeds the allowed maximum of 32767.` |

## Patterns

```sql
-- the first of each group
WITH ranked AS (
    SELECT ..., ROW_NUMBER() OVER (PARTITION BY g ORDER BY x DESC, id) AS rn
    FROM t
)
SELECT ... FROM ranked WHERE rn = 1;

-- deleting duplicates (one of each stays)
WITH d AS (
    SELECT ROW_NUMBER() OVER (PARTITION BY key_column ORDER BY id) AS rn
    FROM t
)
DELETE FROM d WHERE rn > 1;

-- down a tree
... UNION ALL SELECT e.* FROM t e JOIN r ON e.parent_id = r.id

-- up a tree
... UNION ALL SELECT e.* FROM t e JOIN r ON e.id = r.parent_id

-- a series of months
WITH months AS (
    SELECT CAST('2026-01-01' AS DATE) AS month
    UNION ALL
    SELECT DATEADD(month, 1, month) FROM months WHERE month < '2026-06-01'
)
SELECT month FROM months;
```
