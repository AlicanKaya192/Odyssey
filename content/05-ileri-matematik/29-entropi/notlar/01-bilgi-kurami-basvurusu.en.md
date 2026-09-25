A short version of everything in the lesson. Come back here when you get stuck on a question.

## Definitions

| Concept | Formula |
|---|---|
| information | $I(x) = -\log_2 p(x)$ |
| entropy | $H(P) = -\sum p(x)\log_2 p(x)$ |
| cross-entropy | $H(P, Q) = -\sum p(x)\log_2 q(x)$ |
| KL divergence | $D_{\mathrm{KL}}(P \parallel Q) = \sum p(x)\log_2\frac{p(x)}{q(x)}$ |
| relationship | $H(P, Q) = H(P) + D_{\mathrm{KL}}(P \parallel Q)$ |
| information gain | $H(\text{parent}) - \sum \frac{n_k}{n} H(\text{child}_k)$ |
| perplexity | $2^{H}$ (bits) or $e^{H}$ (nats) |

## Properties

- $0 \leq H(P) \leq \log_2 K$; the largest value is for the uniform
  distribution.
- $H(P, Q) \geq H(P)$, $D_{\mathrm{KL}} \geq 0$; equality only when
  $P = Q$.
- KL is not symmetric.
- $0 \log 0 = 0$; if $q = 0$ where $p > 0$, KL and cross-entropy are
  infinite.

## Useful values

| $p$ | $-\log_2 p$ | $-\ln p$ |
|---|---|---|
| $1/2$ | $1$ | $0.693$ |
| $1/4$ | $2$ | $1.386$ |
| $0.9$ | $0.152$ | $0.105$ |
| $0.1$ | $3.322$ | $2.303$ |

$1$ bit $= \ln 2 \approx 0.693$ nats.

## Practical tips

- With a one-hot label, cross-entropy $= -\log q_{\text{correct}}$.
- Minimising cross-entropy = minimising KL = MLE.
- In information gain, weight the children's entropies by their numbers of
  examples.
