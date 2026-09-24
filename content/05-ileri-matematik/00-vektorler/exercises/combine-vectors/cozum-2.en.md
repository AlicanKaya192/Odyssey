**Idea:** Vector operations never mix components. The $x$ component of the result comes only from the $x$ components of $\mathbf{u}$ and $\mathbf{v}$, and the $y$ component only from the $y$'s. So we can solve the same expression as two separate number problems.

**Step 1 — The $x$ component.** The $x$ of $\mathbf{u}$ is $2$, the $x$ of $\mathbf{v}$ is $-3$. Put these two numbers in place of $\mathbf{u}$ and $\mathbf{v}$:

$$
\begin{aligned}
x &= 3 \cdot 2 - 2 \cdot (-3) \\
&= 6 - (-6) \\
&= 6 + 6 = 12
\end{aligned}
$$

**Step 2 — The $y$ component.** The $y$ of $\mathbf{u}$ is $-1$, the $y$ of $\mathbf{v}$ is $4$:

$$
\begin{aligned}
y &= 3 \cdot (-1) - 2 \cdot 4 \\
&= -3 - 8 = -11
\end{aligned}
$$

**Why the same result?** Every step of the first method was already done component by component. Here we only changed the order: instead of the whole vector, we took one component all the way to the end.

**Why is it useful?** When the dimension grows (a 784-component image vector, say) this view is far more practical: the same small calculation is repeated in every component. That is exactly how a computer does vector operations.

**Answer:** $(12, -11)$.
