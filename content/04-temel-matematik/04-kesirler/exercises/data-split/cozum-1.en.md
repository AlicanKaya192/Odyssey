**What is asked?** Splitting a data set three ways, into training, validation and test; the size and share of the test set.

**Idea:** Find how many examples are left step by step. "$\frac{1}{3}$ of the rest" is a part of what is left after training, not of the whole.

**Step 1 — Training.**

$$
\frac{7}{10} \cdot 1\,200 = 840
$$

That leaves $1\,200 - 840 = 360$ examples.

**Step 2 — Validation.**

$$
\frac{1}{3} \cdot 360 = 120
$$

**Step 3 — Test.** $360 - 120 = 240$ examples.

**Step 4 — The share.**

$$
\frac{240}{1\,200} = \frac{1}{5}
$$

(We divided $240$ and $1\,200$ by $240$.)

**Check:** $840 + 120 + 240 = 1\,200$ ✓.

**Reading the result:** The split is about 70% training, 10% validation, 20% test; a common split in machine learning.

**Answer:** $240$ examples; $\dfrac{1}{5}$ of the data.
