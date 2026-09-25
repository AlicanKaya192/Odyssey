**What is asked?** The value of the function at a point and the height of the chord there.

**Idea:** If the function is convex, its value must stay below the chord.

**Step 1 — The midpoint.** $\frac{1}{2} \cdot 0 + \frac{1}{2} \cdot 2 = 1$: $f(1) = e \approx 2.718$.

**Step 2 — The chord.** $\frac{e^0 + e^2}{2} = \frac{1 + 7.389}{2} \approx 4.195$.

**Step 3 — Compare.** $2.718 \le 4.195$ ✓; the chord is about $1.48$ units above.

**Check:** $(e^x)'' = e^x > 0$: $e^x$ is convex everywhere, so the inequality must hold for every $a$, $b$, $t$ ✓.

**Watch out:** Holding in one example does not prove convexity; the proof comes from the second derivative (or from a general argument like the one in the next solution).

**Answer:** $2.718$ and $4.195$.
