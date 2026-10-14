| | PCA | Neural network autoencoder |
|---|---|---|
| Encoding | Linear projection | Non-linear layers |
| Training | A single SVD, under a second | Thousands of steps, needs tuning (learning rate, momentum) |
| Result | The same on every run | Varies a little with the initial weights and arithmetic differences |
| Error with the same code size | Higher (0.0539 in 2 dimensions) | Lower (0.0393 in 2 dimensions) |
| When | A quick baseline, little data | Curved structure, a lot of data |

**Try PCA first.** If the network's error is not clearly lower than PCA's,
the extra complexity is not worth it. In this section the difference was
clear, but it may not be for every dataset.

**Common mistakes:**

- **Using test data in training.** An autoencoder can memorise too; the
  reconstruction error is always measured on images it has not seen.
- **PCA without subtracting the mean.** Without `X - mean` before the SVD the
  first direction describes the data's mean instead of its spread.
- **An output activation that does not fit the data.** If the pixels are
  between 0 and 1, `sigmoid` makes sense at the output; `tanh` gives the
  range (−1, 1).
- **Choosing a code that is too wide.** A 64-number code for 64 pixels
  compresses nothing; the error comes out near zero but the model has learnt
  nothing.
