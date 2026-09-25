**Idea:** $x(2 - x)$ is a parabola with its top at $x = 1$ and zeros at $0$ and $2$; it is symmetric about $1$.

**Step 1 — $c$.** The area under a parabola is $\frac{2}{3}$ of the $2 \times 1$ rectangle around it: $\frac{2}{3} \cdot 2 = \frac{4}{3}$. $c = \frac{3}{4}$.

**Step 2 — $E[X]$.** The density is symmetric about $x = 1$; the point where the probability mass balances is $1$.

**Step 3 — The probability.** Symmetry is not enough here; the area needs the integral: $\frac{5}{32}$. Symmetry still gives a check: $P(X \geq 1.5)$ is also $\frac{5}{32}$, and the middle interval $[0.5, 1.5]$ has $1 - \frac{10}{32} = \frac{11}{16}$.

**Why the same result?** The expected value of a symmetric density is its point of symmetry: in $\int (x - 1) f(x) dx$ the two sides contribute equal amounts with opposite signs. The $\frac{2}{3}$ rule for a parabola's area is a geometric result of the same integral.

**Answer:** $\frac{3}{4}$, $1$ and $\frac{5}{32}$.
