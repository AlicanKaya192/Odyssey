**What is asked?** The last term of an arithmetic sequence, its sum, and where it first passes a bound.

**Idea:** The rows form an arithmetic sequence with $a_1 = 12$, $d = 3$. The general term is $a_n = 12 + 3(n - 1)$ and the sum $\frac{n(a_1 + a_n)}{2}$.

**Step 1 — The last row.** $a_{20} = 12 + 19 \cdot 3 = 69$.

**Step 2 — The total.**

$$
S_{20} = \frac{20 \cdot (12 + 69)}{2} = 10 \cdot 81 = 810
$$

**Step 3 — The row above $50$.**

$$
\begin{aligned}
12 + 3(n - 1) &> 50 \\
3(n - 1) &> 38 \\
n - 1 &> 12.67
\end{aligned}
$$

The smallest whole number is $n - 1 = 13$, so $n = 14$. $a_{13} = 48$, $a_{14} = 51$.

**Check:** $a_{14} = 12 + 13 \cdot 3 = 51 > 50$ ✓ and $a_{13} = 48 \leq 50$ ✓.

**Watch out:** The twentieth row is reached in $19$ steps. Writing $12 + 20 \cdot 3 = 72$ would compute one row too many.

**Answer:** $69$ seats, $810$ in total, row $14$.
