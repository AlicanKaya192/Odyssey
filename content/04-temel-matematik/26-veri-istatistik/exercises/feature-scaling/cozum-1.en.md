**What is asked?** Applying scaling values computed from the training data to test data.

**Idea:** The mean, standard deviation, minimum and maximum are computed **from the training data only**; test values are transformed with the same numbers.

**Step 1 — The standard deviation.** The mean is $30$. The squared deviations are $400, 100, 0, 100, 400$; total $1000$; variance $200$.

$$
\sigma = \sqrt{200} = 10\sqrt{2} \approx 14.142
$$

**Step 2 — The z-score of $45$.** $\frac{45 - 30}{14.142} \approx 1.061$.

**Step 3 — The min–max value of $60$.** $\frac{60 - 10}{50 - 10} = \frac{50}{40} = 1.25$.

**Check:** Under min–max the training values become $0, 0.25, 0.5, 0.75, 1$. $60$ is larger than the training maximum, so going above $1$ is natural ✓.

**Watch out:** Seeing $60$ and resetting the maximum to $60$ would leak information from the test data. The scaling numbers are fixed once on the training data and do not change; test values can fall outside $[0, 1]$.

**Answer:** $14.142$, $1.061$, $1.25$.
