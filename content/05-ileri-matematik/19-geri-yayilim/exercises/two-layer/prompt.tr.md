Bir girdi, iki gizli ReLU nöronu, bir çıktı:

$$
\begin{aligned}
z_j &= W_{1j} x + b_{1j}, & a_j &= \mathrm{ReLU}(z_j) \\
\hat{y} &= w_{21} a_1 + w_{22} a_2, & L &= \tfrac{1}{2}(\hat{y} - y)^2
\end{aligned}
$$

$x = 1$, $W_1 = (1, -1)$, $b_1 = (0, 2)$, $w_2 = (2, -1)$, hedef $y = 3$.

1. $\dfrac{\partial L}{\partial w_{21}}$ kaç?
2. $\dfrac{\partial L}{\partial W_{11}}$ kaç?
3. $\dfrac{\partial L}{\partial W_{12}}$ kaç?
