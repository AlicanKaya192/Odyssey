**Idea:** The normal vector of the line $3x + 4y = 25$ is $(3, 4)$. The shortest way from the origin to the line runs along this normal; look for the point as $t(3, 4)$.

**Step 1 — Put it on the line.** $3(3t) + 4(4t) = 25t = 25$: $t = 1$. The point is $(3, 4)$.

**Step 2 — The distance.** $\lVert (3, 4) \rVert = 5$; its square is $25$. With the general formula too: $\frac{\lvert 25 \rvert}{\sqrt{3^2 + 4^2}} = 5$.

**Why the same result?** The Lagrange condition $\nabla f = \lambda \nabla g$ says "at the closest point, the line from the origin (the direction $\nabla f = 2(x, y)$) is parallel to the constraint's normal ($\nabla g = (3, 4)$)"; that is the definition of a perpendicular projection. Both methods state the same geometric fact.

**Answer:** $3$, $4$ and $25$.
