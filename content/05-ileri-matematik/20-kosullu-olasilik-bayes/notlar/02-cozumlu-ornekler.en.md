A worked example for each method in the lesson, step by step. Try each question yourself first, then read the solution.

## 1. The two directions of a condition

**Question:** A class of $40$ has $25$ girls; $10$ of the girls and $6$ of
the boys wear glasses. What are $P(\text{glasses} \mid \text{girl})$ and
$P(\text{girl} \mid \text{glasses})$?

$\frac{10}{25} = 0.4$. $16$ people wear glasses, $10$ of them girls:
$\frac{10}{16} = 0.625$. The denominators are different groups.

## 2. The product rule

**Question:** Two bulbs are taken without replacement from $2$ broken and
$8$ working. What is the probability that the first is broken and the
second works?

$\frac{2}{10} \cdot \frac{8}{9} = \frac{16}{90} = \frac{8}{45}$. The second
factor is conditional: once the first is broken, $8$ of the $9$ left work.

## 3. Total probability

**Question:** $30$ percent of days are rainy. On rainy days the bus is late
with probability $40$ percent, on dry days $10$ percent. What is the
probability that it is late on a random day?

$0.3 \cdot 0.4 + 0.7 \cdot 0.1 = 0.12 + 0.07 = 0.19$.

## 4. Bayes

**Question:** In the same setting the bus was late. What is the probability
that it was a rainy day?

$\frac{0.12}{0.19} \approx 0.632$. Being late raised the belief in rain from
$0.3$ to $0.63$.

## 5. A test question

**Question:** The disease rate is $2$ percent; the sensitivity $90$ percent;
the false positive rate $10$ percent. What is the probability of being ill
after a positive result?

$P(+) = 0.9 \cdot 0.02 + 0.1 \cdot 0.98 = 0.018 + 0.098 = 0.116$.
$P(I \mid +) = \frac{0.018}{0.116} \approx 0.155$.

## 6. With natural frequencies

**Question:** Think of the same question with $1000$ people.

$20$ ill, $18$ of them positive. $980$ healthy, $98$ of them positive.
$\frac{18}{116} \approx 0.155$ of the positives are ill.

## 7. A second test

**Question:** The same person is also positive on an independent second
test. Now what?

Prior $0.155$: $\frac{0.9 \cdot 0.155}{0.9 \cdot 0.155 + 0.1 \cdot 0.845}
\approx 0.623$.

## 8. The odds form

**Question:** Solve the fifth example with odds.

Prior odds $2 : 98 = 1 : 49$. Likelihood ratio $\frac{0.9}{0.1} = 9$.
Posterior odds $9 : 49$; probability $\frac{9}{58} \approx 0.155$.

## 9. Two boxes

**Question:** The first box has $3$ red and $2$ blue balls, the second $1$
red and $4$ blue. A box is chosen at random and a ball drawn; it is red.
What is the probability it came from the first box?

$\frac{0.5 \cdot 0.6}{0.5 \cdot 0.6 + 0.5 \cdot 0.2} = \frac{0.3}{0.4} =
0.75$.

## 10. Naive Bayes

**Question:** Two classes with $P(A) = 0.6$ and $P(B) = 0.4$. For an
example's two features $P(x_1 \mid A) = 0.2$, $P(x_2 \mid A) = 0.5$,
$P(x_1 \mid B) = 0.6$, $P(x_2 \mid B) = 0.3$. Which class is chosen?

$A$: $0.6 \cdot 0.2 \cdot 0.5 = 0.06$. $B$: $0.4 \cdot 0.6 \cdot 0.3 =
0.072$. $B$ is chosen; $P(B \mid x) = \frac{0.072}{0.132} \approx 0.545$.
