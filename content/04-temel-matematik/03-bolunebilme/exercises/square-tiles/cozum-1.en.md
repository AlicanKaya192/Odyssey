**What is asked?** The largest square that exactly covers both sides, and how many of those squares are needed.

**Idea:** For square tiles to fit exactly along the short side, the tile side must divide $360$; to fit along the long side, it must divide $840$. The largest number dividing both is the GCD.

**Step 1 — Prime factors.**

$$
\begin{aligned}
360 &= 2^3 \cdot 3^2 \cdot 5 \\
840 &= 2^3 \cdot 3 \cdot 5 \cdot 7
\end{aligned}
$$

**Step 2 — GCD: common primes, smaller exponents.** The common primes are $2$, $3$, $5$ ($7$ is only in $840$):

$$
\text{GCD} = 2^3 \cdot 3 \cdot 5 = 120
$$

The tile side is $120$ cm.

**Step 3 — Tiles per side.** $360 \div 120 = 3$ along the short side, $840 \div 120 = 7$ along the long side.

**Step 4 — Total.**

$$
3 \cdot 7 = 21
$$

**Reading the result:** $3$ and $7$ are coprime; this shows that $120$ really is the largest choice. If they had a common factor, we could enlarge the tile by that much.

**Answer:** $120$ cm; $21$ tiles.
