**What is asked?** Two Newton steps and the true minimising point.

**Idea:** At each step Newton goes to $w - \frac{L'}{L''}$. The derivatives are easy: $L' = e^w - 2$, $L'' = e^w$.

**Step 1 — The first step.** $w = 0$: $L' = -1$, $L'' = 1$; $w = 0 - \frac{-1}{1} = 1$.

**Step 2 — The second step.** $w = 1$: $L' = e - 2 \approx 0.71828$, $L'' = e$;

$$
w = 1 - \frac{0.71828}{2.71828} \approx 1 - 0.26424 = 0.73576
$$

**Step 3 — The true minimum.** $e^w = 2 \Rightarrow w = \ln 2 \approx 0.693$. $L'' = e^w > 0$: really a minimum.

**Check:** After the first step the error is $1 - 0.693 = 0.307$, after the second $0.736 - 0.693 = 0.043$. With Newton the error drops to about its square: $0.307^2 \cdot \frac{1}{2} \approx 0.047$ ✓.

**Watch out:** Writing $w - \eta L'$ as in gradient descent is not Newton; Newton has no learning rate, and $L''$ sets the step size.

**Answer:** $1$, $0.736$ and $0.693$.
