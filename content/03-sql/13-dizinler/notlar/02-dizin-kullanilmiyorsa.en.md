You created an index and the query is still slow. In the cases measured
in this section the cause was always one of these six. None of them
raises an error — the query brings back the right result, only by
reading the table from start to end.

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">A function</span><span class="anat-body">The column is inside a function: <code>YEAR(created_at)</code>, <code>UPPER(session_code)</code>.</span></div>
    <div class="anat-row"><span class="anat-label">A leading %</span><span class="anat-body"><code>LIKE '%0050'</code> cannot be sought in a sorted list.</span></div>
    <div class="anat-row"><span class="anat-label">No first column</span><span class="anat-body">The composite index's first column does not appear in <code>WHERE</code>.</span></div>
    <div class="anat-row"><span class="anat-label">Too many trips back</span><span class="anat-body">The columns asked for are not in the index and there are many rows.</span></div>
    <div class="anat-row"><span class="anat-label">Low selectivity</span><span class="anat-body">The value searched for is a large part of the table.</span></div>
    <div class="anat-row"><span class="anat-label">The filter does not fit</span><span class="anat-body">The rows searched for are not in the filtered index.</span></div>
  </div>
</figure>

## 1. A function

| `WHERE` | Reads |
|---|---|
| `created_at >= '2025-06-01' AND created_at < '2025-06-02'` | 2 |
| `YEAR(created_at) = 2025 AND MONTH(...) = 6 AND DAY(...) = 1` | 42 |
| `DATEADD(day, 1, created_at) >= ...` | 42 |
| `UPPER(session_code) = 'S010000'` | 54 |

**Fix:** take the function off the column and write it on the other
side. Instead of `YEAR = 2025`, `>= '2025-01-01' AND < '2026-01-01'`.
For letter case there is no need on this server anyway: comparisons
ignore case (the tenth section).

`CAST(created_at AS DATE) = '2025-06-01'` is an exception: it sought in 2
reads. Following the rule gives fewer surprises than relying on the
exception.

## 2. A leading %

`LIKE 'S0050%'` 3 reads, `LIKE '%0050'` 54. A text whose beginning is not
known cannot be sought in a sorted list.

**Fix:** search from the beginning if you can. If searching from the end
is really needed, there are other tools outside this section's scope
(like full-text search).

## 3. No first column in a composite index

With a `(customer_id, created_at)` index, searching by `created_at` alone
took 52 reads — the whole index. With the same index, searching by
`customer_id` alone took 11.

**Fix:** build the index for the query. Whichever column is also searched
on its own should come first.

## 4. Too many trips back

With a `created_at` index, `SELECT *` for one day's 58 rows scanned the
table (150 reads), while a 15-row query used the index and went back to
the table for each row (130 reads). As the number of trips back grows,
the server chooses the scan.

**Fix:** write the columns you need instead of `SELECT *`; for a query
that runs often, add the needed columns to the index with `INCLUDE`
(150 → 3).

## 5. Low selectivity

`event_type` takes four values. `'purchase'` is 5,000 rows: `SELECT id`
came from the index in 22 reads, `SELECT *` scanned the table.

**Fix:** build indexes on columns that rule out many rows. A column with
few values on its own is more useful as the second column of a
composite index.

## 6. The filter does not fit

With an index filtered by `WHERE amount IS NOT NULL`, `amount > 490`
took 2 reads; `amount IS NULL` 150 — those rows are not in the index.

**Fix:** build a filtered index for the part that queries always look
for.

## One more thing: the number of indexes

Every index makes writing more expensive: a single-row `INSERT` went from
2 reads to 22 with five indexes. An index that is never used is only a
cost.

## The questions to ask

If a query is slow, ask in order:

- **Is the column bare?** Is the column itself in the `WHERE`, or the
  result of a function?
- **Does the index's first column appear in the query?**
- **How many rows come back, and are the requested columns in the
  index?**
