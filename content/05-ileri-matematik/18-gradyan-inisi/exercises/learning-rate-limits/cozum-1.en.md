**What is asked?** For which values the learning rate works on a parabola.

**Idea:** One step multiplies $w$ by $1 - \eta\lambda$; $\lambda = L'' = 6$.

**Step 1 — The limit.** $\lvert 1 - 6\eta \rvert < 1 \Leftrightarrow 0 < \eta < \frac{1}{3}$.

**Step 2 — $\eta = 0.3$.** $1 - 1.8 = -0.8$: the sign flips each step and the size shrinks to $0.8$ times. It converges with swings.

**Step 3 — One step.** $1 - 6\eta = 0$: $\eta = \frac{1}{6}$.

**Check:** $\eta = 0.4 > \frac{1}{3}$: the factor is $-1.4$ and $w$ grows ✓ (divergence).

**Watch out:** $\eta = \frac{1}{3}$ is exactly on the edge: the factor is $-1$ and $w$ bounces between two values forever; it does not converge.

**Answer:** $\frac{1}{3}$, $-0.8$ and $\frac{1}{6}$.
