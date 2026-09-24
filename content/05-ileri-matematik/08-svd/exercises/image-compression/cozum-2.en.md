**Idea:** Set up the same calculation in general and go one step further: up to which $k$ does compression really save space? Knowing this shows why $k = 30$ is a good choice.

**Step 1 — The general formula.** The rank-$k$ approximation takes $k(m + n + 1)$ numbers, the original $mn$. The ratio:

$$
\frac{k(m + n + 1)}{mn}
$$

**Step 2 — For $k = 30$.**

$$
\begin{aligned}
\frac{30 \cdot 1001}{400 \cdot 600} &= \frac{30\,030}{240\,000} \\
&\approx 0.125
\end{aligned}
$$

That is 12.5%; the number stored is $30\,030$.

**Step 3 — The break-even point.** The gain ends when the ratio reaches $1$:

$$
\begin{aligned}
k(m + n + 1) &= mn \\
k &= \frac{240\,000}{1001} \approx 240
\end{aligned}
$$

Beyond $k \approx 240$, storing the layers takes more space than the original. This matrix has at most $400$ singular values (rank $\le \min(400, 600)$); the first 30 are an eighth of the break-even point.

**Why does it work?** The gain comes from describing each layer with $m + n + 1$ numbers instead of $m \times n$. As long as few layers are kept, the saving is huge.

**Answer:** $30\,030$ and $12.5$.
