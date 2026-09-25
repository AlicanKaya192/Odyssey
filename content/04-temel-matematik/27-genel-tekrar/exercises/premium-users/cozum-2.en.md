**Idea:** Draw the three users one after another; in the tree multiply along paths and add the matching ones.

**Step 1 — At least one.** Only one path does not match: none premium, $0.7 \cdot 0.7 \cdot 0.7$. The rest of the paths give $1 - 0.343 = 0.657$.

**Step 2 — Exactly one.** The matching paths are PNN, NPN, NNP; each $0.147$: $0.441$.

**Step 3 — Without replacement.** No premium at all: $\frac{7}{10} \cdot \frac{6}{9} \cdot \frac{5}{8} = \frac{210}{720} = \frac{7}{24}$. At least one: $1 - \frac{7}{24} = \frac{17}{24}$.

**Why the same result?** $\frac{7}{10} \cdot \frac{6}{9} \cdot \frac{5}{8}$ is the same fraction as $\frac{\binom{7}{3}}{\binom{10}{3}}$; one counts in order and the other without, and in both the ordering factor cancels between top and bottom.

**Answer:** $0.657$, $0.441$ and $\frac{17}{24}$.
