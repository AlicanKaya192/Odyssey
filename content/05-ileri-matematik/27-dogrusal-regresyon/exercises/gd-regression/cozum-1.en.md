**What is asked?** One step of gradient descent on the linear regression loss, and where it will end up.

**Idea:** $w \leftarrow w - \eta J'(w)$; $J'(w^*) = 0$.

**Step 1 — Gradient.** $J'(w) = -2 \cdot 22 + 2w \cdot 14 = -44 + 28w$. $J'(0) = -44$.

**Step 2 — One step.** $w_1 = 0 - 0.01 \cdot (-44) = 0.44$.

**Step 3 — Target.** $-44 + 28w = 0$, $w^* = \frac{22}{14} \approx 1.571$.

**Check:** $J'(0.44) = -44 + 12.32 = -31.68 < 0$; we still need to move right, $w^*$ is further right ✓.

**Watch out:** The sign of the gradient: a negative gradient says $w$ must increase; the minus-sign update does this.

**Answer:** $-44$, $0.44$, $\approx 1.571$.
