**Idea:** Split the distance into two series: all the falls and all the rises. The falls are $81, 54, 36, \dots$; the rises $54, 36, 24, \dots$. Both are geometric series with ratio $\frac{2}{3}$.

**Step 1 — The fourth bounce.** The fourth rise: $54, 36, 24, 16$.

**Step 2 — Up to the fifth touch.** Five falls ($81, 54, 36, 24, 16$) and four rises ($54, 36, 24, 16$):

$$
211 + 130 = 341
$$

**Step 3 — Forever.** The falls give $\frac{81}{1/3} = 243$ and the rises $\frac{54}{1/3} = 162$; the total is $405$.

**Why the same result?** Every rise is followed by a fall of the same length; the series of falls is the series of rises with $81$ added at the front. That is why $243 + 162 = 81 + 2 \cdot 162$.

**Answer:** $16$, $341$ and $405$.
