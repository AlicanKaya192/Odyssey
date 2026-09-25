**Idea:** If the infinite reward sum is $V$, everything after the first step is again the same sum times $\gamma$: $V = 2 + \gamma V$. This is the simplest form of the Bellman equation in reinforcement learning.

**Step 1 — MSE.** As in the first solution: $\frac{1 + 0 + 4 + 1}{4} = 1.5$.

**Step 2 — $V$.** $V = 2 + 0.8 V$, so $0.2 V = 2$ and $V = 10$.

**Step 3 — The weights.** The sum of all the weights is $W = (1 - \beta) + \beta W$, so $W = 1$. Everything after the first three is $\beta^3 W = 0.125$; the first three make $1 - 0.125 = 0.875$.

**Why the same result?** The equality "$S = a_1 + rS$" is another way of writing the geometric series trick $S - rS = a_1$. An infinite sum contains a shrunken copy of itself; that is how to use the formula without memorising it.

**Answer:** $1.5$, $10$ and $0.875$.
