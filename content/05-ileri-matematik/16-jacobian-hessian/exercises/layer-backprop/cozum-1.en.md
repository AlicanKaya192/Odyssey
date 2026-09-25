**What is asked?** The derivative of the loss with respect to the input of a layer and one of its weights.

**Idea:** Start from the loss and walk back, multiplying by each link's Jacobian: $\frac{\partial L}{\partial \mathbf{a}} \to \frac{\partial L}{\partial \mathbf{z}} \to \frac{\partial L}{\partial \mathbf{x}}$.

**Step 1 — The forward pass.** $\mathbf{z} = (1 + 2, \ 3 - 1) = (3, 2)$, both positive: $\mathbf{a} = (3, 2)$.

**Step 2 — Back from the loss.** $\frac{\partial L}{\partial \mathbf{a}} = \mathbf{a} - \mathbf{y} = (2, 1)$. ReLU's Jacobian is the identity: $\frac{\partial L}{\partial \mathbf{z}} = (2, 1)$.

**Step 3 — To the input.**

$$
\frac{\partial L}{\partial \mathbf{x}} = W^\mathsf{T} \begin{bmatrix} 2 \\ 1 \end{bmatrix} = \begin{bmatrix} 1 & 3 \\ 2 & -1 \end{bmatrix} \begin{bmatrix} 2 \\ 1 \end{bmatrix} = \begin{bmatrix} 5 \\ 3 \end{bmatrix}
$$

**Step 4 — To the weight.** $\frac{\partial L}{\partial W_{12}} = \frac{\partial L}{\partial z_1} \cdot x_2 = 2 \cdot 1 = 2$.

**Check:** Increase $x_1$ by $0.01$: $\mathbf{z} = (3.01, 2.03)$, $L = \frac{1}{2}(2.01^2 + 1.03^2) \approx 2.5506$; the old $L = 2.5$. The difference over $0.01$ is $\approx 5.06$ ✓.

**Watch out:** $W^\mathsf{T}$, not $W$, is needed; $W(2, 1) = (4, 5)$ gives the wrong answer.

**Answer:** $5$, $3$ and $2$.
