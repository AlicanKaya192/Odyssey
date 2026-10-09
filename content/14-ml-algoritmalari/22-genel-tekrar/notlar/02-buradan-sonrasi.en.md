In the ML Algorithms module you built the core of classical machine learning. A few paths open
from here:

- **Deep learning.** The same network as in Section 20, with more layers.
  PyTorch or TensorFlow compute derivatives automatically (autograd); the
  library writes the `backward` function you wrote. Convolutional networks
  (CNNs) for images, attention and transformers for text and sequences are the
  next steps.
- **Gradient boosting libraries.** XGBoost, LightGBM and CatBoost apply the
  idea of Section 12 quickly and powerfully on large tabular data; they are
  common in tabular data competitions.
- **Probabilistic modelling.** The thinking behind Naive Bayes and GMMs:
  Bayesian statistics, latent variable models, predictions that measure
  uncertainty.
- **Time series.** Validation on ordered data follows other rules; Odyssey has
  a separate path for it.
- **Big data and production.** Serving a model through an API (Writing APIs),
  packaging it with Docker, working on large data (the Big Data path).

Keep the habit of writing from scratch: first write a new method by hand on a
small example, then compare it with the library. When a method gives an
unexpected result, this habit tells you where to look.
