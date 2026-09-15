# Dates and Text

Most real data is either a date or a piece of text. In the fifth section
you saw the basic text functions: `LEN`, `UPPER`, `LEFT`, `SUBSTRING`,
`REPLACE`, `CONCAT`. This section looks at two new things: **calculating
with dates** and **searching and gathering** in text.

The two share one thing: the result can depend on the server's
**settings**. Everything below was measured, and what depends on a setting
is marked as such.

## Date types

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">DATE</span><span class="anat-body">The day only: <code>2026-03-14</code>. An order date, a birthday.</span></div>
    <div class="anat-row"><span class="anat-label">DATETIME2</span><span class="anat-body">Day and time: <code>2026-03-14 09:30:00</code>. The moment of an event.</span></div>
    <div class="anat-row"><span class="anat-label">DATETIME</span><span class="anat-body">The older day-and-time type. New tables prefer <code>DATETIME2</code>.</span></div>
  </div>
</figure>

The current time comes as `DATETIME` from `GETDATE()` and as `DATETIME2`
from `SYSDATETIME()` (measured). For today's date only:
`CAST(GETDATE() AS DATE)`.

## Writing a date safely

This is the sneakiest trap in the section. Measured:

| Written as | Setting | As `DATE` | As `DATETIME` |
|---|---|---|---|
| `'2026-03-04'` | default | March 4 | March 4 |
| `'2026-03-04'` | `SET DATEFORMAT dmy` | March 4 | **April 3** |
| `'03/04/2026'` | `SET DATEFORMAT dmy` | **April 3** | — |
| `'03/04/2026'` | `SET DATEFORMAT mdy` | March 4 | — |
| `'20260304'` | any setting | March 4 | March 4 |

The same text becomes a different day depending on the server's date
format setting — and **raises no error**. The old `DATETIME` type can
misread even a date written with dashes.

The rule:

- **`'YYYY-MM-DD'` is safe for `DATE` columns.**
- **With `DATETIME`, write it without separators: `'20260304'`.**
- Never use the slashed form like `'03/04/2026'`.

## DATEADD: adding time to a date

```sql
SELECT DATEADD(day, 7, order_date) AS due_date FROM orders;
```

`DATEADD(unit, amount, date)`. The unit can be `day`, `month`, `year`,
`hour`; a negative amount goes backwards.

Adding months is subtler than it looks — measured:

| Expression | Result |
|---|---|
| January 31 + 1 month | **February 28** |
| March 31 + 1 month | **April 30** |
| March 31 − 1 month | February 28 |
| February 29, 2024 + 1 year | February 28, 2025 |
| January 31 + 30 days | March 2 |

If the day does not exist in the target month, the server clips it to
**the last day of the month**. "One month later" and "30 days later" are
not the same thing.

## DATEDIFF: the gap between two dates

```sql
SELECT DATEDIFF(day, o.order_date, s.shipped_date) AS days
FROM orders o JOIN shipments s ON s.order_id = o.id;
```

`DATEDIFF(unit, earlier, later)`. Give them the other way round and the
result is negative (`-2`, measured).

**Careful: `DATEDIFF` counts boundaries, not durations.** It asks "how
many new years lie in between?":

| Range | Unit | Result |
|---|---|---|
| December 31, 2025 → January 1, 2026 (1 day) | `year` | **1** |
| January 1, 2025 → December 31, 2025 (364 days) | `year` | **0** |
| January 31 → February 1 (1 day) | `month` | **1** |

For length of service that gives the wrong answer. Measured as of January
10, 2026:

| Employee | Hired | `DATEDIFF(year, ...)` | `DATEDIFF(day, ...) / 365` |
|---|---|---|---|
| Deniz Kaya | February 5, 2024 | **2** | 1 |
| Fulya Demir | May 30, 2025 | **1** | 0 |

Deniz Kaya has worked there for 1 year and 11 months; the year difference
says "2". If whole years are what you need, dividing the gap in days by
365 comes much closer.

## Parts, month start, month end

```sql
SELECT YEAR(order_date), MONTH(order_date), DAY(order_date) FROM orders;
```

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">EOMONTH(date)</span><span class="anat-body">The last day of the month: February 2026 → <code>2026-02-28</code>, February 2024 → <code>2024-02-29</code>.</span></div>
    <div class="anat-row"><span class="anat-label">EOMONTH(date, -1)</span><span class="anat-body">The last day of the previous month. Add a day and you get the first of this month: <code>2026-03-01</code>.</span></div>
    <div class="anat-row"><span class="anat-label">DATEFROMPARTS(y, m, d)</span><span class="anat-body">A date from its parts: <code>DATEFROMPARTS(2026, 3, 1)</code>. A day that does not exist (February 30) is an <b>error</b>.</span></div>
  </div>
</figure>

## Filtering a month

There are three ways to find the March orders:

```sql
-- 1. a half-open range
WHERE order_date >= '2026-03-01' AND order_date < '2026-04-01'

-- 2. with a function
WHERE MONTH(order_date) = 3

-- 3. BETWEEN
WHERE order_date BETWEEN '2026-03-01' AND '2026-03-31'
```

On this data all three bring back the same three orders. But they differ:

- The second brings back March of **every year**; for the year you have
  to add `YEAR(...)` as well. And because it applies a function to the
  column, it cannot use the indexes you will meet at the advanced level.
- The third goes wrong on values **with times**. Measured — on a
  `DATETIME2` column holding four events:

| Filter | Found |
|---|---|
| `BETWEEN '2026-03-01' AND '2026-03-31'` | **2** |
| `>= '2026-03-01' AND < '2026-04-01'` | **3** |

