For every manager with at least one employee below them, show the size of
their team and the revenue the team brought in. The team is **everyone**
below the manager: direct and indirect, not counting themselves. The
revenue comes from orders that were not cancelled; a team with no sales
has `0`.

Columns: `name`, `team_size`, `team_revenue`. Sort by `team_revenue`
(largest first), then `name`.

```
name         team_size  team_revenue
-----------  ---------  ------------
Ada Kilic    5          72615.00
Bora Yilmaz  2          72615.00
Emre Sahin   1          0.00
```

Only Ceren and Deniz make sales; both are in Bora's team, and Bora is in
Ada's — that is why the two teams show the same revenue. Fulya, Emre's
only employee, has no sales. Sections: recursive `WITH` (12), `LEFT
JOIN` (06), grouping (05).
