**What is asked?** The quartiles of a dataset and the fence for outliers.

**Idea:** The median splits the data in two halves; the median of each half is a quartile.

**Step 1 — The halves.** The data is sorted. Lower half $12, 15, 17, 18, 20$; upper half $21, 23, 25, 26, 48$. (The median is $\frac{20 + 21}{2} = 20.5$.)

**Step 2 — The quartiles.** Q1 $= 17$, Q3 $= 25$.

**Step 3 — The fence.** IQR $= 8$; $25 + 1.5 \cdot 8 = 37$. $48 > 37$: that day is an outlier. The lower fence is $17 - 12 = 5$; no value lies below it.

**Check:** The middle half of the values (around $18, 20, 21, 23, 25$) lies between $17$ and $25$ ✓.

**Watch out:** An outlier does not mean "bad data"; if a campaign ran that day, $48$ is a real value. The rule only says "look at this".

**Answer:** Q1 $= 17$, Q3 $= 25$, upper fence $37$.
