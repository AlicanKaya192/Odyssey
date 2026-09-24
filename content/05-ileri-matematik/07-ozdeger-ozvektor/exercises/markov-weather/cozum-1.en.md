**What is asked?** The values the weather probabilities settle into after a very long time, and how fast they get there.

**Idea:** If today's probabilities are $\mathbf{p}$, tomorrow's are $M\mathbf{p}$. In the long run the probabilities **do not change** from one day to the next: $M\mathbf{p} = \mathbf{p}$. That is the eigenvector of $M$ with eigenvalue $1$.

**Step 1 — $(M - I)\mathbf{p} = \mathbf{0}$.**

$$
M - I = \begin{bmatrix} -0.1 & 0.5 \\ 0.1 & -0.5 \end{bmatrix}
$$

The first row: $-0.1x + 0.5y = 0$, so $x = 5y$. (The second row gives the same information.)

**Step 2 — The eigenvector.** Choosing $y = 1$ gives $(5, 1)$.

**Step 3 — Turn it into probabilities.** The components must add up to $1$; divide $(5, 1)$ by its sum ($6$):

$$
\mathbf{p} = \left( \frac{5}{6},\ \frac{1}{6} \right) \approx (0.833,\ 0.167)
$$

**Check:** The first component of $M\mathbf{p}$ is $0.9 \cdot \tfrac{5}{6} + 0.5 \cdot \tfrac{1}{6} = \tfrac{4.5 + 0.5}{6} = \tfrac{5}{6}$ ✓.

**Step 4 — The other eigenvalue.** The eigenvalues add up to the trace: $1 + \lambda_2 = 0.9 + 0.5 = 1.4$, so $\lambda_2 = 0.4$. Check with the product: $1 \cdot 0.4 = 0.4$ and $\det M = 0.45 - 0.05 = 0.4$ ✓.

**Reading the result:** Whatever the start, since $0.4^k$ goes to zero fast, after a few weeks about 83% of days are sunny. The share of the initial difference left after one day is $0.4$; after a week $0.4^7 \approx 0.002$.

**Answer:** $\tfrac{5}{6}$ (about $0.83$) and $0.4$.
