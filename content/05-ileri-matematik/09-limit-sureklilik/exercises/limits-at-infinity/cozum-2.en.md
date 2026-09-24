**Idea:** For very large $x$, the term with the highest power in each polynomial swamps the others. Write top and bottom with only their dominant terms.

**Step 1 — The first limit.** At $x = 1000$, $4x^2 = 4\,000\,000$ and $3x = 3000$; the second is less than a thousandth. Dominant terms: $\frac{4x^2}{2x^2} = 2$.

**Step 2 — The second limit.** Dominant terms: $\frac{5x}{x^2} = \frac{5}{x} \to 0$.

**Step 3 — Check with a number.** $x = 1000$: the first expression is $\frac{3\,997\,000}{2\,000\,005} \approx 1.9985$; the second $\frac{5001}{1\,000\,002} \approx 0.005$.

**Why the same result?** Dividing by the highest power is the written form of putting the non-dominant terms in the form $\frac{c}{x^k}$ and sending them to zero. Thinking in dominant terms does the same job in your head.

**Answer:** $2$ and $0$.
