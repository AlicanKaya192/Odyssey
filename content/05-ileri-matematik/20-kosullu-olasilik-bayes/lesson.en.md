# Conditional Probability and Bayes

When new information arrives, how much we believe something should change:
a positive test makes illness more likely, the word "free" in an e-mail
makes spam more likely. The rule that says by how much is **Bayes' rule**.
Intuition often goes wrong here: when a test that is $99$ percent accurate
comes back positive, the probability of being ill is not $99$ percent; it
is usually much lower. In this section we will see conditional
probability, the law of total probability, Bayes' rule, sequential
updating and the Naive Bayes classifier.

Prerequisites: Introduction to Probability and Counting in MATH 1.

## Conditional probability and the product rule

"The probability of $B$ given that $A$ happened" shrinks the sample space
to $A$:

$$
P(B \mid A) = \frac{P(A \cap B)}{P(A)}
$$

Read the other way round, the same equality is the **product rule**: the
probability that two events happen together is the probability of one
times the probability of the other given the first.

$$
P(A \cap B) = P(A) \, P(B \mid A) = P(B) \, P(A \mid B)
$$

Multiplying along a branch of a probability tree is exactly this. If $A$
and $B$ are independent, $P(B \mid A) = P(B)$ and the rule becomes
$P(A)P(B)$.

## The law of total probability

If the sample space is split into pieces that exclude each other and cover
everything ($A_1, A_2, \dots$), an event's probability is the sum of its
shares in the pieces:

$$
P(B) = \sum_{i} P(B \mid A_i) \, P(A_i)
$$

**Example.** In a factory, machine A makes $50$ percent of the products,
B $30$ percent and C $20$ percent. Their defect rates are $2$, $3$ and $5$
percent. The probability that a random product is defective:

$$
0.5 \cdot 0.02 + 0.3 \cdot 0.03 + 0.2 \cdot 0.05 = 0.01 + 0.009 + 0.01 = 0.029
$$

## Bayes' rule

Setting the two forms of the product rule equal and solving for
$P(A \mid B)$:

$$
P(A \mid B) = \frac{P(B \mid A) \, P(A)}{P(B)}
$$

The names of the parts describe how a belief is updated:

| Part | Name | Meaning |
|---|---|---|
| $P(A)$ | prior | the belief before the evidence |
| $P(B \mid A)$ | likelihood | the probability of seeing this evidence if $A$ is true |
| $P(B)$ | evidence | the total probability of the evidence (by total probability) |
| $P(A \mid B)$ | posterior | the belief after the evidence |

In the factory example a defective product is found; the probability that
it came from machine C is $\frac{0.05 \cdot 0.2}{0.029} = \frac{0.01}{0.029}
\approx 0.345$. C makes only $20$ percent of the products but $34.5$
percent of the defective ones come from it.

## The test paradox

A disease affects $1$ percent of the population. The test is positive for
$99$ percent of the ill (sensitivity), and wrongly positive for $5$ percent
of the healthy. What is the probability that someone with a positive test
is ill?

Intuition says "$99$ percent". The calculation says otherwise. The easiest
way is to think in natural frequencies: take $10{,}000$ people.

<figure class="fig">
<svg viewBox="0 0 440 236" width="440"><line class="curve3" x1="220" y1="40" x2="110" y2="82"/><line class="curve3" x1="220" y1="40" x2="330" y2="82"/><line class="curve3" x1="110" y1="118" x2="55" y2="158"/><line class="curve3" x1="110" y1="118" x2="165" y2="158"/><line class="curve3" x1="330" y1="118" x2="275" y2="158"/><line class="curve3" x1="330" y1="118" x2="385" y2="158"/><rect class="box" x="165.0" y="12.0" width="110" height="28" rx="6"/><text class="ink" x="220" y="30.0" font-size="11" text-anchor="middle">10,000 people</text><rect class="box" x="65.0" y="82.0" width="90" height="36" rx="6"/><text class="ink" x="110" y="97.0" font-size="11" text-anchor="middle">ill</text><text class="ink" x="110" y="111.0" font-size="11" text-anchor="middle">100</text><rect class="box" x="285.0" y="82.0" width="90" height="36" rx="6"/><text class="ink" x="330" y="97.0" font-size="11" text-anchor="middle">healthy</text><text class="ink" x="330" y="111.0" font-size="11" text-anchor="middle">9900</text><rect class="box" x="12.0" y="158.0" width="86" height="36" rx="6"/><rect class="dot2" opacity="0.35" x="12.0" y="158.0" width="86" height="36" rx="6"/><text class="ink" x="55" y="173.0" font-size="11" text-anchor="middle">test +</text><text class="ink" x="55" y="187.0" font-size="11" text-anchor="middle">99</text><rect class="box" x="122.0" y="158.0" width="86" height="36" rx="6"/><text class="ink" x="165" y="173.0" font-size="11" text-anchor="middle">test −</text><text class="ink" x="165" y="187.0" font-size="11" text-anchor="middle">1</text><rect class="box" x="232.0" y="158.0" width="86" height="36" rx="6"/><rect class="dot2" opacity="0.35" x="232.0" y="158.0" width="86" height="36" rx="6"/><text class="ink" x="275" y="173.0" font-size="11" text-anchor="middle">test +</text><text class="ink" x="275" y="187.0" font-size="11" text-anchor="middle">495</text><rect class="box" x="342.0" y="158.0" width="86" height="36" rx="6"/><text class="ink" x="385" y="173.0" font-size="11" text-anchor="middle">test −</text><text class="ink" x="385" y="187.0" font-size="11" text-anchor="middle">9405</text><text class="ink" x="220" y="222" font-size="12" text-anchor="middle">99 / (99 + 495) = 1/6 of the positives are ill</text></svg>
  <figcaption>Of 10,000 people, 100 are ill and 99 of them test positive. 5 percent of the 9900 healthy, that is 495, test positive too. Of the 594 positives only 99 are ill.</figcaption>
