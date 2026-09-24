**Idea:** What makes $e^x$ special is $f' = f$ and $f(0) = 1$. Find the coefficients from these two conditions, without a table of derivatives: for $P(x) = c_0 + c_1 x + c_2 x^2 + c_3 x^3 + \cdots$, ask for $P' = P$.

**Step 1 — Compare.** $P' = c_1 + 2c_2 x + 3c_3 x^2 + \cdots$. The coefficients of equal powers match: $c_1 = c_0$, $2c_2 = c_1$, $3c_3 = c_2$.

**Step 2 — Chain them.** $c_0 = 1$ ($P(0) = 1$), $c_1 = 1$, $c_2 = \frac{1}{2}$, $c_3 = \frac{1}{6}$.

**Step 3 — The value.** $1 + 0.5 + 0.125 + 0.0208\overline{3} = 1.6458\overline{3} = \frac{79}{48}$.

**Why the same result?** The rule $c_{k+1} = \frac{c_k}{k + 1}$ produces $c_k = \frac{1}{k!}$ step by step; the factorial is the natural result of the condition "equal to its own derivative". The Taylor formula says the same thing through the derivatives.

**Answer:** $\frac{1}{6}$ and $\frac{79}{48} \approx 1.6458$.
