In backpropagation through time the derivative is multiplied once more by
`W_h` and the derivative of `tanh` at every step. Going 40 steps back means
40 factors. If these factors are below one on average, the derivative
**vanishes** (vanishing gradient); if above, it **explodes** (exploding
gradient). Let us measure it in an RNN with random weights:

```python
import numpy as np

H = 32
for scale in [0.1, 0.25, 0.5]:
    rng = np.random.default_rng(0)
    Wh = rng.normal(0, scale, (H, H))
    hs = [np.zeros(H)]
    for t in range(40):
        hs.append(np.tanh(rng.normal(0, 1, H) + hs[-1] @ Wh))
    dh = np.ones(H)
    norms = []
    for t in reversed(range(1, 41)):
        norms.append(np.linalg.norm(dh))
        dh = Wh @ ((1 - hs[t] ** 2) * dh)
    print(scale, " ".join(f"{norms[k]:.0e}" for k in [0, 10, 20, 30, 39]))
```

```text
0.1 6e+00 1e-04 2e-09 7e-14 4e-18
0.25 6e+00 5e-01 2e-02 3e-03 8e-04
0.5 6e+00 4e+01 3e+02 1e+03 6e+02
```

The columns are the size of the derivative 0, 10, 20, 30 and 39 steps back
from the end.

- With small weights (0.1) the derivative falls from 6 to 0.0001 in 10 steps
  and to 10⁻¹⁸ in 39 steps: nothing can be learned from a word 40 words
  earlier.
- With large weights (0.5) the derivative grows more than a hundredfold; a
  single update can wreck the weights.
- The cure for exploding is the **gradient clipping** we used in the lesson.
  The cure for vanishing is not so simple: the network's structure has to
  change. LSTM and GRU were designed for this (the second note).
- In the lesson sentences have at most 11 words, so vanishing was not a
  problem. In real texts the subject at the start of a paragraph can be
  dozens of words away from the pronoun at its end.
