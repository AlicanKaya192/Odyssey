**What is asked?** The length of the straight line between $A$ and $B$.

**Idea:** If we find the arrow (vector) from $A$ to $B$, the distance is the length of that arrow. The arrow is "end minus start". Its length comes from Pythagoras: the square root of the sum of the squared components.

**Step 1 — The vector from $A$ to $B$.** In each component, subtract $A$'s coordinate from $B$'s:

$$
\begin{aligned}
\overrightarrow{AB} &= \big(5 - (-1),\ 10 - 2\big) \\
&= (6,\ 8)
\end{aligned}
$$

So to get from $A$ to $B$ we go 6 units right and 8 units up.

**Step 2 — The length of the arrow.** Think of 6 and 8 as the two legs of a right triangle; the distance we want is the hypotenuse:

$$
\begin{aligned}
\|\overrightarrow{AB}\| &= \sqrt{6^2 + 8^2} \\
&= \sqrt{36 + 64} \\
&= \sqrt{100} = 10
\end{aligned}
$$

**Watch out:** $A$'s $x$ is negative: $5 - (-1) = 6$, not $4$.

Subtracting the other way ($A - B = (-6, -8)$) gives the same result, because squaring removes the minus signs. Distance does not care about direction.

**Answer:** 10.