</figure>

$\frac{99}{99 + 495} = \frac{99}{594} = \frac{1}{6} \approx 0.167$ of the
positives are ill. The same calculation with Bayes' rule:

$$
P(I \mid +) = \frac{0.99 \cdot 0.01}{0.99 \cdot 0.01 + 0.05 \cdot 0.99} = \frac{0.0099}{0.0594} \approx 0.167
$$

<figure class="fig">
<svg viewBox="0 0 440 142" width="440"><rect class="dot2" opacity="0.6" x="20" y="40" width="66.7" height="46"/><rect class="dot" opacity="0.45" x="86.7" y="40" width="333.3" height="46"/><text class="dim" x="20" y="30" font-size="11" text-anchor="start">594 positive results</text><text class="ink" x="53.333333333333336" y="104" font-size="11" text-anchor="middle">ill: 99</text><text class="ink" x="253.33333333333331" y="68.0" font-size="12" text-anchor="middle">healthy (false alarm): 495</text><text class="ink" x="220.0" y="130" font-size="12" text-anchor="middle">only 1/6 of the positives are ill</text></svg>
  <figcaption>All the positive results in one bar, to scale: 99 from the ill, 495 from the healthy. Almost every ill person is caught, but the healthy are so many that even a 5 percent false alarm rate produces five times as many positives.</figcaption>
</figure>

**Why?** The disease is rare: false alarms are a small rate applied to a
big crowd, true positives a big rate applied to a small group. Ignoring
the effect of the prior ($1$ percent) is called the **base rate
fallacy**.

## Sequential updating

The posterior of one test becomes the prior of the next. The first test is
positive: $16.7$ percent. If the same person is also positive on an
independent second test:

$$
\frac{0.99 \cdot 0.167}{0.99 \cdot 0.167 + 0.05 \cdot 0.833} \approx 0.798
$$

<figure class="fig">
<svg viewBox="0 0 440 236" width="440"><line class="grid" x1="50.0" y1="210.0" x2="50.0" y2="20.0"/><line class="grid" x1="137.5" y1="210.0" x2="137.5" y2="20.0"/><line class="grid" x1="225.0" y1="210.0" x2="225.0" y2="20.0"/><line class="grid" x1="312.5" y1="210.0" x2="312.5" y2="20.0"/><line class="grid" x1="400.0" y1="210.0" x2="400.0" y2="20.0"/><line class="grid" x1="50.0" y1="210.0" x2="400.0" y2="210.0"/><line class="grid" x1="50.0" y1="162.5" x2="400.0" y2="162.5"/><line class="grid" x1="50.0" y1="115.0" x2="400.0" y2="115.0"/><line class="grid" x1="50.0" y1="67.5" x2="400.0" y2="67.5"/><line class="grid" x1="50.0" y1="20.0" x2="400.0" y2="20.0"/><line class="line" x1="50.0" y1="210.0" x2="400.0" y2="210.0"/><line class="line" x1="50.0" y1="210.0" x2="50.0" y2="20.0"/><text class="dim" x="45.0" y="165.5" font-size="9" text-anchor="end">25</text><text class="dim" x="45.0" y="118.0" font-size="9" text-anchor="end">50</text><text class="dim" x="45.0" y="70.5" font-size="9" text-anchor="end">75</text><text class="dim" x="45.0" y="23.0" font-size="9" text-anchor="end">100</text><rect class="dot" opacity="0.6" x="67.5" y="208.1" width="52.5" height="1.9"/><text class="ink" x="93.8" y="202.1" font-size="11" text-anchor="middle">1</text><text class="dim" x="93.8" y="226" font-size="10" text-anchor="middle">at first</text><rect class="dot" opacity="0.6" x="155.0" y="178.3" width="52.5" height="31.7"/><text class="ink" x="181.2" y="172.3" font-size="11" text-anchor="middle">16.7</text><text class="dim" x="181.2" y="226" font-size="10" text-anchor="middle">1st test +</text><rect class="dot" opacity="0.6" x="242.5" y="58.4" width="52.5" height="151.6"/><text class="ink" x="268.8" y="52.4" font-size="11" text-anchor="middle">79.8</text><text class="dim" x="268.8" y="226" font-size="10" text-anchor="middle">2nd test +</text><rect class="dot" opacity="0.6" x="330.0" y="22.5" width="52.5" height="187.5"/><text class="ink" x="356.2" y="16.5" font-size="11" text-anchor="middle">98.7</text><text class="dim" x="356.2" y="226" font-size="10" text-anchor="middle">3rd test +</text><text class="dim" x="56.0" y="30.0" font-size="10" text-anchor="start">probability of being ill (percent)</text></svg>
  <figcaption>Each positive test uses the posterior of the previous one as its prior: from 1 percent to 16.7, 79.8 and 98.7. A single test says little; as independent evidence builds up, the belief becomes clear fast.</figcaption>
