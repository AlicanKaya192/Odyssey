# Introduction to Generative AI

A model that decides whether an image shows a cat or a dog and a model that
draws a cat that never existed do not learn the same thing. The first learns
to **tell two classes apart**; the second learns **what cats look like**. The
second kind is called a **generative model**; every system that writes text,
draws pictures, or produces sound and code belongs to this family. In this
section we build the distinction with a small, tangible example: the length
and weight of two fish species. From the same data we will first build a
classifier, then a model that produces new fish, and we will measure the
difference between "generating" and "memorising".

## Two kinds of model

<figure class="fig">
  <div class="versus">
    <div class="dim">
      <h5>DISCRIMINATIVE</h5>
<pre><code>model.predict(fish)
# "bream"</code></pre>
      <p>Only decides: which class is this example from?</p>
    </div>
    <div class="ok">
      <h5>GENERATIVE</h5>
<pre><code>model.sample("bream")
# [31.2, 546.3]</code></pre>
      <p>Learns what the data looks like; can produce new examples.</p>
    </div>
  </div>
  <figcaption>Both learn from the same data; only the generative model can recreate it.</figcaption>
</figure>

- A **discriminative model** answers only one question: "Given this example,
  what is the label?" In maths this is written $p(y \mid x)$. Logistic
  regression, decision trees and text classifiers are of this kind.
- A **generative model** models the data itself: "What does an example of
  this kind look like?" That is $p(x)$, or $p(x \mid y)$ per class. Once it
  has learnt this distribution it can **draw samples** from it: new examples
  it has never seen but which resemble the real ones.

Today's large language models are generative models too: they learn the
distribution of the tokens that make up text and pick the next token from
that distribution. We wrote how they do it from scratch in the second module
of the NLP path (Text Generation); in this path we cover the rest of the
generative models and how to build applications around language models.

## The data: two fish species

`gen_data.py` produces the length (cm) and weight (g) of two fish species
(perch and bream). Every run gives the same 600 fish, because the generator
uses a fixed seed.

```python
import numpy as np
from gen_data import make_fish

X, y = make_fish()
y = np.array(y)
print(X.shape)
print(X[:3])
for name in ["perch", "bream"]:
    part = X[y == name]
    print(name, len(part), part.mean(axis=0).round(1))
```

```text
(600, 2)
[[ 33.5 595.6]
 [ 31.2 593.4]
 [ 26.6 496.7]]
perch 319 [ 24.  304.5]
bream 281 [ 31.  555.5]
```

Bream are longer and heavier on average, but the two species overlap: a
26 cm, 450 g fish could be either.

## Describing a species with a distribution

The simplest form of a generative model is this: describe each species'
measurements with a **normal distribution** (Gaussian distribution). With
two measurements we use a two-dimensional normal distribution, which is set
by two things:

- **The mean vector:** the species' typical length and weight.
- **The covariance matrix:** how much each measurement spreads and how the
  two change together. A long fish is heavy; this relationship shows up as
  positive numbers off the diagonal.

We first split the data into training and test sets and build the model from
the training fish only:

```python
rng = np.random.default_rng(0)
order = rng.permutation(len(y))
train, test = order[:450], order[450:]


def fit_gaussian(points):
    return points.mean(axis=0), np.cov(points, rowvar=False)


params = {}
for name in ["perch", "bream"]:
    part = X[train][y[train] == name]
    params[name] = fit_gaussian(part)
    mean, cov = params[name]
    print(name, mean.round(1), cov.round(1).tolist())
```

```text
perch [ 24.1 304.4] [[15.5, 197.0], [197.0, 4453.5]]
bream [ 30.8 559.1] [[13.1, 280.2], [280.2, 10012.2]]
```

Five numbers per species (two means, the three distinct covariance values)
and the share of each species are the whole "model". No neural network, but the idea
is the same: **learning a distribution from data**.

## The same model can classify

Someone who knows each species' distribution can also say which species a
new fish resembles more. With Bayes' rule: the fish's **probability density**
(likelihood) under the species' distribution is multiplied by the species'
overall share (prior), and the larger one wins. For easier arithmetic we
work with logarithms.

