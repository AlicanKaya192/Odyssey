A worked example for each method in the lesson, step by step. Try each question yourself first, then read the solution.

## 1. Information

**Question:** How many bits of information does an outcome of probability
$\frac{1}{16}$ carry?

$-\log_2\frac{1}{16} = 4$ bits.

## 2. The entropy of a die

**Question:** What is the entropy of a fair die?

Six equally likely outcomes: $\log_2 6 \approx 2.585$ bits.

## 3. An outcome of probability zero

**Question:** $P = (0.5, \ 0.5, \ 0)$. What is $H(P)$?

$0 \log 0 = 0$: $H = 1$ bit, like a two-outcome fair coin.

## 4. An unequal distribution

**Question:** $P = (0.7, \ 0.2, \ 0.1)$. What is $H(P)$?

$0.7 \cdot 0.515 + 0.2 \cdot 2.322 + 0.1 \cdot 3.322 \approx 0.360 + 0.464 +
0.332 = 1.157$ bits. With three outcomes it could be at most $1.585$.

## 5. From bits to nats

**Question:** How many nats are $2$ bits?

$2 \cdot \ln 2 \approx 1.386$ nats.

## 6. Cross-entropy

**Question:** $P = (0.5, \ 0.5)$, $Q = (0.8, \ 0.2)$. What is $H(P, Q)$?

$-0.5\log_2 0.8 - 0.5\log_2 0.2 \approx 0.161 + 1.161 = 1.322$ bits.

## 7. KL divergence

**Question:** With the same distributions, what is
$D_{\mathrm{KL}}(P \parallel Q)$?

$H(P, Q) - H(P) = 1.322 - 1 = 0.322$ bits.

## 8. A classification loss

**Question:** In a four-class model the correct class has probability
$0.25$. What is the cross-entropy (in nats)?

$-\ln 0.25 \approx 1.386$ nats: the model has not got beyond guessing; it
is as undecided as the uniform distribution.

## 9. Information gain

**Question:** $4$ positive and $4$ negative examples. Split A: $(4, 0)$ and
$(0, 4)$. Split B: $(2, 2)$ and $(2, 2)$. What are the gains?

Parent $H = 1$. A: the children are pure, entropy $0$; gain $1$ bit. B: the
children are as mixed as the parent; gain $0$.

## 10. Perplexity

**Question:** A language model's cross-entropy per word is $3$ bits. What is
its perplexity?

$2^3 = 8$: at each word the model is as if undecided among $8$ equal
options.
