The model is $\hat{y} = wx$, with a single example: $x = 2$, $y = 6$. The loss is the squared error:

$$
L(w) = (2w - 6)^2
$$

Initially $w = 1$, and the learning rate is $\eta = 0.05$.

1. What is $L'(1)$?
2. After one step ($w \leftarrow w - \eta L'(w)$), what is $w$?
3. What is the loss with the new $w$?
