# Autoencoders and VAEs

In the Generative AI Fundamentals module we built the autoencoder and the
variational autoencoder (VAE) with NumPy. In short: the **encoder** squeezes
the input into a **latent code** of a few numbers, the **decoder** tries to
rebuild the input from that code; by shrinking the reconstruction error the
network learns to pass the essence of the data through a narrow place. A VAE
produces the code not as a single point but as a **distribution** (a mean and
a variance); so we can draw new codes from that distribution and produce
**new examples**.

There we wrote the derivatives by hand. In PyTorch autograd writes them; this
section's PyTorch-specific lesson is the VAE's **reparameterisation trick**:
getting a derivative through random sampling.

## Data: 8×8 digits

```python
import torch
from torch import nn
import torch.nn.functional as F
from sklearn.datasets import load_digits

digits = load_digits()
x = torch.tensor(digits.data / 16.0, dtype=torch.float32)
x_train, x_test = x[:1500], x[1500:]
print(x.shape, x.min().item(), x.max().item())
```

```text
torch.Size([1797, 64]) 0.0 1.0
```

1797 handwritten digits that come with scikit-learn; each has 64 pixels
between 0 and 16. We divided by 16 to bring them into `[0, 1]`.

## The autoencoder

```python
class AutoEncoder(nn.Module):
    def __init__(self, code=4):
        super().__init__()
        self.encoder = nn.Sequential(nn.Linear(64, 32), nn.ReLU(), nn.Linear(32, code))
        self.decoder = nn.Sequential(nn.Linear(code, 32), nn.ReLU(), nn.Linear(32, 64),
                                     nn.Sigmoid())

    def forward(self, x):
        return self.decoder(self.encoder(x))


def train(model, loss_fn, epochs=30):
    loader = torch.utils.data.DataLoader(x_train, batch_size=64, shuffle=True,
                                         generator=torch.Generator().manual_seed(0))
    opt = torch.optim.Adam(model.parameters(), lr=0.005)
    for epoch in range(epochs):
        model.train()
        for xb in loader:
            opt.zero_grad()
            loss_fn(model, xb).backward()
            opt.step()
    return model.eval()


def ae_loss(model, xb):
    return F.mse_loss(model(xb), xb)


torch.manual_seed(0)
ae = train(AutoEncoder(), ae_loss)
with torch.no_grad():
    code = ae.encoder(x_test)
    err = F.mse_loss(ae(x_test), x_test).item()
baseline = F.mse_loss(x_train.mean(dim=0).expand_as(x_test), x_test).item()
print(code.shape)
print(err < baseline / 2)
```

```text
torch.Size([297, 4])
True
```

- 64 pixels were squeezed into 4 numbers: `code` is `(297, 4)`.
- The `nn.Sigmoid` in the last layer squeezes the output into `[0, 1]`; the
  pixels are in that range too.
- The baseline: answering every test digit with the training set's
  **average digit**. The autoencoder's error is less than half of that: 4
  numbers carry the digit's shape.
- We gave the `DataLoader` a tensor directly; no label is needed, the input
  is its own target.

## The VAE: the code is a distribution

A VAE's encoder produces two things: a mean `mu` and a log variance
`logvar`. The code is drawn from that distribution. The problem: "draw at
random" has no derivative; the derivative cannot reach `mu` and `logvar`.
**Reparameterisation** moves the randomness outside: `z = mu + σ · ε`, with
`ε` from a standard normal. The randomness now lives in `ε`; `mu` and `σ` are
part of an ordinary computation and get derivatives.

```python
class VAE(nn.Module):
    def __init__(self, code=4):
        super().__init__()
        self.body = nn.Sequential(nn.Linear(64, 32), nn.ReLU())
        self.mu = nn.Linear(32, code)
        self.logvar = nn.Linear(32, code)
        self.decoder = nn.Sequential(nn.Linear(code, 32), nn.ReLU(), nn.Linear(32, 64),
                                     nn.Sigmoid())

    def reparameterize(self, mu, logvar):
        std = torch.exp(0.5 * logvar)
        return mu + std * torch.randn_like(std)

    def forward(self, x):
        h = self.body(x)
        mu, logvar = self.mu(h), self.logvar(h)
        return self.decoder(self.reparameterize(mu, logvar)), mu, logvar


def kl_term(mu, logvar):
    return -0.5 * torch.mean(torch.sum(1 + logvar - mu ** 2 - logvar.exp(), dim=1))


print(kl_term(torch.zeros(3, 4), torch.zeros(3, 4)).item() + 0.0)
mu = torch.zeros(2, 4, requires_grad=True)
logvar = torch.zeros(2, 4, requires_grad=True)
VAE().reparameterize(mu, logvar).sum().backward()
print(mu.grad.shape, logvar.grad is not None)
```

```text
0.0
torch.Size([2, 4]) True
```

- The KL term (Kullback–Leibler divergence) pulls the code's distribution
  towards a standard normal. If the code already is a standard normal (`mu =
  0`, `logvar = 0`) the KL is exactly 0 (`+ 0.0` prints the minus zero the
  computation gives as `0.0`).
- The last line shows reparameterisation working: from the sum of the
  randomly drawn `z` a derivative reached `mu` and `logvar`.

## Training the VAE and generating new digits

```python
def vae_loss(model, xb):
    recon, mu, logvar = model(xb)
    rec = F.binary_cross_entropy(recon, xb, reduction="sum") / len(xb)
    return rec + kl_term(mu, logvar)


torch.manual_seed(0)
vae = train(VAE(), vae_loss)
with torch.no_grad():
    z = torch.randn(5, 4, generator=torch.Generator().manual_seed(1))
    samples = vae.decoder(z)
print(samples.shape, bool(samples.min() >= 0), bool(samples.max() <= 1))
```

```text
torch.Size([5, 64]) True True
```

- The reconstruction term is binary cross-entropy: since the pixels are in
  `[0, 1]`, they can be read as "the probability that the pixel is on".
- Generation needs no encoder at all: we drew 5 codes from a standard normal
  and passed them **only through the decoder**; out came 5 new 64-pixel
  images. That is why the KL term matters: training keeps the codes close to
  a standard normal, so a code drawn from there lands on a meaningful digit.

## Summary

- An autoencoder: encoder → narrow code → decoder; the loss is the
  reconstruction error, no labels.
- A VAE produces the code as a distribution (`mu`, `logvar`); the loss is
  reconstruction + KL.
- Reparameterisation: `z = mu + exp(0.5·logvar) · ε`. The randomness moves
  into `ε`, and the derivative reaches `mu` and `logvar`.
- To generate, draw a code from a standard normal and run only the decoder.