```python
def log_density(points, mean, cov):
    diff = points - mean
    inv = np.linalg.inv(cov)
    _, logdet = np.linalg.slogdet(cov)
    dist = np.einsum("ij,jk,ik->i", diff, inv, diff)
    return -0.5 * (dist + logdet + 2 * np.log(2 * np.pi))


names = ["perch", "bream"]
scores = []
for name in names:
    prior = np.mean(y[train] == name)
    scores.append(log_density(X[test], *params[name]) + np.log(prior))
pred = np.array(names)[np.argmax(scores, axis=0)]
print("generative:", round(float(np.mean(pred == y[test])), 3))

from sklearn.linear_model import LogisticRegression

clf = LogisticRegression(max_iter=1000).fit(X[train], y[train])
print("logistic:", round(clf.score(X[test], y[test]), 3))
```

```text
generative: 0.9
logistic: 0.88
```

The two models are almost equally accurate on the 150 test fish. The
difference is elsewhere: logistic regression only **decides**. You cannot
ask it to "show me a bream"; it holds no information about what a fish
looks like. The generative model can do that.

## Generating: drawing from the distribution

```python
gen = np.random.default_rng(42)
mean, cov = params["bream"]
new_fish = gen.multivariate_normal(mean, cov, size=5)
print(new_fish.round(1))

many = gen.multivariate_normal(mean, cov, size=1000)
real = X[train][y[train] == "bream"]
print("generated", many.mean(axis=0).round(1), many.std(axis=0).round(1))
print("real     ", real.mean(axis=0).round(1), real.std(axis=0).round(1))
```

```text
[[ 32.4 528.5]
 [ 26.6 484. ]
 [ 39.3 754.2]
 [ 31.2 546.3]
 [ 32.8 560.7]]
generated [ 31.1 566.2] [ 3.7 99.1]
real      [ 30.8 559.1] [ 3.6 99.8]
```

These five fish are not in the data; the model **made them up**. But not at
random: the mean and spread of a thousand samples are very close to those of
the real bream. This is the first way to evaluate a generative model: not
whether each sample is "right", but **whether the statistics of what it
generates resemble reality**. In generation there is no single right answer.

## Generating or memorising?

There is an easy trick: return a random fish from the training data as it
is. The statistics match perfectly, but the model has generated nothing; it
has only **copied**. In real generative models this is a serious problem: a
model that returns a text or image from its training data almost verbatim
can leak personal information or copyrighted content.

A simple way to measure it is the distance from each generated sample to its
**nearest neighbour** in the training data. Since length is in centimetres
and weight in grams, we first bring both measurements to the same scale
(their standard deviation):

```python
scale = real.std(axis=0)


def nearest_distance(points, data):
    a = points / scale
    b = data / scale
    d = np.sqrt(((a[:, None, :] - b[None, :, :]) ** 2).sum(axis=2))
    return d.min(axis=1)


copies = real[gen.integers(0, len(real), size=100)]
print("model :", np.median(nearest_distance(many[:100], real)).round(3))
print("copier:", np.median(nearest_distance(copies, real)).round(3))
```

```text
model : 0.089
copier: 0.0
```

Every sample of the copying "model" sits exactly on a training fish
(distance 0). The real model produces new points; they are still close to
the training fish, because it learnt from them. A healthy generative model
sits somewhere in between: **it resembles reality, but it is not a copy.**

## Why are generative models hard?

Here two measurements and one normal distribution were enough. An image,
however, has millions of pixels and a text thousands of tokens. At these
sizes a distribution cannot be described by a single mean and covariance,
so generative models developed different ideas:

| Idea | In short | In this path |
|---|---|---|
| Autoencoder | Compress the data into a small code and expand it back | 02 |
| VAE | Make the code a distribution and sample from it | 03 |
| GAN | Make a generator and a discriminator compete | 04 |
| Diffusion | Remove noise step by step | 05 |
| Language model | Learn the distribution of the next token | 06–08 |

The second half of the module is about language models: how they generate,
why they are sometimes confidently wrong (hallucination), how they are
supported with outside documents (RAG) and how they are adapted to our own
work (fine-tuning, LoRA).

## Summary

- A discriminative model learns $p(y \mid x)$ and decides; a generative
  model learns the distribution of the data and **can produce new examples**.
- The simplest generative model: fit a normal distribution to each class.
  The same model can also classify (Bayes' rule).
- In generation there is no single right answer; the **statistics** of what
  is generated should resemble reality.
- A good model resembles reality but **does not copy**; the nearest
  neighbour distance is a simple way to measure memorisation.
