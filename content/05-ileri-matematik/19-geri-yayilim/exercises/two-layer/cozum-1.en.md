**What is asked?** The derivatives of the loss with respect to the output and first-layer weights of a small network.

**Idea:** Start from the loss; at each layer carry the incoming gradient back through the weights, and find the weight derivatives by multiplying with the input.

**Step 1 — Forward.** $z_1 = 1$, $z_2 = -1 + 2 = 1$; $a = (1, 1)$; $\hat{y} = 2 - 1 = 1$; $L = 2$.

**Step 2 — The output.** $\frac{\partial L}{\partial \hat{y}} = -2$. $\frac{\partial L}{\partial w_{21}} = -2 \cdot a_1 = -2$.

**Step 3 — Into the hidden layer.** $\frac{\partial L}{\partial a} = -2 \cdot (2, -1) = (-4, 2)$. Both $z$'s are positive: $\frac{\partial L}{\partial z} = (-4, 2)$.

**Step 4 — The first-layer weights.** $\frac{\partial L}{\partial W_{1j}} = \frac{\partial L}{\partial z_j} \cdot x$: $-4$ and $2$.

**Check:** Increase $W_{11}$ by $0.01$: $z_1 = 1.01$, $\hat{y} = 2.02 - 1 = 1.02$, $L = \frac{1}{2}(1.98)^2 = 1.9602$; the change is $-0.0398 / 0.01 \approx -3.98$ ✓.

**Watch out:** The second hidden neuron's weight $w_{22} = -1$ is negative, so the gradient going to it is positive ($+2$). Missing the sign gives $W_{12}$ as $-2$.

**Answer:** $-2$, $-4$ and $2$.
