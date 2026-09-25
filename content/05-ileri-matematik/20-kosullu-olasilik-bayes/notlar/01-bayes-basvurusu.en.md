A short version of everything in the lesson. Come back here when you get stuck on a question.

## Rules

| Name | Formula |
|---|---|
| conditional probability | $P(B \mid A) = \dfrac{P(A \cap B)}{P(A)}$ |
| product rule | $P(A \cap B) = P(A) \, P(B \mid A)$ |
| total probability | $P(B) = \sum_i P(B \mid A_i) \, P(A_i)$ |
| Bayes | $P(A \mid B) = \dfrac{P(B \mid A) \, P(A)}{P(B)}$ |
| odds form | posterior odds $=$ prior odds $\times$ likelihood ratio |
| conditional independence | $P(A \cap B \mid C) = P(A \mid C) \, P(B \mid C)$ |

## Names

| Term | Meaning |
|---|---|
| prior $P(A)$ | the belief before the evidence |
| likelihood $P(B \mid A)$ | the probability of the evidence if $A$ is true |
| evidence $P(B)$ | the total probability of the evidence |
| posterior $P(A \mid B)$ | the belief after the evidence |
| sensitivity | $P(+ \mid \text{ill})$ |
| false positive rate | $P(+ \mid \text{healthy})$ |

## A template for test questions

1. Write the prior: $P(I)$.
2. The two ways to be positive: $P(+ \mid I) P(I)$ and $P(+ \mid H) P(H)$.
3. $P(+)$ is the sum of the two.
4. $P(I \mid +) = \frac{\text{first way}}{P(+)}$.

Or the same four steps with natural frequencies for $10{,}000$ people.

## Sequential updating

The posterior becomes the prior of the next independent piece of evidence.
In odds form each piece of evidence multiplies the odds by the likelihood
ratio once more.

## Naive Bayes

$$
P(\text{class} \mid x_1, \dots, x_n) \propto P(\text{class}) \prod_i P(x_i \mid \text{class})
$$

The class with the largest value is chosen; if a probability is needed,
divide by the total.

## Practical tips

- Check the direction of the condition: "positive if ill" or "ill if
  positive"?
- For rare events the prior decides the result.
- Natural frequencies (numbers of people) keep intuition on track.
- Ask whether the pieces of evidence are independent.
