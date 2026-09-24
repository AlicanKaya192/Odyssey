**What is asked?** A coefficient and a value of the third degree Taylor polynomial of $e^x$.

**Idea:** $P_3(x) = \sum_{k=0}^{3} \frac{f^{(k)}(0)}{k!} x^k$. All derivatives of $e^x$ are $1$ at $0$.

**Step 1 — The coefficients.** $\frac{1}{0!}, \frac{1}{1!}, \frac{1}{2!}, \frac{1}{3!}$: $1, 1, \frac{1}{2}, \frac{1}{6}$. The coefficient of $x^3$ is $\frac{1}{6}$.

**Step 2 — The value.**

$$
\begin{aligned}
P_3(0.5) &= 1 + \frac{1}{2} + \frac{1}{8} + \frac{1}{48} \\
&= \frac{79}{48} \approx 1.6458
\end{aligned}
$$

**Check:** $e^{0.5} \approx 1.6487$; the difference is $0.0029$. The first term left out is $\frac{0.5^4}{24} \approx 0.0026$ ✓.

**Watch out:** Writing $\frac{x^3}{3}$ (a $3$ instead of the factorial) makes the coefficient $\frac{1}{3}$; the denominators grow as $1, 2, 6, 24$.

**Answer:** $\frac{1}{6}$ and $\frac{79}{48}$.
