The model is $\hat{y} = wx$, the examples are $(1, 2)$ and $(3, 3)$, the example loss is $\ell_i = (y_i - w x_i)^2$ and the average loss is $L = \frac{1}{2}(\ell_1 + \ell_2)$. Start at $w = 0$ with $\eta = 0.05$.

1. What is the average gradient $L'(0)$ at $w = 0$?
2. What is $w$ after one full-gradient step?
3. If instead SGD takes two steps, using the second example first and then the first example, what is $w$?
