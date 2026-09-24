**Idea:** The question only asks for the solution with $z = 1$. Substituting $z$ first brings the number of unknowns down to two; three equations in two unknowns remain. If the system really has infinitely many solutions, these three equations must be **consistent**.

**Step 1 — Put in $z = 1$ and move the constants to the right.**

$$
\begin{aligned}
x + y + 2 = 5 \;&\Rightarrow\; x + y = 3 \\
2x + 3y + 3 = 13 \;&\Rightarrow\; 2x + 3y = 10 \\
x + 2y + 1 = 8 \;&\Rightarrow\; x + 2y = 7
\end{aligned}
$$

**Step 2 — Solve the first two.** From the first, $x = 3 - y$; put it into the second:

$$
\begin{aligned}
2(3 - y) + 3y &= 10 \\
6 + y &= 10 \\
y &= 4
\end{aligned}
$$

and $x = 3 - 4 = -1$.

**Step 3 — Test with the third equation.** $x + 2y = -1 + 8 = 7$ ✓. The third equation holds too; the system is consistent.

**Why does it work?** Giving the free variable a value means picking one point from the infinite solution set. Giving $z$ another value (say $0$) would give another point, $(2, 3, 0)$, which is also a solution.

**Watch out:** This shortcut only works if $z$ really is free. In a system with a single solution, giving $z$ an arbitrary value makes the remaining three equations contradict each other.

**Answer:** $x = -1$, $y = 4$.
