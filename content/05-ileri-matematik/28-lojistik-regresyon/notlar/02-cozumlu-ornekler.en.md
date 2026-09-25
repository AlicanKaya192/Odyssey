A worked example for each method in the lesson, step by step. Try each question yourself first, then read the solution.

## 1. Sigmoid values

**Question:** What are $\sigma(0)$, $\sigma(2)$, $\sigma(-2)$?

$0.5$; $\frac{1}{1 + e^{-2}} \approx 0.881$; $1 - 0.881 = 0.119$.

## 2. Odds and log-odds

**Question:** $p = 0.75$. What are the odds and the log-odds?

Odds $\frac{0.75}{0.25} = 3$; log-odds $\ln 3 \approx 1.099$.

## 3. From log-odds to probability

**Question:** $z = -1$. What is $p$?

Odds $e^{-1} \approx 0.368$; $p = \frac{0.368}{1.368} \approx 0.269$.

## 4. Interpreting a coefficient

**Question:** A feature has coefficient $0.4$. What happens to the odds
when the feature rises by one unit?

They are multiplied by $e^{0.4} \approx 1.49$; they rise by about $49$
percent.

## 5. The decision boundary

**Question:** $z = 2x_1 - x_2 - 4$. Which class is the point $(3, 1)$
assigned to?

$z = 6 - 1 - 4 = 1 > 0$: class $1$, $p = \sigma(1) \approx 0.731$.

## 6. Log-loss for one example

**Question:** $y = 0$, $p = 0.3$. What is the loss?

$-\ln(1 - 0.3) = -\ln 0.7 \approx 0.357$.

## 7. Average log-loss

**Question:** Two examples: ($y = 1$, $p = 0.8$) and ($y = 0$, $p = 0.4$).
What is the average loss?

$-\ln 0.8 \approx 0.223$ and $-\ln 0.6 \approx 0.511$; average
$\approx 0.367$.

## 8. The gradient

**Question:** $x = (1, 3)$, $y = 0$, $p = 0.7$. What is the gradient of the
loss with respect to $w$?

$(p - y)x = 0.7 \cdot (1, 3) = (0.7, \ 2.1)$.

## 9. Softmax

**Question:** The scores are $(1, 1, 0)$. What are the probabilities?

$e, e, 1$; sum $2e + 1 \approx 6.437$. $p \approx (0.422, \ 0.422, \
0.155)$.

## 10. Choosing a threshold

**Question:** For a disease the model gives $p = 0.3$. If the threshold was
chosen as $0.2$, what is the decision?

$0.3 \geq 0.2$: "may be ill", sent for further tests. With a threshold of
$0.5$ it would have been missed.
