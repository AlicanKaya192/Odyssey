**Idea:** First find the test set's share of all the data using fractions; compute the number of examples at the end with a single multiplication.

**Step 1 — Left after training.** $1 - \frac{7}{10} = \frac{3}{10}$.

**Step 2 — Test within what is left.** Validation is $\frac{1}{3}$ of what is left, test is $1 - \frac{1}{3} = \frac{2}{3}$ of it.

**Step 3 — The test share of all the data.** A fraction of a fraction is a product:

$$
\frac{2}{3} \cdot \frac{3}{10} = \frac{2}{10} = \frac{1}{5}
$$

**Step 4 — The number of examples.**

$$
\frac{1}{5} \cdot 1\,200 = 240
$$

**Why the same result?** The first method worked with counts out of the whole $1\,200$ at every step; this one multiplied the shares and multiplied by the whole at the end. The order of multiplication changes but the same products are made. The advantage of this route: even if the size of the data set changes, the test share stays $\frac{1}{5}$.

**Answer:** $240$ and $\dfrac{1}{5}$.
