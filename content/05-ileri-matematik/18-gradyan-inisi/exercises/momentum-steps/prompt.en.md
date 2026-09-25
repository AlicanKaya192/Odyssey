$L(w) = w^2$, $w_0 = 1$, $\eta = 0.1$. The update with momentum ($\beta = 0.9$, $v_0 = 0$):

$$
v_{k+1} = \beta v_k + L'(w_k), \qquad w_{k+1} = w_k - \eta \, v_{k+1}
$$

1. What is $w_2$ with momentum?
2. What is $w_3$ with momentum?
3. What is $w_3$ with plain gradient descent?
