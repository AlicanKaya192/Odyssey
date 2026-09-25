**What is asked?** Derivatives in a graph with multiplication, max and branching.

**Idea:** The final addition distributes the gradient $1$ to both branches. In the multiplication branch the inputs are swapped; in the max branch the gradient goes only to the winner. $y$ appears in both branches: its contributions add up.

**Step 1 — Forward.** $xy = -6$, $\max(-2, 1) = 1$, $f = -5$.

**Step 2 — The multiplication branch.** Incoming $1$: to $x$, $y = -2$; to $y$, $x = 3$.

**Step 3 — The max branch.** Incoming $1$: the winner is $z$, which gets $1$; $y$ gets $0$.

**Step 4 — Add up.** $\frac{\partial f}{\partial x} = -2$, $\frac{\partial f}{\partial y} = 3 + 0 = 3$, $\frac{\partial f}{\partial z} = 1$.

**Check:** Increase $y$ by $0.01$: $xy = -5.97$ and the max is still $1$; $f = -4.97$, change $0.03 / 0.01 = 3$ ✓.

**Watch out:** Sending the max node's gradient to both inputs gives $\frac{\partial f}{\partial y} = 4$; since $y$ does not win the max, it gets nothing from there.

**Answer:** $-2$, $3$ and $1$.
