A one-page list of the functions in this section. All of them were
measured on SQL Server; the values in the result column are real output.

## Text

| Function | Example | Result |
|---|---|---|
| `LEN` | `LEN('Keyboard')` | `6` |
| `LEN` (trailing space) | `LEN('abc   ')` | `3` |
| `LEN` (leading space) | `LEN('   abc')` | `6` |
| `DATALENGTH` | `DATALENGTH('abc   ')` | `6` |
| `UPPER` / `LOWER` | `UPPER('abc')` | `ABC` |
| `TRIM` | `TRIM('  abc  ')` | `abc` |
| `LTRIM` / `RTRIM` | `RTRIM('abc  ')` | `abc` |
| `LEFT` | `LEFT('Keyboard', 3)` | `Kla` |
| `RIGHT` | `RIGHT('Keyboard', 3)` | `vye` |
| `SUBSTRING` | `SUBSTRING('Keyboard', 2, 3)` | `lav` |
| `REPLACE` | `REPLACE('Keyboard','a','A')` | `KlAvye` |
| `CONCAT` | `CONCAT('a', NULL, 'b')` | `ab` |

In `SUBSTRING`, counting starts at **1**. Most programming languages start
at 0, so this gets mixed up often.

That `LEN` ignores trailing spaces but counts leading ones is a quirk
rather than a design decision — behaviour inherited from older versions.

## Numbers

| Function | Example | Result |
|---|---|---|
| `ROUND` | `ROUND(2.5, 0)` | `3` |
| `ROUND` | `ROUND(3.5, 0)` | `4` |
| `ROUND` | `ROUND(2.345, 2)` | `2.35` |
| `CEILING` | `CEILING(2.1)` | `3` |
| `FLOOR` | `FLOOR(2.9)` | `2` |
| `ABS` | `ABS(-5)` | `5` |

`ROUND` rounds halves **away from zero**. Python's `round` rounds to even
(`round(2.5)` is 2), so the same calculation can differ between the two
languages. When report numbers do not match, this is one of the places to
look.

## Converting types

| Function | Input | Result |
|---|---|---|
| `CAST` | `CAST('12' AS INT)` | `12` |
| `CAST` | `CAST('abc' AS INT)` | **error** |
| `TRY_CAST` | `TRY_CAST('abc' AS INT)` | `NULL` |

When `CAST` cannot convert, **the whole query fails**. A single bad row
stops the entire report. `TRY_CAST` gives `NULL` on that row and carries
on.

There is also `CONVERT`, specific to SQL Server and useful for formatting
dates. `CAST` is standard SQL and the portable one.

## Filling gaps

| Function | Example | Result |
|---|---|---|
| `ISNULL` | `ISNULL(NULL, 'none')` | `none` |
| `COALESCE` | `COALESCE(NULL, NULL, 'c')` | `c` |
| `NULLIF` | `NULLIF(5, 5)` | `NULL` |

`ISNULL` takes two values and is specific to SQL Server. `COALESCE` takes
as many as you like and is standard.

`NULLIF` works the other way: it turns a value into `NULL`. Its most
common use is preventing division by zero — in `a / NULLIF(b, 0)`, when
`b` is zero the result is `NULL` instead of an error.

## Two rules of arithmetic

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">Integer division</span><span class="anat-body"><code>7 / 2</code> → <b>3</b>. When both sides are integers the result is an integer and the fraction is <b>thrown away</b>. Make one side fractional: <code>7.0 / 2</code> → 3.5</span></div>
    <div class="anat-row"><span class="anat-label">NULL is contagious</span><span class="anat-body"><code>5 + NULL</code> → <b>NULL</b>. Any operation containing an empty value produces an empty result.</span></div>
  </div>
</figure>

## The difference between `+` and `CONCAT`

| Expression | Result |
|---|---|
| `'a' + 'b'` | `ab` |
| `'a' + NULL` | `NULL` |
| `'a' + 1` | **error** |
| `CONCAT('a', NULL, 'b')` | `ab` |
| `CONCAT('a', 1)` | `a1` |

`CONCAT` both skips `NULL` and converts numbers to text itself. It should
be your default choice for joining text.
