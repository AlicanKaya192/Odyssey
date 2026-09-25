**What is asked?** Derivatives in a graph where two inputs reach the output through two separate intermediate values.

**Idea:** Each input's gradient is the sum of the contributions of all roads to the output.

**Step 1 — Forward.** $s = 4$, $d = 2$, $g = 8$.

**Step 2 — The multiplication.** $\frac{\partial g}{\partial s} = d = 2$, $\frac{\partial g}{\partial d} = s = 4$.

**Step 3 — $x$.** From the $s$ road $2 \cdot 1$, from the $d$ road $4 \cdot 1$: total $6$.

**Step 4 — $y$.** From the $s$ road $2 \cdot 1$, from the $d$ road $4 \cdot (-1)$: total $-2$.

**Check:** The subtraction node flips the sign of the gradient for its second input ($g$, $-g$ for $a - b$) ✓.

**Watch out:** Computing along only one road gives $\frac{\partial g}{\partial x}$ as $2$ or $4$; both are incomplete.

**Answer:** $6$ and $-2$.
