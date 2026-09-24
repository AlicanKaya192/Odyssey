**What is asked?** The best parameter of two simple models on three data points, and the smallest loss.

**Idea:** Write the loss as a function of the parameter and set its derivative to zero.

**Step 1 — The derivative.** $L(w) = \sum (y_i - w x_i)^2$, $L'(w) = -2 \sum x_i (y_i - w x_i) = 0$:

$$
w = \frac{\sum x_i y_i}{\sum x_i^2} = \frac{2 + 6 + 21}{1 + 4 + 9} = \frac{29}{14} \approx 2.071
$$

**Step 2 — The loss.** Residuals: $2 - \frac{29}{14} = -\frac{1}{14}$, $3 - \frac{58}{14} = -\frac{16}{14}$, $7 - \frac{87}{14} = \frac{11}{14}$. The sum of squares is $\frac{1 + 256 + 121}{196} = \frac{378}{196} = \frac{27}{14} \approx 1.93$.

**Step 3 — The constant model.** $L(c) = \sum (y_i - c)^2$, $L'(c) = 0 \Rightarrow c = \frac{2 + 3 + 7}{3} = 4$.

**Check:** $L''(w) = 2 \sum x_i^2 = 28 > 0$: really a minimum ✓. With $w = 2$ the loss is $0 + 1 + 1 = 2 > \frac{27}{14}$ ✓.

**Watch out:** Finding $w$ as $\frac{\sum y_i}{\sum x_i} = \frac{12}{6} = 2$ is wrong; that is not what minimises the squared error.

**Answer:** $w = \frac{29}{14}$, loss $\frac{27}{14}$, $c = 4$.
