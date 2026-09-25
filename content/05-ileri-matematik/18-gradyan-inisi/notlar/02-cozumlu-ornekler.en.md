A worked example for each method in the lesson. Try the question yourself first, then read the solution.

## 1. One step

**Question:** $L(w) = (w - 2)^2$, $w = 5$, $\eta = 0.1$. What is $w$ after one step?

$L'(5) = 6$; $5 - 0.6 = 4.4$.

## 2. The factor

**Question:** For the same loss ($\lambda = 2$) with $\eta = 0.1$, by what factor does the distance shrink each step?

$1 - 0.2 = 0.8$.

## 3. The upper limit

**Question:** For $L(w) = 5w^2$, what is the largest learning rate that still converges?

$\lambda = 10$; $\eta < \frac{2}{10} = 0.2$.

## 4. Two variables

**Question:** $f = x^2 + y^2$, starting at $(3, 4)$, $\eta = 0.25$. Where is it after one step?

$\nabla f = (6, 8)$; $(3 - 1.5, \ 4 - 2) = (1.5, \ 2)$.

## 5. The condition number

**Question:** The Hessian's eigenvalues are $50$ and $0.5$. What is the condition number?

$\frac{50}{0.5} = 100$.

## 6. Mini-batch

**Question:** $10\,000$ examples, $B = 100$. How many steps in an epoch?

$\frac{10\,000}{100} = 100$.

## 7. Momentum

**Question:** $\beta = 0.9$, $\mathbf{v} = 2$, new gradient $1$. What is the new $\mathbf{v}$?

$0.9 \cdot 2 + 1 = 2.8$.

## 8. Diagnosis

**Question:** The loss became `nan` within a few steps. What should be changed first?

The learning rate should be reduced (or the gradient clipped).
