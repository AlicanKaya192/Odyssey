**What is asked?** The accuracy of two models, and what these numbers tell us.

**Idea:** Accuracy is the ratio of correct predictions to all predictions. A model that always gives the same answer gets every example right for which that answer is correct.

**Step 1 — The model's accuracy.**

$$
\frac{1\,870}{2\,200} = \frac{187}{220} = \frac{17}{20} = 0.85 = 85\%
$$

(We divided $1\,870$ and $2\,200$ first by $10$, then by $11$.)

**Step 2 — The always-"normal" model.** It gets all $2\,090$ normal transactions right and all $110$ fraud cases wrong:

$$
\frac{2\,090}{2\,200} = \frac{19}{20} = 0.95 = 95\%
$$

**Step 3 — Compare.** The model that learned nothing scored **higher** accuracy than the trained model.

**Reading the result:** The data is very unbalanced: $95\%$ of transactions are normal. On such data accuracy alone misleads; what really matters is success on the minority class (fraud). The always-"normal" model does not catch a single fraud, so it is useless.

**Answer:** $85\%$ and $95\%$.
