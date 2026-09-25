**What is asked?** The height of one bounce of a bouncing ball, the distance up to a given moment, and the total distance forever.

**Idea:** The bounce heights form a geometric sequence: $h_k = 54 \cdot \left( \frac{2}{3} \right)^{k - 1}$. The distance is the first fall plus twice each bounce.

**Step 1 — The fourth bounce.** $h_4 = 54 \cdot \left( \frac{2}{3} \right)^3 = 54 \cdot \frac{8}{27} = 16$.

**Step 2 — Up to the fifth touch.** The first touch ends the fall. The next four touches each come after a bounce:

$$
\begin{aligned}
54 + 36 + 24 + 16 &= 130 \\
81 + 2 \cdot 130 &= 341
\end{aligned}
$$

With the series formula as well: $54 \cdot \frac{1 - (2/3)^4}{1 - 2/3} = 54 \cdot \frac{65/81}{1/3} = 130$.

**Step 3 — Forever.** $r = \frac{2}{3}$, so $-1 < r < 1$:

$$
\begin{aligned}
\sum_{k=1}^{\infty} h_k &= \frac{54}{1 - 2/3} = 162 \\
81 + 2 \cdot 162 &= 405
\end{aligned}
$$

**Check:** $341$ up to the fifth touch is less than the infinite total $405$ ✓; the remaining $64$ metres are the later bounces: $2 \cdot \frac{h_5}{1 - 2/3} = 2 \cdot \frac{32/3}{1/3} = 64$ ✓.

**Watch out:** Counting the first $81$ m twice is a common mistake: the ball never went up to that height, it only fell.

**Answer:** $16$ m, $341$ m, $405$ m.
