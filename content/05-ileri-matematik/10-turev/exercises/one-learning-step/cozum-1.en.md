**What is asked?** One gradient descent step for a model with a single weight.

**Idea:** The derivative of the loss says which way to push the weight. Find the derivative, take the step, compute the new loss.

**Step 1 — The derivative.** $L(w) = 4w^2 - 24w + 36$, $L'(w) = 8w - 24$. $L'(1) = -16$.

**Step 2 — The step.**

$$
w \leftarrow 1 - 0.05 \cdot (-16) = 1 + 0.8 = 1.8
$$

**Step 3 — The new loss.** $L(1.8) = (3.6 - 6)^2 = (-2.4)^2 = 5.76$.

**Check:** The old loss is $L(1) = (2 - 6)^2 = 16$; the new loss is $5.76$. The loss went down ✓. The best weight is $w = 3$ ($2 \cdot 3 = 6$); $w$ moved the right way, from $1$ to $1.8$.

**Watch out:** Adding $\eta L'$ while the slope is negative ($1 - 0.8 = 0.2$) goes the wrong way and raises the loss; the minus sign in the formula means "against the slope".

**Answer:** $L'(1) = -16$, $w = 1.8$, loss $5.76$.
