**Idea:** Think first about the total number of examples processed in four epochs, then about the batch structure of each epoch. This route shows why the number of steps cannot be found by simply dividing the total number of examples.

**Step 1 — The structure of one epoch.** $64 \cdot 390 = 24\,960$ examples go into full batches and the remaining $25\,000 - 24\,960 = 40$ into the last batch. Since $40 < 64$, $390$ full batches is right.

**Step 2 — Why not $100\,000 \div 64$?** Four epochs process $4 \cdot 25\,000 = 100\,000$ examples in total. $100\,000 = 64 \cdot 1\,562 + 32$; that calculation would give $1\,563$ steps. But each epoch ends with **its own** partial batch: batches are not merged across epochs.

**Step 3 — The correct count.** Each epoch is $391$ steps (390 full + 1 partial):

$$
4 \cdot 391 = 1\,564
$$

**Reading the result:** The difference between the two counts is exactly this: there is a short batch at the end of every epoch. Libraries even have an option to throw this last batch away ("drop last"); if it is dropped, an epoch is $390$ steps.

**Answer:** $390$, $40$ and $1\,564$.
