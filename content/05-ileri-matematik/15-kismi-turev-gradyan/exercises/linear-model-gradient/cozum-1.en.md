**What is asked?** The partial derivatives of the loss with respect to the weights of a linear model, and the result of one gradient descent step.

**Idea:** The chain rule: $\frac{\partial L}{\partial w_j} = \frac{\partial L}{\partial \hat{y}} \cdot \frac{\partial \hat{y}}{\partial w_j} = 2(\hat{y} - y) \cdot x_j$.

**Step 1 — The forward pass.** $\hat{y} = 1.5$, error $\hat{y} - y = -1.5$, loss $2.25$.

**Step 2 — The partial derivatives.** $\frac{\partial L}{\partial w_1} = 2(-1.5)(1) = -3$, $\frac{\partial L}{\partial w_2} = 2(-1.5)(2) = -6$, $\frac{\partial L}{\partial b} = -3$.

**Step 3 — The step.** $w_1 = 0.5 + 0.3 = 0.8$, $w_2 = 0.5 + 0.6 = 1.1$, $b = 0.3$.

**Step 4 — The new loss.** $\hat{y} = 0.8 + 2.2 + 0.3 = 3.3$; $L = 0.3^2 = 0.09$.

**Check:** The loss dropped from $2.25$ to $0.09$ ✓. $w_2$ changed twice as much as $w_1$: its feature ($x_2 = 2$) is twice as large.

**Watch out:** Forgetting to update $b$ would make the new prediction $3.0$; in this example the loss then happens to be zero, but the question asks for all parameters to be updated.

**Answer:** $-3$, $-6$ and $0.09$.
