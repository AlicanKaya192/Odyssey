**Idea:** Sort the $100$ emails into four boxes by two questions: what did the model say, and what is the truth? This table is called a **confusion matrix**; all the measures are read from it.

**Step 1 — The boxes.**

| | really spam | really normal | total |
|---|---|---|---|
| model: spam | $24$ | $30 - 24 = 6$ | $30$ |
| model: normal | $40 - 24 = 16$ | $54$ | $70$ |
| total | $40$ | $60$ | $100$ |

**Step 2 — Precision.** The "model: spam" row: $\dfrac{24}{30} = 0.8$.

**Step 3 — Recall.** The "really spam" column: $\dfrac{24}{40} = 0.6$.

**Why the same result?** The table's four boxes are the four regions of the Venn diagram of two sets: $P \cap S$ ($24$), $P$ only ($6$), $S$ only ($16$), neither ($54$). Precision looks along the row, recall down the column.

**Answer:** $0.8$ and $0.6$.
