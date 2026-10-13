The NLP path ends here. Across two modules you walked the whole road from
cleaning text to the transformer block, building every piece with your own
hands. From here it opens in a few directions.

## Scaling up

Everything in this module was small and written with NumPy; we computed the
derivatives by hand. In real models the same ideas run with deep learning
libraries that **take derivatives automatically**, and on graphics cards
(GPUs): the library does the backward pass, you only write the forward pass.
Every backward pass you wrote by hand in this module (08, 09, 10) lets you
understand what those libraries do behind the scenes.

Things to try next:

- Rewrite the attention model of 10 and the block of 11 with a deep learning
  library and **train** them on a small text: a character-level language
  model is a good first project.
- Plug the embeddings of a pretrained transformer with open weights into the
  search engine of 15 and measure: how does 12's learning curve change?
- Repeat the steps of 15 with your own text (emails, notes, a forum): the
  index, hybrid search, measurement, the threshold, error analysis.

## Links to other paths

| Path / module | Which part of this module |
|---|---|
| Mathematics (MAT 2) | vectors, matrix multiplication, SVD, backpropagation, entropy |
| ML Algorithms | inside a neural network, backpropagation, gradient descent |
| Algorithm Techniques | dynamic programming (Viterbi, LCS, beam search) |
| Time Series | sequence models, why order matters |
| API | serving a search engine or a classifier as a service |
| Big Data | counting piece by piece over very large texts |

## Open questions

The fast-changing part of this field is the large models themselves; the
part that does not change is the foundations you saw in this module. When
you meet a new method, ask the same questions:

- What does it predict during training? (the next word, a hidden word, the
  context)
- How does it split text, and how does it see order?
- What was it measured with, and what does that measure miss?
- Which domain does its data come from, and what biases does it carry?
