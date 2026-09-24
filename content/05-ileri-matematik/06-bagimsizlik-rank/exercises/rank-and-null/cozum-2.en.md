**Idea:** $A\mathbf{x} = \mathbf{0}$ means $x \cdot (\text{column 1}) + y \cdot (\text{column 2}) + z \cdot (\text{column 3}) = \mathbf{0}$. So the null space is looking for dependences among the columns. Let us look at the columns directly.

**Step 1 — Write the columns.**

$$
\begin{aligned}
\mathbf{a}_1 &= (1, 2, 1) \\
\mathbf{a}_2 &= (2, 4, 1) \\
\mathbf{a}_3 &= (3, 6, 1)
\end{aligned}
$$

**Step 2 — Are the first two independent?** $\mathbf{a}_2$ is not a multiple of $\mathbf{a}_1$ (twice in the 1st component, once in the 3rd). They are independent: the rank is at least 2.

**Step 3 — Is the third a combination of the first two?** Look for $\mathbf{a}_3 = p\,\mathbf{a}_1 + q\,\mathbf{a}_2$. The 1st and 3rd components:

$$
\begin{aligned}
p + 2q &= 3 \\
p + q &= 1
\end{aligned}
$$

Subtracting gives $q = 2$, then $p = -1$. Test with the 2nd component: $-1 \cdot 2 + 2 \cdot 4 = 6$ ✓. So $\mathbf{a}_3 = -\mathbf{a}_1 + 2\mathbf{a}_2$: the third column is redundant and the rank is exactly $2$.

**Step 4 — Turn the relation into a null-space vector.** Move everything to one side:

$$
\mathbf{a}_1 - 2\mathbf{a}_2 + \mathbf{a}_3 = \mathbf{0}
$$

The coefficients are $(1, -2, 1)$: this vector is in the null space, and it is exactly the solution with $z = 1$.

**Why does it work?** Null-space vectors are "recipes" that send the columns to zero. The first method found this recipe by elimination, this one by looking straight at the columns.

**Answer:** $2$; $x = 1$, $y = -2$.
