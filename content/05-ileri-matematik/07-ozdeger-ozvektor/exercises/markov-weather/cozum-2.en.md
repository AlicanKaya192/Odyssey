**Idea:** Let the long-run share of sunny days be $s$ (rainy days $1 - s$). If the share of sunny days does not change from one day to the next, the probability of tomorrow being sunny must also be $s$. This single equation is enough, without writing the eigenvector.

**Step 1 — The probability that tomorrow is sunny.** If today is sunny (probability $s$) tomorrow is sunny with $0.9$; if rainy (probability $1 - s$), with $0.5$:

$$
0.9\,s + 0.5\,(1 - s)
$$

**Step 2 — Set it equal to the balance.**

$$
\begin{aligned}
0.9\,s + 0.5\,(1 - s) &= s \\
0.9\,s + 0.5 - 0.5\,s &= s \\
0.5 &= s - 0.4\,s \\
0.5 &= 0.6\,s \\
s &= \frac{5}{6}
\end{aligned}
$$

**Step 3 — The other eigenvalue, from the determinant.** The product of the eigenvalues is the determinant:

$$
\det M = 0.9 \cdot 0.5 - 0.5 \cdot 0.1 = 0.45 - 0.05 = 0.4
$$

One eigenvalue is $1$, so the other is $0.4$.

**Why the same result?** The balance equation is the first row of $M\mathbf{p} = \mathbf{p}$ with $\mathbf{p} = (s, 1 - s)$. The sum-to-one condition was built in from the start, so no division was needed afterwards.

**Why is 1 always an eigenvalue?** Every column adds up to $1$ (the next day always has some weather). That means $M^\mathsf{T}(1, 1) = (1, 1)$; since $M^\mathsf{T}$ and $M$ have the same eigenvalues, $1$ is an eigenvalue of $M$ too.

**Answer:** $\tfrac{5}{6}$ and $0.4$.
