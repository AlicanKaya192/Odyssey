Some of the traps in writing a recursive query raise an error; others
quietly give a wrong result. This note collects the ones measured in
this section and the fix for each.

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">Wrong direction</span><span class="anat-body">Check which column the join goes from and to.</span></div>
    <div class="anat-row"><span class="anat-label">Type</span><span class="anat-body">When building up text, <code>CAST</code> in both parts.</span></div>
    <div class="anat-row"><span class="anat-label">Stopping condition</span><span class="anat-body">A <code>WHERE</code> in the self-referring part, or a join that runs out.</span></div>
    <div class="anat-row"><span class="anat-label">Limit</span><span class="anat-body">If you will pass 100, <code>OPTION (MAXRECURSION n)</code> at the end of the statement.</span></div>
    <div class="anat-row"><span class="anat-label">Aggregation</span><span class="anat-body">Outside the recursion, not inside.</span></div>
    <div class="anat-row"><span class="anat-label">Semicolon</span><span class="anat-body">End the statement before <code>WITH</code> with <code>;</code>.</span></div>
  </div>
</figure>

## 1. The wrong direction — no error, missing rows

In the downward level query the join has to be `e.manager_id = c.id`:
"the employees whose manager is in the chain". Written the other way
round (`e.id = c.manager_id`), the query brought back only Ada **without
an error**: Ada has no manager, nobody was added to the chain, and the
recursion ended at the first step.

| Direction | Join | Measured |
|---|---|---|
| down (who is below whom) | `e.manager_id = c.id` | 6 employees |
| up (who is above whom) | `e.id = c.manager_id` | Fulya → Emre → Ada |

**Fix:** read it out loud — "the **manager** of the one in the chain", or
"the one whose manager is **in the chain**"?

## 2. Type mismatch

At the start `name` (`NVARCHAR(40)`), in the self-referring part
`c.path + N' > ' + e.name` (a longer type):

`Types don't match between the anchor and the recursive part in column
"path" of recursive query "chain".`

The same happens with numbers: `0` (`INT`) at the start and then
`c.total + x.price` (`DECIMAL`) leaves the two parts with different
types.

**Fix:** the same `CAST` in both parts: `CAST(... AS NVARCHAR(200))`.
Pick a length that fits the longest chain.

## 3. The stopping condition and the limit

In a recursion that generates a counter or dates, you write the stopping
condition (`WHERE k < 200`, `WHERE month < '2026-06-01'`). Forget it and
the server cuts it off at the limit:

| Situation | Measured |
|---|---|
| the default limit | 101 rows passed, at 102 `The maximum recursion 100 has been exhausted` |
| `OPTION (MAXRECURSION 200)` | 200 rows |
| `OPTION (MAXRECURSION 0)` | no limit — 1000 rows |
| no `WHERE`, `MAXRECURSION 50` | stopped at 50 with an error |

In a tree the stopping condition is there by itself: for an employee with
nobody below, the join comes back empty.

**Fix:** in generated series, write the condition first; remove the limit
(`0`) only when you are sure the condition is right.

## 4. Where OPTION goes

Written inside the CTE, `OPTION (MAXRECURSION n)` gave `Incorrect syntax
near the keyword 'OPTION'`. Its place is **the end of the statement**
that uses the CTE:

```sql
WITH n AS (...)
SELECT COUNT(*) FROM n
OPTION (MAXRECURSION 200);
```

## 5. Aggregation inside the recursion

The self-referring part cannot contain `MAX`, `GROUP BY`, `HAVING`
(error 467) or `LEFT JOIN` (error 462).

**Fix:** let the recursion only produce rows; counting and totalling
happen outside. That is how the number of people below each employee
was measured: the recursion listed who is below each root, and the outer
`GROUP BY root` counted (Ada 5, Bora 2, Emre 1).

## 6. UNION ALL, not UNION

Write `UNION` and you get an error: `does not contain a top-level UNION
ALL operator`. If duplicates have to be removed, that is done outside
too (`DISTINCT`).

## 7. The semicolon

The most frequent error in this section is not about recursion but about
`WITH` itself: if the previous statement does not end with `;`, one of
two different messages comes back. Both end up saying the same thing —
finish the previous statement.

## The questions to ask

When you write a recursive query, ask three things:

- **"Which rows are there at the start?"** — run the query before
  `UNION ALL` on its own.
- **"Who is added at each step?"** — read the direction of the join.
- **"When does it stop?"** — in a tree, the data; in a series, your
  `WHERE`.
