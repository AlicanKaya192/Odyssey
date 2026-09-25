**Idea:** The network is small; write $\hat{y}$ as an explicit function of the weights. Near the point both $z$'s are positive, so ReLU does nothing.

**Step 1 — The explicit form.** $\hat{y} = w_{21}(W_{11}x) + w_{22}(W_{12}x + 2)$.

**Step 2 — The chain.** $\frac{\partial L}{\partial \theta} = (\hat{y} - y) \frac{\partial \hat{y}}{\partial \theta} = -2 \frac{\partial \hat{y}}{\partial \theta}$.

**Step 3 — The derivatives.** $\frac{\partial \hat{y}}{\partial w_{21}} = W_{11}x = 1$: $-2$. $\frac{\partial \hat{y}}{\partial W_{11}} = w_{21}x = 2$: $-4$. $\frac{\partial \hat{y}}{\partial W_{12}} = w_{22}x = -1$: $2$.

**Why the same result?** Backpropagation builds these products (such as $w_{21} \cdot x$) layer by layer, computing the shared parts ($\frac{\partial L}{\partial \hat{y}} = -2$) once. Writing it out is possible here; in a ten-layer network the number of terms explodes, while the cost of backpropagation grows linearly with the number of layers.

**Answer:** $-2$, $-4$, $2$.
