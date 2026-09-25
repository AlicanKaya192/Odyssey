**Idea:** "At least one woman" means "exactly $1$, $2$, $3$ or $4$ women". These cases do not overlap; the addition principle adds them.

**Step 1 — All teams.** $\binom{12}{4} = 495$.

**Step 2 — The cases.**

| Women | Men | Count |
|---|---|---|
| $1$ | $3$ | $\binom{5}{1}\binom{7}{3} = 5 \cdot 35 = 175$ |
| $2$ | $2$ | $\binom{5}{2}\binom{7}{2} = 10 \cdot 21 = 210$ |
| $3$ | $1$ | $\binom{5}{3}\binom{7}{1} = 10 \cdot 7 = 70$ |
| $4$ | $0$ | $\binom{5}{4} = 5$ |

**Step 3 — Add.** $175 + 210 + 70 + 5 = 460$.

**Why the same result?** All teams split into non-overlapping parts by the number of women, $0$ to $4$; adding every part except "$0$ women" is the same as taking that part away from the whole. The complement way does it in one calculation.

**Answer:** $495$, $210$ and $460$.
