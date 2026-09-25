**Idea:** Build a four-cell table: $A$ yes/no, $B$ yes/no. The margins come from what is given.

**Step 1 — The table.** Row $A$ adds up to $0.6$, column $B$ to $0.5$, everything to $1$. The "neither" cell is $1 - 0.8 = 0.2$.

| | $B$ | $B'$ | total |
|---|---|---|---|
| $A$ | $0.3$ | $0.3$ | $0.6$ |
| $A'$ | $0.2$ | $0.2$ | $0.4$ |
| total | $0.5$ | $0.5$ | $1$ |

If row $A'$ is $0.4$ and its $B'$ cell is $0.2$, then $A' \cap B = 0.2$; if column $B$ is $0.5$, then $A \cap B = 0.3$.

**Step 2 — Conditional.** The share of $A$ within column $B$: $\frac{0.3}{0.5} = 0.6$.

**Step 3 — Neither.** From the table, $0.2$.

**Why the same result?** Every row and column of the table is the numerical form of the union, intersection and complement rules. Independence shows in the table too: row $A$ splits $0.5$ to $0.5$ between $B$ and $B'$, just like the whole table.

**Answer:** $0.3$, $0.6$ and $0.2$.
