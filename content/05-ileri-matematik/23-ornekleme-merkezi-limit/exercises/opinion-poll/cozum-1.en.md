**What is asked?** The standard error of a poll proportion, the probability of an extreme result and the sample needed.

**Idea:** $\hat{p}$ is a Bernoulli mean; by the CLT it is approximately $\mathcal{N}\!\left(p, \frac{p(1 - p)}{n}\right)$.

**Step 1 — SE.** $\sqrt{\frac{0.2475}{400}} = \sqrt{0.000619} \approx 0.0249$.

**Step 2 — $0.60$ or more.** $z = \frac{0.05}{0.0249} \approx 2.01$; $1 - 0.978 = 0.022$.

**Step 3 — The $n$ needed.** $n = \frac{0.2475}{0.000225} = 1100$.

**Check:** Cutting the error from $0.0249$ to $0.015$ (about $1.66$ times) takes $1.66^2 \approx 2.75$ times the data: $400 \cdot 2.75 = 1100$ ✓.

**Watch out:** Writing the standard error as $\frac{p(1 - p)}{n}$ without the square root gives the variance.

**Answer:** $\approx 0.0249$, $\approx 0.022$, $1100$.
