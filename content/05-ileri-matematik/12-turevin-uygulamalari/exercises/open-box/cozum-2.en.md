**Idea:** Expand the volume as a polynomial, differentiate with the power rule, then confirm with the second derivative.

**Step 1 — Expand.** $(12 - 2x)^2 = 144 - 48x + 4x^2$; $V(x) = 4x^3 - 48x^2 + 144x$.

**Step 2 — The derivative.** $V'(x) = 12x^2 - 96x + 144 = 12(x^2 - 8x + 12) = 12(x - 2)(x - 6)$.

**Step 3 — Confirm.** $V''(x) = 24x - 96$; $V''(2) = -48 < 0$: a maximum. $V(2) = 32 - 192 + 288 = 128$.

**Why the same result?** $12(x - 2)(x - 6)$ and $(12 - 2x)(12 - 6x)$ are the same polynomial: $(12 - 2x)(12 - 6x) = 2(6 - x) \cdot 6(2 - x) = 12(x - 6)(x - 2)$. Expanding is longer but carries no risk of a sign error in the chain rule.

**Answer:** $2$ and $128$.
