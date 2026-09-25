**What is asked?** Three gradient descent steps on a one-variable loss.

**Idea:** At each step compute the derivative, multiply by $\eta$ and subtract from $w$.

**Step 1.** $L'(0) = -8$: $w_1 = 0 + 2 = 2$.

**Step 2.** $L'(2) = -4$: $w_2 = 2 + 1 = 3$.

**Step 3.** $L'(3) = -2$: $w_3 = 3 + 0.5 = 3.5$.

**Check:** The losses go $16 \to 4 \to 1 \to 0.25$: a quarter at each step ✓.

**Watch out:** While the derivative is negative, $w$ **increases**; minus times minus.

**Answer:** $2$, $3$ and $3.5$.
