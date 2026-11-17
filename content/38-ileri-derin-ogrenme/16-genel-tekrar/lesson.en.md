# Overall Review

You have reached the end of the Sequences, Generative Models and Deployment
module. We turned words and numbers into vectors with an embedding layer and
read sequences with RNNs, LSTMs, 1D convolution and the Transformer. Then we
moved on to models that generate data: the autoencoder, the VAE, the GAN; we
saw learning without labels with a contrastive loss, and adapting a large
model with few parameters with LoRA. In the last part we looked at the life
of a trained model: measuring its speed, exporting it, shrinking it, making
results reproducible and serving it behind a function. This section walks
the path once more; at the end there is a short example where the pieces work
together.

<figure class="fig">
<div class="flow">
<span class="node">Sequences<br><small>00–06</small></span><span class="arrow">→</span>
<span class="node">Generative<br><small>07–08</small></span><span class="arrow">→</span>
<span class="node">Few labels<br><small>09–10</small></span><span class="arrow">→</span>
<span class="node">Deployment<br><small>11–14</small></span><span class="arrow">→</span>
<span class="node acc">Project<br><small>15</small></span>
</div>
<figcaption>The module's path: read the sequence, generate data, learn with few labels, prepare the model for delivery, build an end-to-end detector.</figcaption>
</figure>

## 1. Sequences (Sections 0–6)

- **Embeddings and padding:** word → id → `nn.Embedding`; short sequences
  are lengthened with a padding id, `padding_idx` and a mask keep track of
  the padding (00).
- **RNN, LSTM, GRU:** the hidden state summarises the sequence so far; LSTM
  and GRU carry long dependencies with gates. With `batch_first=True` the
  input is `(B, T, D)`; a packed sequence lets the padding be skipped (01).
- **Classification and forecasting:** the last hidden state or pooling → a
  linear layer (02); sliding windows and recursive forecasting, measuring
  against baselines (03).
- **1D convolution:** local patterns, the receptive field, dilated
  convolution; often faster than an RNN (04).
- **Language model:** predicting the next character, sampling with a
  temperature (05).
- **Attention and the Transformer:** query–key–value, the causal mask,
  positional embeddings; `nn.TransformerEncoder` (06).

## 2. Generative models (Sections 7–8)

- **Autoencoder:** rebuilding from a narrow code; the reconstruction error as
  an anomaly measure (07).
- **VAE:** the code is a distribution; reparameterisation `z = mu + σ·ε`, the
  loss is reconstruction + KL (07).
- **GAN:** two networks, two optimisers; `fake.detach()` in the
  discriminator's step, the generator's loss is "call the fake 1"; success is
  measured from the examples (08).

## 3. Learning with few labels (Sections 9–10)

- **Contrastive learning:** two views of the same example close; NT-Xent,
  temperature; the negatives prevent collapse (09).
- **LoRA:** the base frozen, `ΔW = B·A` trained; `r · (inputs + outputs)`
  parameters, the adaptation is plugged in and out or folded into the weight
  (10).

## 4. Deployment (Sections 11–14)

- **Performance:** measure first, compare ratios; batches, `inference_mode`,
  `autocast`, profiling (11).
- **Exporting:** `torch.export`, a free batch size (`Dim`), `.pt2` loads
  without the class; `torch.cond` for a data-dependent branch (12).
- **Shrinking:** `int8` quantisation (4 times), a scale per channel; pruning
  and structured pruning (13).
- **Reproducibility and serving:** seeds, an experiment record, a data hash;
  a prediction function that loads the model once and checks the input (14).

## 5. The project (Section 15)

A sensor fault detector: get to know the data, a baseline with a simple rule,
a 1D convolutional network, precision and recall, a delivery package.

## All together

The short example below combines four parts of the module: reading sequences
with an embedding and 1D convolution (00, 04), reproducible training with a
seed (14), `int8` quantisation (13), and exporting and checking against a
golden output (12). The task: in sequences of numbers 0–9, does "3, 5" occur
in a row?

```python
import torch
import torch.nn.functional as F
from torch import nn
from dl_data import make_sequences


class Detector(nn.Module):
    def __init__(self):
        super().__init__()
        self.embed = nn.Embedding(10, 8)
        self.conv = nn.Conv1d(8, 16, kernel_size=2)
        self.head = nn.Linear(16, 2)

    def forward(self, ids):
        h = self.embed(ids).transpose(1, 2)
        return self.head(torch.relu(self.conv(h)).amax(dim=2))


x_np, y_np = make_sequences(600, seed=7)
x, y = torch.tensor(x_np), torch.tensor(y_np)
torch.manual_seed(0)
model = Detector()
opt = torch.optim.Adam(model.parameters(), lr=0.01)
gen = torch.Generator().manual_seed(1)
for epoch in range(20):
    perm = torch.randperm(500, generator=gen)
    for i in range(0, 500, 50):
        idx = perm[i:i + 50]
        opt.zero_grad()
        F.cross_entropy(model(x[idx]), y[idx]).backward()
        opt.step()
model.eval()


def accuracy(m):
    with torch.no_grad():
        return (m(x[500:]).argmax(1) == y[500:]).float().mean().item()


acc = accuracy(model)
with torch.no_grad():
    for layer in (model.conv, model.head):
        scale = layer.weight.abs().max() / 127
        q = torch.round(layer.weight / scale).clamp(-127, 127).to(torch.int8)
        layer.weight.copy_(q.float() * scale)
batch = torch.export.Dim("batch")
ep = torch.export.export(model, (x[:4],), dynamic_shapes=({0: batch},))
with torch.no_grad():
    golden = model(x[500:])
print(acc > 0.95, abs(accuracy(model) - acc) < 0.02)
print(torch.allclose(ep.module()(x[500:]), golden, atol=1e-5), ep.module()(x[:7]).shape)
```

```text
True True
True torch.Size([7, 2])
```

- `transpose(1, 2)`: the embedding gives `(B, T, D)`, `Conv1d` wants
  `(B, D, T)`.
- A convolution with kernel size 2 looks at two numbers in a row;
  `amax(dim=2)` makes it irrelevant where in the sequence the pattern is.
- With the weights brought down to `int8` the accuracy stayed close; the
  exported model matches the golden output and works with a batch of 7 too.

## Next

In this module we did everything with small models that finish in seconds on
a CPU. Real systems are built from the same parts; the difference is in
scale, data and hardware. The notes have a one-page summary of the module and
where to go from here.
