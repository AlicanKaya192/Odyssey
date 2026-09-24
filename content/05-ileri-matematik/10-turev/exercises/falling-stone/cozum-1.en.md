**What is asked?** The average speed over an interval and the speed at an instant.

**Idea:** Average speed is the slope of the secant; instantaneous speed is the limit of this slope as the interval shrinks to zero, that is, the derivative.

**Step 1 — The average.** $s(1) = 5$, $s(3) = 45$: $\frac{45 - 5}{3 - 1} = 20$.

**Step 2 — The instantaneous speed.**

$$
\begin{aligned}
\frac{s(3 + h) - s(3)}{h} &= \frac{5(9 + 6h + h^2) - 45}{h} \\
&= 30 + 5h \;\to\; 30
\end{aligned}
$$

**Check:** $s'(t) = 10t$ (from the definition, $5 \cdot 2t$), $s'(3) = 30$ ✓. An interesting detail: the average speed $20$ equals the instantaneous speed at the middle of the interval, $s'(2) = 20$; this always happens for parabolas.

**Watch out:** Taking the average speed to be the mean of the speeds at the two ends ($\frac{10 + 30}{2} = 20$) happens to work here; the general method is distance over time.

**Answer:** $20$ m/s and $30$ m/s.
