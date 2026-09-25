**What is asked?** The derivatives of a small expression with respect to three inputs, using the computational graph.

**Idea:** Compute the intermediate values in the forward pass; in the backward pass start with $1$ and multiply by the local derivative at each node.

**Step 1 — Forward.** $q = 3$, $f = 3 \cdot (-4) = -12$.

**Step 2 — The multiplication node.** Incoming $1$. To $q$: $1 \cdot z = -4$; to $z$: $1 \cdot q = 3$.

**Step 3 — The addition node.** Incoming $-4$; unchanged to $x$ and $y$: $-4$, $-4$.

**Check:** Increase $x$ by $0.01$: $f = (3.01)(-4) = -12.04$; the change is $-0.04 / 0.01 = -4$ ✓.

**Watch out:** The addition node does not split the gradient; it gives the whole of it to both.

**Answer:** $-4$, $-4$ and $3$.
