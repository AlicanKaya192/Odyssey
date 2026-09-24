**What is asked?** The derivative of the loss with respect to a neuron's two parameters, and one learning step.

**Idea:** $L$ is tied to $w$ through $\hat{y}$ and $z$; the chain rule multiplies the derivatives of the links. First find the intermediate values with a forward pass.

**Step 1 — The forward pass.** $z = 0 \cdot 2 + 0 = 0$, $\hat{y} = 0.5$, $L = 0.25$.

**Step 2 — The links.** $\frac{\partial L}{\partial \hat{y}} = 2(0.5 - 1) = -1$. $\frac{\partial \hat{y}}{\partial z} = 0.5 \cdot 0.5 = 0.25$. $\frac{\partial z}{\partial w} = x = 2$, $\frac{\partial z}{\partial b} = 1$.

**Step 3 — Multiply.**

$$
\begin{aligned}
\frac{\partial L}{\partial w} &= (-1)(0.25)(2) = -0.5 \\
\frac{\partial L}{\partial b} &= (-1)(0.25)(1) = -0.25
\end{aligned}
$$

**Step 4 — The step.** $w \leftarrow 0 - 1 \cdot (-0.5) = 0.5$.

**Check:** With the new values ($w = 0.5$, $b = 0.25$): $z = 1.25$, $\hat{y} = \sigma(1.25) \approx 0.777$, loss $(0.777 - 1)^2 \approx 0.05$. Down from $0.25$ ✓.

**Watch out:** The gradient is negative, so $w$ **goes up**. The prediction ($0.5$) is below the target ($1$), and raising $w$ raises the prediction.

**Answer:** $\frac{\partial L}{\partial w} = -0.5$, $\frac{\partial L}{\partial b} = -0.25$, new $w = 0.5$.
