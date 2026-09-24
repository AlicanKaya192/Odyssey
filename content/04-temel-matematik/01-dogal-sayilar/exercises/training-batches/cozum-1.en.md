**What is asked?** How a data set is split into batches and how many steps training takes.

**Idea:** Dividing $25\,000$ by $64$ with remainder, the quotient gives the number of full batches and the remainder the size of the last batch: $25\,000 = 64 \cdot q + r$.

**Step 1 — A rough estimate.** $64 \approx 60$ and $25\,000 \div 60 \approx 417$; since $64$ is a bit larger, the quotient is a bit smaller, around $400$.

**Step 2 — $64 \cdot 400$.** $25\,600$: that is more than $25\,000$, so $400$ is too many. The excess is $600$; $600 \div 64 \approx 9.4$, so we need about $10$ fewer batches.

**Step 3 — $64 \cdot 390$.** $25\,600 - 640 = 24\,960$. The remainder:

$$
25\,000 - 24\,960 = 40
$$

$40 < 64$: another batch does not fit.

$$
25\,000 = 64 \cdot 390 + 40
$$

**Step 4 — Full batches and the last batch.** $390$ full batches, $40$ examples in the last batch.

**Step 5 — Steps.** One epoch is $390 + 1 = 391$ steps. Four epochs:

$$
4 \cdot 391 = 1\,564
$$

**Watch out:** Forgetting the last, partial batch and writing $4 \cdot 390 = 1\,560$ is the most common slip; those $40$ examples are processed in every epoch too.

**Answer:** $390$ full batches; $40$ examples in the last batch; $1\,564$ steps in $4$ epochs.
