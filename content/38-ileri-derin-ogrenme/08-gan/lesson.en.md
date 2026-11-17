# Generative Adversarial Networks

In the Generative AI Fundamentals module we built a GAN (generative
adversarial network) with NumPy. In short: two networks play against each
other. The **generator** produces an example from random noise; the
**discriminator** looks at an example and gives a probability that it is
real. The discriminator learns to tell them apart, the generator learns to
fool it; when the game reaches a balance the generated examples can no
longer be told from the real ones.

<figure class="fig">
<div class="flow">
<span class="node">noise z</span><span class="arrow">→</span>
<span class="node acc">generator G</span><span class="arrow">→</span>
<span class="node">fake example</span><span class="arrow">→</span>
<span class="node ok">discriminator D</span><span class="arrow">→</span>
<span class="node">real?</span>
</div>
<figcaption>The discriminator is shown real and fake examples in turn. The generator never sees real data; whatever it learns, it learns from the discriminator's reaction.</figcaption>
</figure>

There we wrote the derivatives of both networks by hand. In PyTorch autograd
writes them; the real subject of this section is three things specific to
PyTorch: **two separate optimisers**, choosing where the derivative goes with
`detach()`, and the order of the training steps.

## The data and the two networks

Our goal is simple: produce numbers with mean 3 and standard deviation 0.5.
One-dimensional data lets us see what was learned in a single number.

```python
import torch
from torch import nn

torch.manual_seed(0)
real = 3 + 0.5 * torch.randn(2000, 1, generator=torch.Generator().manual_seed(1))
G = nn.Sequential(nn.Linear(4, 16), nn.ReLU(), nn.Linear(16, 1))
D = nn.Sequential(nn.Linear(1, 16), nn.LeakyReLU(0.2), nn.Linear(16, 1))
z = torch.randn(64, 4)
print(G(z).shape, D(G(z)).shape)
print(sum(p.numel() for p in G.parameters()), sum(p.numel() for p in D.parameters()))
print(round(real.mean().item(), 1), round(real.std().item(), 1))
```

```text
torch.Size([64, 1]) torch.Size([64, 1])
97 49
3.0 0.5
```

- The generator turns 4 numbers of noise into one number; the discriminator
  turns one number into a single score (a logit).
- There is no `Sigmoid` at the end of the discriminator: we compute the loss
  with `nn.BCEWithLogitsLoss`, which applies the sigmoid itself in a
  numerically safer way.
- `LeakyReLU` in the discriminator: it leaves a small slope on the negative
  side too; common in GANs so that the derivative reaches the generator
  without being cut off.

## `detach`: where should the derivative go?

When training the discriminator we show it the fake example with the label
"0". But in this step **only the discriminator** should change; letting the
derivative travel all the way to the generator is wasted work and also
wrong: the generator collects derivatives in the direction "let me be caught
more easily". `fake.detach()` cuts the fake example off the computation
graph.

```python
loss_fn = nn.BCEWithLogitsLoss()
fake = G(z)
d_loss = loss_fn(D(fake.detach()), torch.zeros(64, 1))
d_loss.backward()
print(G[0].weight.grad is None, D[0].weight.grad is not None)
D.zero_grad()
loss_fn(D(fake), torch.zeros(64, 1)).backward()
print(G[0].weight.grad is None)
```

```text
True True
False
```

- With `detach`: there is no derivative on the generator's weight (`None`),
  there is one on the discriminator's.
- Without `detach` the same loss wrote a derivative into the generator too.

## The training loop

Every step does two jobs in order:

1. **Discriminator:** says "1" to the real ones and "0" to the (detached)
   fakes; only `opt_d` takes a step.
2. **Generator:** shows the same fakes to the discriminator, this time
   **without detaching**, and asks for the label "1": "take me for real".
   Only `opt_g` takes a step.

```python
def train_gan(G, D, steps=1500, lr=0.002):
    opt_g = torch.optim.Adam(G.parameters(), lr=lr, betas=(0.5, 0.999))
    opt_d = torch.optim.Adam(D.parameters(), lr=lr, betas=(0.5, 0.999))
    gen = torch.Generator().manual_seed(2)
    ones, zeros = torch.ones(64, 1), torch.zeros(64, 1)
    for step in range(steps):
        xb = real[torch.randint(0, len(real), (64,), generator=gen)]
        fake = G(torch.randn(64, 4, generator=gen))
        opt_d.zero_grad()
        d_loss = loss_fn(D(xb), ones) + loss_fn(D(fake.detach()), zeros)
        d_loss.backward()
        opt_d.step()
        opt_g.zero_grad()
        loss_fn(D(fake), ones).backward()
        opt_g.step()


def samples(G):
    with torch.no_grad():
        return G(torch.randn(2000, 4, generator=torch.Generator().manual_seed(3)))


print(abs(samples(G).mean().item() - 3) < 0.2)
train_gan(G, D)
s = samples(G)
print(abs(s.mean().item() - 3) < 0.2)
print(abs(torch.sigmoid(D(s)).mean().item() - 0.5) < 0.05)
```

```text
False
True
True
```

- Before training the mean of the generated numbers is far from 3; after it,
  closer than 0.2.
- The last line shows the balance: on average the discriminator says about
  0.5 to the generated examples, that is, it is now tossing a coin.
- In the generator's step `D(fake)` also writes derivatives into the
  discriminator's weights; that does no harm, because those weights change
  only through `opt_d`, and `opt_d.zero_grad()` clears them in the next
  step. Calling `opt_d.step()` in the generator's step would be the mistake.
- `betas=(0.5, 0.999)`: trimming Adam's momentum a little is a common setting
  for GANs; since the two networks keep changing relative to each other, a
  long memory amplifies oscillation.

The mean gets close to 3 in every run, but the standard deviation changes
noticeably with the seed (on this computer, between about 0.3 and 0.8 over
five seeds). A GAN does not learn the whole distribution, only as much as it
needs to fool the discriminator; in the notes we look at the best-known
result of this, mode collapse.

## Summary

- GAN: the generator produces examples from noise, the discriminator tells
  real from fake.
- In PyTorch: two networks, two optimisers; every step first the
  discriminator, then the generator.
- In the discriminator's step `fake.detach()`: the derivative does not go to
  the generator.
- The generator's loss is "call the fake 1" (`BCEWithLogitsLoss(D(fake), ones)`).
- Success is measured from the generated examples, not from the loss.
