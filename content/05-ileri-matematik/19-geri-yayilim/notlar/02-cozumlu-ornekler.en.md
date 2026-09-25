A worked example for each method in the lesson. Try the question yourself first, then read the solution.

## 1. The addition gate

**Question:** $f = a + b$ with incoming gradient $3$. What goes to $a$ and to $b$?

$3$ to both.

## 2. The multiplication gate

**Question:** $f = a \cdot b$, $a = 4$, $b = -2$, incoming gradient $1$. What are the derivatives?

$\frac{\partial f}{\partial a} = b = -2$, $\frac{\partial f}{\partial b} = a = 4$.

## 3. The max gate

**Question:** $f = \max(a, b)$, $a = 1$, $b = 5$, incoming gradient $2$. What are the derivatives?

$0$ to $a$, $2$ to $b$.

## 4. Branching

**Question:** $f = x \cdot x$, $x = 3$. In the graph $x$ is used twice. What is $\frac{df}{dx}$?

The multiplication sends each copy the other one: $3 + 3 = 6$; the same as $(x^2)' = 2x$.

## 5. ReLU

**Question:** $z = -1$, incoming gradient $5$. What is $\frac{\partial L}{\partial z}$ after the ReLU?

$z < 0$: $0$.

## 6. Sigmoid

**Question:** $\sigma(z) = 0.5$, incoming gradient $4$. What is $\frac{\partial L}{\partial z}$?

$4 \cdot 0.5 \cdot 0.5 = 1$.

## 7. A linear layer

**Question:** $W = \begin{bmatrix} 1 & 2 \\ 0 & 1 \end{bmatrix}$, $\frac{\partial L}{\partial \mathbf{z}} = (1, 3)$. What is $\frac{\partial L}{\partial \mathbf{x}}$?

$W^\mathsf{T}(1, 3) = (1 \cdot 1 + 0 \cdot 3, \ 2 \cdot 1 + 1 \cdot 3) = (1, 5)$.

## 8. Depth

**Question:** The factor at each layer is $0.5$. After $8$ layers, by what factor has the gradient shrunk?

$0.5^8 = \frac{1}{256}$.