</figure>

**The odds form.** Written as odds, Bayes becomes a multiplication:

$$
\underbrace{\frac{P(I \mid +)}{P(H \mid +)}}_{\text{posterior odds}} = \underbrace{\frac{P(I)}{P(H)}}_{\text{prior odds}} \cdot \underbrace{\frac{P(+ \mid I)}{P(+ \mid H)}}_{\text{likelihood ratio}}
$$

The prior odds are $1 : 99$ and the likelihood ratio
$\frac{0.99}{0.05} = 19.8$. The posterior odds are $19.8 : 99 = 1 : 5$, a
probability of $\frac{1}{6}$. Each new independent piece of evidence
multiplies the odds by $19.8$ once more.

## Conditional independence

Two events can be independent once a third thing is known:
$P(A \cap B \mid C) = P(A \mid C) \, P(B \mid C)$. The words "free" and "win"
often appear together in an e-mail (dependent), but once we know the
e-mail is spam, most of the link between them is explained. Naive Bayes is
built on this assumption.

## Bayes in machine learning

**The Naive Bayes classifier.** For each class it computes "prior times the
likelihoods of the words" and picks the largest. $P(\text{spam}) = 0.3$;
"free" appears in $40$ percent of spam and $5$ percent of non-spam; "win"
in $30$ percent of spam and $2$ percent of the rest. For an e-mail with
both words:

$$
\begin{aligned}
\text{spam} &: 0.3 \cdot 0.4 \cdot 0.3 = 0.036 \\
\text{not spam} &: 0.7 \cdot 0.05 \cdot 0.02 = 0.0007
\end{aligned}
$$

Normalising, $P(\text{spam} \mid \text{words}) = \frac{0.036}{0.0367}
\approx 0.98$. The denominator (the evidence) is the same for both classes,
so it is not needed for the comparison; it is only computed to make the
probabilities add up to $1$.

**Precision is a Bayes question.** How many of the things a model calls
"positive" really are positive? With rare classes (fraud, failures) even a
good model falls into the test paradox: false alarms can outnumber real
catches.

**The prior is an assumption.** Bayesian methods write down the prior
belief about the weights explicitly; regularisation (preferring small
weights) is another name for a prior.

## Common mistakes

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Wrong</h4>
      <p>$P(I \mid +) = P(+ \mid I) = 0.99$</p>
      <p>ignoring the prior</p>
      <p>taking only one branch for $P(B)$</p>
      <p>two tests = twice the probability</p>
    </div>
    <div class="ok">
      <h4>Right</h4>
      <p>$P(I \mid +) \approx 0.167$</p>
      <p>the base rate decides the result</p>
      <p>total probability: the sum of all branches</p>
      <p>the posterior becomes the new prior</p>
    </div>
  </div>
  <figcaption>The direction of the condition matters: "positive if ill" and "ill if positive" are different questions.</figcaption>
</figure>

- **Multiplying evidence that is not independent.** Doing the same test on
  the same person twice may not count as two independent pieces of
  evidence; the error can repeat for the same reason.

## Summary

- $P(B \mid A) = \frac{P(A \cap B)}{P(A)}$; product rule
  $P(A \cap B) = P(A) P(B \mid A)$.
- Total probability: $P(B) = \sum P(B \mid A_i) P(A_i)$.
- Bayes: $P(A \mid B) = \frac{P(B \mid A) P(A)}{P(B)}$; prior, likelihood,
  evidence, posterior.
- For rare events even a positive result can give a low posterior (base
  rate).
- The posterior is the next step's prior; in odds form each piece of
  evidence multiplies by the likelihood ratio.
- Naive Bayes multiplies likelihoods using conditional independence;
  precision is a Bayes question.
