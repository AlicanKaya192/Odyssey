**Idea:** Without expanding: $L(w) = (2w - 6)^2 = 4(w - 3)^2$. $(w - 3)^2$ is the parabola $w^2$ shifted $3$ units right; its derivative is $2w$ shifted too, $2(w - 3)$.

**Step 1 — The derivative.** $L'(w) = 4 \cdot 2(w - 3) = 8(w - 3)$. $L'(1) = 8 \cdot (-2) = -16$.

**Step 2 — The step.** $w = 1 + 0.05 \cdot 16 = 1.8$.

**Step 3 — The loss.** $4(1.8 - 3)^2 = 4 \cdot 1.44 = 5.76$.

**Why the same result?** $8(w - 3) = 8w - 24$; the two ways found the same derivative in different forms. This form shows one more thing: at every step the gap $w - 3$ shrinks to $1 - 8\eta = 0.6$ times its size ($-2 \to -1.2$). The loss shrinks to $0.6^2 = 0.36$ times: $16 \cdot 0.36 = 5.76$.

**Answer:** $-16$, $1.8$ and $5.76$.
