## Kinds

| Kind | Feature | Within-class distribution | scikit-learn |
|---|---|---|---|
| Gaussian | continuous numbers | normal (mean, variance) | `GaussianNB` |
| Multinomial | counts (word counts) | word shares | `MultinomialNB` |
| Bernoulli | 0/1 (is the word there) | the probability of presence | `BernoulliNB` |

## Formula

`class = argmax ( log P(c) + Σ log P(xᵢ | c) )`

- The prior `P(c)`: the class's share in training.
- Gaussian: `log N(x | mean, var) = −½ log(2π var) − (x − mean)² / (2 var)`.
- Multinomial: `log P(word | c) = log((count + α) / (total + α · V))`, where `V`
  is the vocabulary size.

## Pluses and minuses

- Very fast (one pass), works with little data, handles many features
  (thousands of words), updates easily with new data.
- Because of the independence assumption its probabilities can be
  overconfident; it cannot learn interactions between features.

## Common mistakes

- Multiplying probabilities: underflow. Add the logarithms.
- Turning off smoothing (`alpha`): a single unseen word wipes out the decision.
- A zero-variance feature in Gaussian NB: a division error; that is why
  scikit-learn adds a small margin.
