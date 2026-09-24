**Idea:** The slope is how much the prediction changes when $x$ goes up by one. Once we have it, we can fill in the predictions by walking one unit at a time.

**Step 1 — The change per unit.** As $x$ goes from $2$ to $6$, up $4$ units, the prediction goes from $7$ to $19$, up $12$. Per unit $12 / 4 = 3$: $w = 3$.

**Step 2 — Walking back.** Two units back from $x = 2$ to $x = 0$: $7 - 2 \cdot 3 = 1$. The prediction at $x = 0$ is $b$ itself: $b = 1$.

**Step 3 — Walking forward.** Two units forward from $x = 2$ to $x = 4$: $7 + 2 \cdot 3 = 13$. The true value is $15$, so the error is $2$.

**Why the same result?** In a linear model every unit step adds the same $w$ to the prediction; the slope formula finds this constant step by dividing the total change by the number of steps. And $b$ is by definition the value at $x = 0$.

**Answer:** $3$, $1$ and $2$.