Written without a time, `'2026-03-31'` means "midnight on March 31"; the
event at 14:30 on March 31 was left out.

**The rule: filter a period with a half-open range** — start included,
end excluded. It is right for every type and every period.

## Grouping by date

```sql
SELECT YEAR(order_date) AS y, MONTH(order_date) AS m, COUNT(*) AS n
FROM orders
GROUP BY YEAR(order_date), MONTH(order_date)
ORDER BY y, m;
```

Measured: January 2, February 3, March 3, April 2 orders.

## Showing a date

**How a date is stored** and **how it looks on screen** are separate
things. To show it:

```sql
FORMAT(order_date, 'dd.MM.yyyy')          -- 14.03.2026
FORMAT(order_date, 'MMMM yyyy', 'tr-TR')  -- Mart 2026
FORMAT(order_date, 'MMMM yyyy', 'en-US')  -- March 2026
CONVERT(NVARCHAR(10), order_date, 104)    -- 14.03.2026
```

All four were measured. `DATENAME(month, ...)` also gives the month's
name, but **in the session's language**: on this server it came out as
`March` and `Saturday`. If the name has to be in a particular language,
give `FORMAT` the culture explicitly.

The display functions return **text**; sorting or doing date arithmetic
with it no longer works correctly. Leave formatting to the very end.

## Searching in text: CHARINDEX

```sql
SELECT CHARINDEX(' ', 'Ada Kilic');   -- 4
```

It tells you **at which character** the searched part starts; `0` if it
is not there. To split a first and last name:

```sql
SELECT LEFT(name, CHARINDEX(' ', name) - 1)              AS first_name,
       SUBSTRING(name, CHARINDEX(' ', name) + 1, LEN(name)) AS last_name
FROM employees;
```

It split all six employees correctly (measured). But **with no space**
`CHARINDEX` gives 0, and `LEFT(name, -1)` is an error: `Invalid length
parameter passed to the left function.` If the real data has one-word
names, that needs thinking about in advance.

## Gathering rows into one text: STRING_AGG

```sql
SELECT category_code,
       STRING_AGG(name, ', ') WITHIN GROUP (ORDER BY name) AS products
FROM products
GROUP BY category_code;
```

Measured: for `ACC`, `Cable, Headset, Keyboard, Microphone, Mouse, Webcam`.

Without `WITHIN GROUP (ORDER BY ...)` the order was not alphabetical —
`Keyboard, Mouse, Headset, Webcam, Cable, Microphone`, the order they
were added to the table. If the order matters, you have to write it.

`STRING_SPLIT` does the reverse: `STRING_SPLIT('red,green,,blue', ',')`
returned four rows, including the empty piece in the middle.

## A few small tools

| Expression | Result (measured) |
|---|---|
| `CONCAT_WS(' - ', 'A', NULL, 'C')` | `A - C` — puts the separator in itself and skips the empty part |
| `RIGHT('000' + CAST(1 AS VARCHAR(10)), 3)` | `001` — leading zeros |
| `FORMAT(12, 'D3')` | `012` |

## The Turkish I trap

Turkish has two separate "i"s: dotted (`i` / `İ`) and dotless (`ı` /
`I`). If the server is set to Turkish, capital and small letter
conversion follows that. Measured:

| Expression | Turkish-set server | Latin-set |
|---|---|---|
| `UPPER('istanbul')` | `İSTANBUL` | `ISTANBUL` |
| `LOWER('ISTANBUL')` | `ıstanbul` | — |
| `WHERE city = 'istanbul'` | **0 rows** | 2 rows |
| `WHERE city LIKE 'ist%'` | **0 rows** | — |

Two customers' city in the table is `Istanbul`. On the Turkish-set server
a search in small letters **found neither of them**: the small form of `I`
is `ı`, not `i`.

The server on this machine is set to Turkish. When comparing text that
comes from a search box, stating the language setting explicitly makes
the result fixed:

```sql
WHERE city COLLATE Latin1_General_CI_AS = 'istanbul'   -- 2 rows
```

(The SQL exercises in this application were tried on both a Turkish-set
and a Latin-set server; their results do not depend on the setting.)

## Summary

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">Writing dates</span><span class="anat-body"><code>'YYYY-MM-DD'</code> for <code>DATE</code>, <code>'YYYYMMDD'</code> for <code>DATETIME</code></span></div>
    <div class="anat-row"><span class="anat-label">Adding time</span><span class="anat-body"><code>DATEADD</code> — clips to the month's end when adding months</span></div>
    <div class="anat-row"><span class="anat-label">The gap</span><span class="anat-body"><code>DATEDIFF</code> — counts boundaries; days / 365 for service</span></div>
    <div class="anat-row"><span class="anat-label">Filtering a period</span><span class="anat-body">A half-open range: <code>&gt;= start AND &lt; next start</code></span></div>
    <div class="anat-row"><span class="anat-label">Showing</span><span class="anat-body"><code>FORMAT</code> with an explicit culture — at the very end</span></div>
    <div class="anat-row"><span class="anat-label">Searching / gathering</span><span class="anat-body"><code>CHARINDEX</code>, <code>STRING_AGG ... WITHIN GROUP</code></span></div>
    <div class="anat-row"><span class="anat-label">Turkish I</span><span class="anat-body">Fix the language setting in the comparison with <code>COLLATE</code></span></div>
  </div>
</figure>

The Intermediate level ends here. At the Advanced level you will first
meet **window functions**: adding a group's information to every row
without grouping the rows.
