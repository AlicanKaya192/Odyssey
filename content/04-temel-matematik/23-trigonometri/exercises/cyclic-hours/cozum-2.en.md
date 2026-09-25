**Idea:** Two points on the unit circle with angle $\Delta$ between them form, together with the centre, an isosceles triangle with sides $1$ and $1$. The third side (the chord) comes from the law of cosines.

**Step 1 — The chord.** $c^2 = 1 + 1 - 2\cos\Delta = 2 - 2\cos\Delta$.

**Step 2 — $22$ and $2$.** $4$ hours apart, $\Delta = 60°$: $c^2 = 2 - 1 = 1$, $c = 1$. In fact the triangle is equilateral: two sides $1$ with $60°$ between them.

**Step 3 — $6$ and $18$.** $\Delta = 180°$: $c^2 = 2 + 2 = 4$, $c = 2$. For hour $8$, $\cos 120° = -\frac{1}{2}$.

**Why the same result?** The chord length depends only on the angle between the points; the coordinate calculation gives the same number because expanding the distance formula yields $2 - 2(\cos a \cos b + \sin a \sin b) = 2 - 2\cos(a - b)$. That is the beauty of the encoding: the distance depends only on the difference in hours and does not care about the day boundary.

**Answer:** $1$, $2$ and $-\frac{1}{2}$.
