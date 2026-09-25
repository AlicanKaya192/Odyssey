**What is asked?** Softmax probabilities, cross-entropy and the gradient with respect to the correct class's score.

**Idea:** Exponentiate, add up, divide; the loss is minus the log of the correct class's probability.

**Step 1 — Probabilities.** The sum is $7.389 + 2.718 + 1.105 = 11.212$. $p_1 = \frac{7.389}{11.212} \approx 0.659$, $p_2 \approx 0.242$, $p_3 \approx 0.099$.

**Step 2 — Loss.** $-\ln 0.242 \approx 1.417$.

**Step 3 — Derivative.** $p_2 - 1 \approx -0.758$: increasing $z_2$ lowers the loss.

**Check:** The probabilities sum to $0.659 + 0.242 + 0.099 = 1$ ✓.

**Watch out:** The loss is computed from the correct class's probability, not the largest one ($p_1$); the loss is large because the model gave the wrong class the highest probability.

**Answer:** $\approx 0.659$, $\approx 1.417$, $\approx -0.758$.
