## Layers and activations

| Activation | Formula | Derivative | Where |
|---|---|---|---|
| Sigmoid | `1 / (1 + e^(−z))` | `σ (1 − σ)` | binary output |
| tanh | `(e^z − e^(−z)) / (e^z + e^(−z))` | `1 − tanh²` | hidden layer (small networks) |
| ReLU | `max(0, z)` | 1 if `z > 0`, else 0 | hidden layer (deep networks) |
| Softmax | `e^(z_i) / Σ e^(z_j)` | `p − y` with cross-entropy | multi-class output |

Without activations the layers would multiply into a single linear
transformation again; depth would mean nothing.

## Backpropagation (one hidden layer)

| Step | Formula |
|---|---|
| Forward | `H = f(X W₁ + b₁)`, `p = σ(H W₂ + b₂)` |
| Output | `dz₂ = (p − y) / n` |
| Output weights | `dW₂ = Hᵀ dz₂`, `db₂ = Σ dz₂` |
| Hidden | `dz₁ = (dz₂ W₂ᵀ) ⊙ f′(…)` |
| Hidden weights | `dW₁ = Xᵀ dz₁`, `db₁ = Σ dz₁` |

## In practice

- scikit-learn: `MLPClassifier(hidden_layer_sizes=(10,), activation="tanh")`.
- Deep learning libraries (PyTorch, TensorFlow) compute derivatives
  **automatically** (autograd); there is no need to write backpropagation by
  hand.
- Scale the inputs; initialise weights with small random numbers.
- The learning rate and the number of epochs are the most important
  settings; watch the validation loss.

## Common mistakes

- Initialising weights with zeros (or all with the same number): all neurons
  stay identical (measured in the note).
- Not scaling: tanh and sigmoid saturate on large inputs and the derivative
  drops to zero.
- Writing derivatives by hand without checking: compare with numerical
  derivatives.
- Stopping at training accuracy: a test or validation set is a must.
