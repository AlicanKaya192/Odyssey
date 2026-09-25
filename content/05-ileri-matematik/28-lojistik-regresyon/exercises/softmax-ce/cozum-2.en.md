**Idea:** $-\ln p_2 = -z_2 + \ln\sum_j e^{z_j}$. We can write the loss directly without dividing out each probability.

**Step 1 — $p_1$.** $\frac{e^{2}}{11.212} \approx 0.659$.

**Step 2 — Loss.** $\ln 11.212 \approx 2.417$; the loss is $-1 + 2.417 = 1.417$.

**Step 3 — Derivative.** $\frac{\partial}{\partial z_2}\left[-z_2 + \ln\sum_j e^{z_j}\right] = -1 + \frac{e^{z_2}}{\sum_j e^{z_j}} = -1 + p_2 \approx -0.758$.

**Why the same result?** $\ln\frac{e^{z_2}}{\sum e^{z_j}} = z_2 - \ln\sum e^{z_j}$; and the derivative of log-sum-exp is the softmax itself. Libraries compute the loss in this form because with large scores it can be computed without $e^{z}$ overflowing.

**Answer:** $0.659$, $1.417$ and $-0.758$.
