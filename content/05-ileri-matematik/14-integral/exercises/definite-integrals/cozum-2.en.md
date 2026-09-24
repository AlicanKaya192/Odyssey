**Idea:** Split the first integral into terms and find the linear term with geometry (the area of a trapezoid). In the second, get rid of the root with $x = t^2$.

**Step 1 — The terms.** $\int_1^3 3x^2 \, dx = \big[x^3\big]_1^3 = 26$. $\int_1^3 x \, dx$: a trapezoid under the line $y = x$ from $x = 1$ to $3$; parallel sides $1$ and $3$, height $2$: area $\frac{(1 + 3) \cdot 2}{2} = 4$. Total $26 - 2 \cdot 4 = 18$.

**Step 2 — Substitute.** $x = t^2$, $dx = 2t \, dt$; $x = 1 \to t = 1$, $x = 4 \to t = 2$:

$$
\int_1^4 \frac{dx}{\sqrt{x}} = \int_1^2 \frac{2t}{t} \, dt = \int_1^2 2 \, dt = 2
$$

**Why the same result?** The integral of a linear function really is the area of a trapezoid; the fundamental theorem gives the same number by formula. In the second, the substitution turned the root into a constant function: a rectangle of height $2$ and width $1$.

**Answer:** $18$ and $2$.
