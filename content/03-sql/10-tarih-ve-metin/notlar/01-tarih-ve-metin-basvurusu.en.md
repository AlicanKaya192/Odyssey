This section's functions on one page. Every result was measured on the
real server; the ones that depend on a setting are in the second note.

## Date functions

| Function | Example | Result |
|---|---|---|
| `GETDATE()` | now | `DATETIME` |
| `SYSDATETIME()` | now | `DATETIME2` |
| `CAST(GETDATE() AS DATE)` | today | the day only |
| `DATEADD(day, 7, d)` | January 8 | January 15 |
| `DATEADD(month, 1, '2026-01-31')` | | `2026-02-28` |
| `DATEDIFF(day, a, b)` | January 8 → 10 | `2` |
| `YEAR(d)`, `MONTH(d)`, `DAY(d)` | | the parts |
| `EOMONTH(d)` | February 2024 | `2024-02-29` |
| `EOMONTH(d, -1)` | March | the last day of February |
| `DATEFROMPARTS(2026, 3, 1)` | | `2026-03-01` |

## How DATEADD clips

| Expression | Result |
|---|---|
| January 31 + 1 month | February 28 |
| March 31 + 1 month | April 30 |
| March 31 − 1 month | February 28 |
| February 29, 2024 + 1 year | February 28, 2025 |
| January 31 + 30 days | March 2 |

If the day does not exist in the target month, the last day of the month.

## DATEDIFF counts boundaries

| Range | Unit | Result |
|---|---|---|
| December 31 → January 1 | `year` | 1 |
| January 1 → December 31 (same year) | `year` | 0 |
| January 31 → February 1 | `month` | 1 |
| January 10 → January 8 | `day` | −2 |

For whole years, `DATEDIFF(day, a, b) / 365`.

`DATEDIFF` returns a whole number; convert to `DECIMAL` before averaging
it. For the shipping time, FastLine's average is **2** with whole numbers
and **2.67** correctly.

## Month start and month end

```sql
DATEADD(day, 1, EOMONTH(d, -1))   -- the first day of this month
EOMONTH(d)                        -- the last day of this month
DATEADD(day, 1, EOMONTH(d))       -- the first day of the next month
```

## Filtering a period

```sql
WHERE d >= '2026-03-01' AND d < '2026-04-01'
```

Start included, end excluded. On values with times `BETWEEN` misses the
hours of the last day (of four events `BETWEEN` found 2, the half-open
range 3).

## Text functions (this section's)

| Function | Example | Result |
|---|---|---|
| `CHARINDEX(' ', 'Ada Kilic')` | | `4` |
| `CHARINDEX(' ', 'Madonna')` | not found | `0` |
| `STRING_AGG(name, ', ') WITHIN GROUP (ORDER BY name)` | grouped | `Cable, Headset, ...` |
| `STRING_SPLIT('red,green,,blue', ',')` | | 4 rows, the empty piece included |
| `CONCAT_WS(' - ', 'A', NULL, 'C')` | | `A - C` |
| `RIGHT('000' + CAST(1 AS VARCHAR(10)), 3)` | | `001` |
| `FORMAT(12, 'D3')` | | `012` |

The basic text functions (`LEN`, `UPPER`, `LEFT`, `SUBSTRING`, `REPLACE`,
`TRIM`, `CONCAT`) are in the fifth section.

## Splitting a first and last name

```sql
LEFT(name, CHARINDEX(' ', name) - 1)                 -- first name
SUBSTRING(name, CHARINDEX(' ', name) + 1, LEN(name)) -- last name
```

With no space `CHARINDEX` is 0 and `LEFT(name, -1)` is an error:
`Invalid length parameter passed to the left function.`

## Showing

| Expression | Result |
|---|---|
| `FORMAT(d, 'dd.MM.yyyy')` | `14.03.2026` |
| `FORMAT(d, 'MMMM yyyy', 'tr-TR')` | `Mart 2026` |
| `FORMAT(d, 'MMMM yyyy', 'en-US')` | `March 2026` |
| `CONVERT(NVARCHAR(10), d, 104)` | `14.03.2026` |

The result is text; it is for showing only, not for sorting or
calculating.
