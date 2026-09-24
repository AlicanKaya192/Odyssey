**What is asked?** Two numbers measuring a model's typical error size: MSE and RMSE.

**Idea:** Averaging the errors directly does not work; positives and negatives cancel ($3 - 1 + 2 - 2 = 2$). Squaring removes the sign, averaging reduces to one number, and the square root brings back the unit (the error's own unit). The name spells out the order: **R**oot **M**ean **S**quared **E**rror.

**Step 1 — The squares.**

$$
3^2 = 9, \quad (-1)^2 = 1, \quad 2^2 = 4, \quad (-2)^2 = 4
$$

**Step 2 — The mean (MSE).**

$$
\frac{9 + 1 + 4 + 4}{4} = \frac{18}{4} = 4.5
$$

**Step 3 — The square root (RMSE).** $2.1^2 = 4.41$ and $2.2^2 = 4.84$: the root is between $2.1$ and $2.2$, near $2.1$. $2.12^2 = 4.494$ and $2.13^2 = 4.537$:

$$
\sqrt{4.5} \approx 2.12
$$

**Reading the result:** The error sizes are between $1$ and $3$; the RMSE $2.12$ is their "typical" value. The mean of the absolute errors ($\frac{3 + 1 + 2 + 2}{4} = 2$) is a bit smaller; RMSE gives more weight to large errors (here, the $3$).

**Watch out:** Mixing up the order and taking the root before averaging ($\frac{3 + 1 + 2 + 2}{4}$) gives the mean absolute error, not the RMSE.

**Answer:** MSE $4.5$; RMSE $\approx 2.12$.
