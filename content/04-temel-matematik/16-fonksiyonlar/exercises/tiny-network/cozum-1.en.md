**What is asked?** The output of a small network that is a composition of functions.

**Idea:** The network is a composition: $y = g(\text{ReLU}(f(x)))$, where $f(x) = 2x - 3$ and $g(h) = 3h + 1$. We work from the inside out; ReLU only sets negatives to zero.

**Step 1 — $x = 4$, inner layer.** $2 \cdot 4 - 3 = 5$; $\text{ReLU}(5) = 5$, so $h = 5$.

**Step 2 — Outer layer.** $y = 3 \cdot 5 + 1 = 16$.

**Step 3 — $x = 1$, inner layer.** $2 \cdot 1 - 3 = -1$; $\text{ReLU}(-1) = 0$, so $h = 0$.

**Step 4 — Outer layer.** $y = 3 \cdot 0 + 1 = 1$.

**Reading the result:** For every input with $2x - 3 < 0$, that is $x < 1.5$, the network gives the same output ($1$): ReLU "switches off" that region. For $x \ge 1.5$, $y = 3(2x - 3) + 1 = 6x - 8$, a line. The network's graph is a line that bends at $x = 1.5$.

**Watch out:** Skipping ReLU and getting $y = 3(2 \cdot 1 - 3) + 1 = -2$ forgets to zero the inner layer's negative output.

**Answer:** $16$ and $1$.
