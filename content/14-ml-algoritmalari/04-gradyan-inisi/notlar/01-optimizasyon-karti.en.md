## Kinds of gradient descent

| Kind | Each step uses | Plus | Minus |
|---|---|---|---|
| Batch | all the data | steady, smooth descent | slow on large data |
| Mini-batch | a small group (32–512) | fast, suits GPUs | noisy |
| Stochastic (SGD) | one sample | very fast steps | very noisy |
| Momentum | accumulated gradients | fast in narrow valleys | one more setting (`β`) |
| Adam | a step adapted per weight | robust to scale | more settings (`β₁`, `β₂`) |

## Settings

- **Learning rate:** first a rough sweep (0.001, 0.01, 0.1, 1); if the loss
  diverges make it smaller, if it is too slow make it larger.
- **Stopping:** a fixed number of steps, or when the loss barely falls any more
  (`|L_before − L_after| < tolerance`).
- **Learning-rate schedule:** large steps first, then small ones; it reduces
  SGD's wandering at the bottom.

## Common mistakes

- Forgetting scaling: a single learning rate does not fit all weights.
- Forgetting the `1/n` in the gradient: steps grow with the data and diverge.
- Not shuffling the data every epoch: the mini-batches always come in the same
  order.
- Not checking the written gradient against the numerical gradient.
