**What is asked?** Two basic success measures of a classifier.

**Idea:** Both measures divide the correctly caught ones ($P \cap S$) by a whole; the difference is what the whole is. For precision it is "what the model called spam", for recall "the real spam".

**Step 1 — The intersection.** Called spam by the model and really spam: $n(P \cap S) = 24$.

**Step 2 — Precision.**

$$
\frac{24}{30} = 0.8
$$

$80\%$ of what the model called spam really is spam.

**Step 3 — Recall.**

$$
\frac{24}{40} = 0.6
$$

$60\%$ of the real spam was caught; $16$ spam emails slipped through.

**Reading the result:** The model is cautious: when it says "spam" it is usually right (high precision) but it misses a lot of spam (low recall). Lowering the threshold raises recall and usually lowers precision.

**Watch out:** Mixing up the two denominators is the most common slip. Precision is "among what I flagged", recall "among what really is".

**Answer:** Precision $0.8$, recall $0.6$.
