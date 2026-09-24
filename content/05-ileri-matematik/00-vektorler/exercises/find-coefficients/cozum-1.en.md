**What is asked?** Taking $a$ copies of $(1, 2)$ and $b$ copies of $(3, 1)$ and adding them gives $(7, 9)$. We want these "how many" numbers, $a$ and $b$.

**Idea:** Two vectors are equal only when every component is equal. Expanding the left side and matching it with the right side gives two equations in two unknowns. Then we isolate one unknown and put it into the other equation (substitution).

**Step 1 — Expand the left side.** Scale first, then add:

$$
\begin{aligned}
a\,(1, 2) + b\,(3, 1) &= (a,\ 2a) + (3b,\ b) \\
&= (a + 3b,\ 2a + b)
\end{aligned}
$$

**Step 2 — Match the components.** For this vector to be $(7, 9)$, both components must agree:

$$
\begin{aligned}
a + 3b &= 7 \quad (x \text{ component}) \\
2a + b &= 9 \quad (y \text{ component})
\end{aligned}
$$

**Step 3 — Isolate one unknown.** In the second equation $b$ has no number in front (its coefficient is 1), so it is the easiest to isolate:

$$
b = 9 - 2a
$$

**Step 4 — Put it into the first equation.** Writing $9 - 2a$ in place of $b$ leaves a single unknown:

$$
\begin{aligned}
a + 3(9 - 2a) &= 7 \\
a + 27 - 6a &= 7 \\
-5a &= 7 - 27 \\
-5a &= -20 \\
a &= 4
\end{aligned}
$$

**Step 5 — Find $b$.** Put $a = 4$ into the formula from Step 3: $b = 9 - 2 \cdot 4 = 1$.

**Check:** Put the values into the original equation:

$$
\begin{aligned}
4\,(1, 2) + 1\,(3, 1) &= (4, 8) + (3, 1) \\
&= (7, 9)
\end{aligned}
$$

It holds. ✓

**Answer:** $a = 4$, $b = 1$.
