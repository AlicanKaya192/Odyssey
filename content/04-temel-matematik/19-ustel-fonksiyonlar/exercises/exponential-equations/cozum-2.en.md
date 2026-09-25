**Idea:** Instead of equating exponents, give the repeating power a new letter. We show it on the first equation; the other two follow the same way.

**Step 1 — Split.** $2^{x + 3} = 8 \cdot 2^x$ and $4^{x - 1} = \frac{4^x}{4} = \frac{(2^x)^2}{4}$.

**Step 2 — Let $u = 2^x$.** The equation becomes $8u = \frac{u^2}{4}$, that is $u^2 = 32u$. Since $u = 2^x > 0$ we may divide by $u$: $u = 32$.

**Step 3 — Go back.** $2^x = 32 = 2^5$, $x = 5$.

**The other two.** With $u = 3^x$ the second becomes $u^3 = 81 u^2$, so $u = 81 = 3^4$ and $x = 4$. With $u = 2^x$ the third becomes $\frac{1}{u} = \frac{u^3}{4096}$, so $u^4 = 4096 = 2^{12}$, $u = 8$ and $x = 3$.

**Why the same result?** Substitution applies the exponent rules ($b^{m + n} = b^m b^n$) to the base instead of the exponent; in the end we still reach the step "same base, same exponent". For equations such as $4^x - 3 \cdot 2^x - 4 = 0$, where the exponents cannot be equated directly, this is the only way.

**Answer:** $5$, $4$ and $3$.
