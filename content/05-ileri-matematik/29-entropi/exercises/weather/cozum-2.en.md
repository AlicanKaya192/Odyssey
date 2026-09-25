**Idea:** Entropy is the average number of yes–no questions needed to find the outcome (with the best strategy).

**Step 1 — Questions.** First ask "sunny?": half the time it ends in one question. If not, "cloudy?": $2$ questions. The average is $\frac{1}{2} \cdot 1 + \frac{1}{2} \cdot 2 = 1.5$.

**Step 2 — Nats.** The same information with the natural log: $\frac{1}{2}\ln 2 + \frac{1}{2}\ln 4 = 1.5\ln 2 \approx 1.040$.

**Step 3 — Upper bound.** With three equal outcomes even the best strategy needs $\frac{5}{3} \approx 1.667$ questions on average; the entropy $\log_2 3 \approx 1.585$ is a little less because it has no whole-question constraint (coding many outcomes together approaches this bound).

**Why the same result?** When the probabilities are powers of $2$, the branch lengths of the best question tree are exactly $-\log_2 p$; the average number of questions equals the entropy.

**Answer:** $1.5$, $1.040$ and $1.585$.
