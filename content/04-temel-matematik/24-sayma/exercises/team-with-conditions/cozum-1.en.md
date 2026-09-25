**What is asked?** The numbers of teams with no condition, with an exact condition and with an "at least" condition.

**Idea:** When the choice splits into groups, each group is chosen separately and the counts multiply. For "at least one" it is easier to count the opposite.

**Step 1 — All teams.** $4$ from $12$: $\binom{12}{4} = 495$.

**Step 2 — Exactly $2$ women.** $\binom{5}{2} \cdot \binom{7}{2} = 10 \cdot 21 = 210$.

**Step 3 — At least $1$ woman.** Teams with no women, only men: $\binom{7}{4} = 35$. $495 - 35 = 460$.

**Check:** Teams with $0$, $1$, $2$, $3$, $4$ women: $35 + 175 + 210 + 70 + 5 = 495$ ✓.

**Watch out:** Choosing one woman first ($5$) and then $3$ from the other $11$ ($5 \cdot 165 = 825$) counts the same teams many times: a team with two women is counted twice, once for each woman picked "first".

**Answer:** $495$, $210$, $460$.
