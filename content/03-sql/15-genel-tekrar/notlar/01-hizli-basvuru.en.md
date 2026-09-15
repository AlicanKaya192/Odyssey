The whole SQL path on one page. The details and measurements are in each
section's own notes.

## The skeleton of a query

```sql
SELECT   columns, calculations AS name, AGGREGATE(...), WINDOW() OVER (...)  -- 5
FROM     table_name t                                                       -- 1
JOIN     other o ON o.key_column = t.key_column                             -- 1
WHERE    the row's condition                                                -- 2
GROUP BY grouping columns                                                   -- 3
HAVING   the group's condition                                              -- 4
ORDER BY sort order                                                         -- 6
-- TOP n is written right after SELECT                                      -- 7
```

The number is the order the server runs it in. An alias is visible only
in `ORDER BY`.

## Filtering (01, 03)

| Written as | Note |
|---|---|
| `=`, `<>`, `<`, `>=` | do not work with `NULL` |
| `IS NULL`, `IS NOT NULL` | the only right test for `NULL` |
| `IN (...)`, `NOT IN (...)` | if the list has a `NULL`, `NOT IN` returns no rows |
| `BETWEEN a AND b` | both ends included |
| `LIKE 'M%'`, `'%e'`, `'_a%'` | `%` anything, `_` a single character |
| `AND`, `OR`, `NOT` | group with parentheses |

## Sorting and limiting (02)

`ORDER BY column [ASC|DESC]` — `NULL` first in ascending order. `TOP n`,
`TOP n WITH TIES`, `OFFSET ... FETCH`. If the order matters, `ORDER BY`
is required.

## Calculating (04)

Arithmetic (`7 / 2` = 3), `CAST`, `TRY_CAST`, `ROUND`, `CONCAT`,
`COALESCE`, `NULLIF`, `CASE WHEN ... THEN ... ELSE ... END`, `LEN`,
`UPPER`, `LEFT`, `SUBSTRING`, `REPLACE`, `TRIM`.

## Grouping (05)

`COUNT(*)`, `COUNT(column)` (does not count `NULL`), `COUNT(DISTINCT
...)`, `SUM`, `AVG` (a whole number on whole numbers), `MIN`, `MAX`.
Every non-aggregate column in `SELECT` must be in `GROUP BY`.

## Joining (06)

| Kind | The unmatched |
|---|---|
| `JOIN` | drop out |
| `LEFT JOIN` | the left side stays, the right is `NULL` |
| `FULL JOIN` | both stay |

With `LEFT JOIN`, a condition on the right-hand table goes into `ON`. A
join multiplies rows: `COUNT(DISTINCT ...)`.

## Subqueries (07)

`WHERE x = (SELECT ...)` needs a single value; `IN (SELECT ...)`,
`EXISTS`, `NOT EXISTS`, `FROM (SELECT ...) AS t`.

## Changing data (08)

```sql
INSERT INTO t (a, b) VALUES (1, 'x'), (2, 'y');
UPDATE t SET a = a + 1 WHERE ...;       -- without WHERE: every row
DELETE FROM t WHERE ...;
BEGIN TRAN; ...; ROLLBACK;              -- try it first
```

## Table design (09)

```sql
CREATE TABLE t (
    id INT IDENTITY(1,1) PRIMARY KEY,
    code NVARCHAR(10) NOT NULL UNIQUE,
    price DECIMAL(10,2) NOT NULL CHECK (price > 0),
    status NVARCHAR(20) NOT NULL DEFAULT 'open',
    parent_id INT NULL REFERENCES parents (id) ON DELETE CASCADE
);
ALTER TABLE t ADD c INT NULL;   DROP TABLE t;
```

## Dates and text (10)

`DATEADD`, `DATEDIFF` (counts boundaries), `EOMONTH`, `DATEFROMPARTS`,
`>= start AND < next start` for a period, `'YYYYMMDD'` for `DATETIME`,
`CHARINDEX`, `STRING_AGG ... WITHIN GROUP (ORDER BY ...)`, `FORMAT` at
the very end, `COLLATE` for the Turkish I.

## Windows (11)

`ROW_NUMBER` / `RANK` / `DENSE_RANK`, `SUM(...) OVER (ORDER BY ... ROWS
UNBOUNDED PRECEDING)`, `LAG`, `LEAD`, `x / SUM(x) OVER ()`. The first of
a group: an inner query + `WHERE rn = 1` outside.

## WITH (12)

`WITH a AS (...), b AS (... FROM a) SELECT ...;` — the previous statement
ends with `;`. Recursion: the start + `UNION ALL` + the self-referring
part; `OPTION (MAXRECURSION n)` at the end of the statement.

## Indexes (13)

`CREATE INDEX ix ON t (a, b) INCLUDE (c) WHERE ...;` — sought by its
first column; a function on the column or a `LIKE` starting with `%`
pushes it into a scan; every index makes writes more expensive.
Measuring: `SET STATISTICS IO ON`.

## Views and procedures (14)

`CREATE VIEW dbo.v AS SELECT ...` (no `ORDER BY`, name the columns),
`WITH CHECK OPTION`; `CREATE PROCEDURE dbo.p @x INT, @y INT OUTPUT AS
...`, `EXEC dbo.p 1, @n OUTPUT`, `THROW 50001, N'...', 1;`. Both in a
batch of their own: `GO` in between.
