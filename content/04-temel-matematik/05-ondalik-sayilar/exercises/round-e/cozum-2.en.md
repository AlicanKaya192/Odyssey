**Idea:** Go back to what rounding means: at the required place there are two candidates (below and above); the one nearer the number is chosen.

**Step 1 — Two places.** The candidates are $2.71$ and $2.72$. The distances:

$$
\begin{aligned}
2.718\dots - 2.71 &\approx 0.008 \\
2.72 - 2.718\dots &\approx 0.002
\end{aligned}
$$

$2.72$ is nearer.

**Step 2 — Three places.** The candidates are $2.718$ and $2.719$. $e$ is only $0.000\,28$ above $2.718$, below the midpoint $2.718\,5$. $2.718$ is nearer.

**Step 3 — Four places.** The candidates are $2.7182$ and $2.7183$. The midpoint is $2.718\,25$; $e = 2.718\,28\dots$ is **above** it. $2.7183$ is nearer.

**Why the same result?** The rule "if the next digit is $5$ or more, round up" is a shortcut for asking whether the number is past the midpoint. The midpoint always has a $5$ in the next place.

**Answer:** $2.72$; $2.718$; $2.7183$.
