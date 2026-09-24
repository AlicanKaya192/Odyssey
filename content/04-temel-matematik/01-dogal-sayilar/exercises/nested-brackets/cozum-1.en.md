**What is asked?** The value of an expression with nested brackets.

**Idea:** With nested brackets you start with the innermost one. The order of operations holds **inside** every bracket too: exponent first, then multiplication, finally addition and subtraction.

**Step 1 — The innermost bracket: $(15 - 3 \cdot 4)$.** Inside it, multiplication comes before subtraction:

$$
15 - 3 \cdot 4 = 15 - 12 = 3
$$

The expression is now:

$$
100 - [4 \cdot 3 + 2^3]
$$

**Step 2 — Inside the square bracket.** Exponent first, then multiplication, finally addition:

$$
\begin{aligned}
4 \cdot 3 + 2^3 &= 4 \cdot 3 + 8 \\
&= 12 + 8 = 20
\end{aligned}
$$

**Step 3 — The outer operation.**

$$
100 - 20 = 80
$$

**Watch out:** Doing the innermost bracket left to right, $(15 - 3) \cdot 4 = 48$, is the most common slip; multiplication comes first inside the bracket too. Another trap is taking $2^3$ to be $2 \cdot 3 = 6$.

**Answer:** $80$.
