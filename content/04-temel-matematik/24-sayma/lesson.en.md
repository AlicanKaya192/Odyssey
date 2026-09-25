# Counting: Permutations and Combinations

"How many different ways are there?" is the foundation of probability: the
probability of an event is often "the number of wanted cases over the number
of all cases". Writing cases out one by one becomes impossible after a few;
in this section we will learn to count them without writing them out.
Counting is everywhere in machine learning too: how many models a
hyperparameter search trains, how many different subsets can be chosen from
$20$ features, how many pair comparisons a dataset needs are all counting
questions. We will see the multiplication principle, factorials,
permutations, combinations and when to use which.

Prerequisites: Natural Numbers and Order of Operations, Exponents, Sets and
Logic.

## The addition principle

If the options come from **separate groups** and you choose only one, the
numbers add. With $3$ desserts and $4$ fruits on the menu, there are
$3 + 4 = 7$ ways to choose a dessert **or** a fruit.

The condition is that the groups share no element. If they do, it is
counted twice; the $n(A \cup B) = n(A) + n(B) - n(A \cap B)$ of Sets and
Logic fixes that.

## The multiplication principle

If a task is done **step by step** and the number of options at each step
does not depend on the earlier ones, the numbers **multiply**. With $2$
shirts and $3$ pairs of trousers you can make $2 \cdot 3 = 6$ different
outfits: each shirt goes with three pairs of trousers.

<figure class="fig">
<svg viewBox="0 0 470 264" width="470"><rect class="box" x="22.0" y="117.0" width="56" height="26" rx="6"/><text class="ink" x="50" y="134" font-size="11" text-anchor="middle">start</text><line class="curve3" x1="78" y1="130" x2="134" y2="70"/><rect class="box" x="134.0" y="57.0" width="72" height="26" rx="6"/><text class="ink" x="170" y="74" font-size="11" text-anchor="middle">shirt 1</text><line class="curve3" x1="206" y1="70" x2="266" y2="30"/><rect class="box" x="266.0" y="17.0" width="68" height="26" rx="6"/><text class="ink" x="300" y="34" font-size="11" text-anchor="middle">jeans</text><line class="curve3" x1="206" y1="70" x2="266" y2="70"/><rect class="box" x="266.0" y="57.0" width="68" height="26" rx="6"/><text class="ink" x="300" y="74" font-size="11" text-anchor="middle">chinos</text><line class="curve3" x1="206" y1="70" x2="266" y2="110"/><rect class="box" x="266.0" y="97.0" width="68" height="26" rx="6"/><text class="ink" x="300" y="114" font-size="11" text-anchor="middle">shorts</text><line class="curve3" x1="78" y1="130" x2="134" y2="190"/><rect class="box" x="134.0" y="177.0" width="72" height="26" rx="6"/><text class="ink" x="170" y="194" font-size="11" text-anchor="middle">shirt 2</text><line class="curve3" x1="206" y1="190" x2="266" y2="150"/><rect class="box" x="266.0" y="137.0" width="68" height="26" rx="6"/><text class="ink" x="300" y="154" font-size="11" text-anchor="middle">jeans</text><line class="curve3" x1="206" y1="190" x2="266" y2="190"/><rect class="box" x="266.0" y="177.0" width="68" height="26" rx="6"/><text class="ink" x="300" y="194" font-size="11" text-anchor="middle">chinos</text><line class="curve3" x1="206" y1="190" x2="266" y2="230"/><rect class="box" x="266.0" y="217.0" width="68" height="26" rx="6"/><text class="ink" x="300" y="234" font-size="11" text-anchor="middle">shorts</text><text class="ink" x="400" y="134" font-size="12" text-anchor="middle">2 · 3 = 6 outfits</text></svg>
  <figcaption>A choice tree: 2 branches at the first step and 3 more at the end of each. The leaves are all the outfits; there are 2 · 3 = 6.</figcaption>
</figure>

- A $4$ digit PIN: $10$ options per digit, $10^4 = 10{,}000$ codes.
- A $10$ question test with $4$ options each: $4^{10} = 1{,}048{,}576$
  different answer sheets.
- $3$ learning rates, $4$ tree depths and $5$ tree counts:
  $3 \cdot 4 \cdot 5 = 60$ different settings.

**Ordered choice with repetition.** Choosing $k$ times from $n$ options,
with all options open every time, gives $n^k$.

## Factorials

In how many different orders can $n$ different objects be arranged? The
first place has $n$ options, the second $n - 1$, … the last $1$:

$$
n! = n \cdot (n - 1) \cdot (n - 2) \cdots 2 \cdot 1
$$

Read "$n$ factorial". $3! = 6$, $5! = 120$, $10! = 3{,}628{,}800$.
Factorials grow even faster than exponentials: the number of orderings of a
$52$ card deck is $52!$, about $8 \cdot 10^{67}$.

**$0! = 1$.** There is exactly one way to arrange no objects: do nothing.
This definition is also needed for the formulas to work consistently.

## Permutations: order matters

Choosing $k$ of $n$ objects **in order** (arranging them). By the
multiplication principle this is $n \cdot (n - 1) \cdots (n - k + 1)$,
which is $n!$ with its last $n - k$ factors dropped:

$$
P(n, k) = \frac{n!}{(n - k)!}
$$

In how many ways can the first, second and third places go among $8$
runners? $P(8, 3) = 8 \cdot 7 \cdot 6 = 336$.

**Repeated objects.** If some objects are identical, swapping them among
themselves gives no new arrangement, so we divide. The letters of "KAYAK":
$5$ letters, two K's and two A's:

$$
\frac{5!}{2! \cdot 2!} = \frac{120}{4} = 30
$$

## Combinations: order does not matter

Choosing $k$ of $n$ objects **without order** (forming a group). Each
group can be arranged in $k!$ different orders; a permutation count counts
each group $k!$ times. So:

$$
C(n, k) = \binom{n}{k} = \frac{n!}{k! \, (n - k)!}
$$

<figure class="fig">
<svg viewBox="0 0 440 186" width="440"><text class="ink" x="110" y="22" font-size="12" text-anchor="middle">order matters: 3 · 2 = 6</text><text class="dim" x="110" y="40" font-size="11" text-anchor="middle">president–deputy</text><text class="ink" x="330" y="22" font-size="12" text-anchor="middle">order does not matter: 6 / 2 = 3</text><text class="dim" x="330" y="40" font-size="11" text-anchor="middle">a team of two</text><rect class="box" x="56.0" y="59.0" width="48" height="26" rx="6"/><text class="ink" x="80" y="76" font-size="11" text-anchor="middle">AB</text><rect class="box" x="116.0" y="59.0" width="48" height="26" rx="6"/><text class="ink" x="140" y="76" font-size="11" text-anchor="middle">BA</text><line class="curve2" x1="172" y1="72" x2="282" y2="72" stroke-dasharray="5 4"/><rect class="box" x="295.0" y="59.0" width="70" height="26" rx="6"/><text class="ink" x="330" y="76" font-size="11" text-anchor="middle">{A, B}</text><rect class="box" x="56.0" y="101.0" width="48" height="26" rx="6"/><text class="ink" x="80" y="118" font-size="11" text-anchor="middle">AC</text><rect class="box" x="116.0" y="101.0" width="48" height="26" rx="6"/><text class="ink" x="140" y="118" font-size="11" text-anchor="middle">CA</text><line class="curve2" x1="172" y1="114" x2="282" y2="114" stroke-dasharray="5 4"/><rect class="box" x="295.0" y="101.0" width="70" height="26" rx="6"/><text class="ink" x="330" y="118" font-size="11" text-anchor="middle">{A, C}</text><rect class="box" x="56.0" y="143.0" width="48" height="26" rx="6"/><text class="ink" x="80" y="160" font-size="11" text-anchor="middle">BC</text><rect class="box" x="116.0" y="143.0" width="48" height="26" rx="6"/><text class="ink" x="140" y="160" font-size="11" text-anchor="middle">CB</text><line class="curve2" x1="172" y1="156" x2="282" y2="156" stroke-dasharray="5 4"/><rect class="box" x="295.0" y="143.0" width="70" height="26" rx="6"/><text class="ink" x="330" y="160" font-size="11" text-anchor="middle">{B, C}</text></svg>
  <figcaption>Two people from A, B, C. If a president and a deputy are chosen, AB and BA differ: 6 ways. In a team of two both orders are the same team: each pair counts once, 6 / 2! = 3 ways.</figcaption>
</figure>

A committee of $3$ from $10$ people: $\binom{10}{3} = \frac{10 \cdot 9
\cdot 8}{3 \cdot 2 \cdot 1} = 120$. If a chair, a deputy and a secretary
were chosen it would be $P(10, 3) = 720 = 120 \cdot 3!$.

**Symmetry.** Choosing $k$ people is the same as choosing the $n - k$ who
stay behind: $\binom{n}{k} = \binom{n}{n - k}$.
$\binom{10}{7} = \binom{10}{3} = 120$.

**Pascal's triangle.** Arranged in a triangle, each $\binom{n}{k}$ is the
sum of the two numbers above it:
$\binom{n}{k} = \binom{n - 1}{k - 1} + \binom{n - 1}{k}$. The reason: a
particular person is either in the group (the other $k - 1$ come from
$n - 1$ people) or not (all $k$ come from $n - 1$ people).

<figure class="fig">
<svg viewBox="0 0 440 270" width="440"><circle class="box" cx="220.0" cy="26" r="14"/><text class="ink" x="220.0" y="30" font-size="11" text-anchor="middle">1</text><circle class="box" cx="202.0" cy="58" r="14"/><text class="ink" x="202.0" y="62" font-size="11" text-anchor="middle">1</text><circle class="box" cx="238.0" cy="58" r="14"/><text class="ink" x="238.0" y="62" font-size="11" text-anchor="middle">1</text><circle class="box" cx="184.0" cy="90" r="14"/><text class="ink" x="184.0" y="94" font-size="11" text-anchor="middle">1</text><circle class="box" cx="220.0" cy="90" r="14"/><text class="ink" x="220.0" y="94" font-size="11" text-anchor="middle">2</text><circle class="box" cx="256.0" cy="90" r="14"/><text class="ink" x="256.0" y="94" font-size="11" text-anchor="middle">1</text><circle class="box" cx="166.0" cy="122" r="14"/><text class="ink" x="166.0" y="126" font-size="11" text-anchor="middle">1</text><circle class="dot2" opacity="0.55" cx="202.0" cy="122" r="14"/><text class="ink" x="202.0" y="126" font-size="11" text-anchor="middle">3</text><circle class="dot2" opacity="0.55" cx="238.0" cy="122" r="14"/><text class="ink" x="238.0" y="126" font-size="11" text-anchor="middle">3</text><circle class="box" cx="274.0" cy="122" r="14"/><text class="ink" x="274.0" y="126" font-size="11" text-anchor="middle">1</text><circle class="box" cx="148.0" cy="154" r="14"/><text class="ink" x="148.0" y="158" font-size="11" text-anchor="middle">1</text><circle class="box" cx="184.0" cy="154" r="14"/><text class="ink" x="184.0" y="158" font-size="11" text-anchor="middle">4</text><circle class="dot3" opacity="0.55" cx="220.0" cy="154" r="14"/><text class="ink" x="220.0" y="158" font-size="11" text-anchor="middle">6</text><circle class="box" cx="256.0" cy="154" r="14"/><text class="ink" x="256.0" y="158" font-size="11" text-anchor="middle">4</text><circle class="box" cx="292.0" cy="154" r="14"/><text class="ink" x="292.0" y="158" font-size="11" text-anchor="middle">1</text><circle class="box" cx="130.0" cy="186" r="14"/><text class="ink" x="130.0" y="190" font-size="11" text-anchor="middle">1</text><circle class="box" cx="166.0" cy="186" r="14"/><text class="ink" x="166.0" y="190" font-size="11" text-anchor="middle">5</text><circle class="box" cx="202.0" cy="186" r="14"/><text class="ink" x="202.0" y="190" font-size="11" text-anchor="middle">10</text><circle class="box" cx="238.0" cy="186" r="14"/><text class="ink" x="238.0" y="190" font-size="11" text-anchor="middle">10</text><circle class="box" cx="274.0" cy="186" r="14"/><text class="ink" x="274.0" y="190" font-size="11" text-anchor="middle">5</text><circle class="box" cx="310.0" cy="186" r="14"/><text class="ink" x="310.0" y="190" font-size="11" text-anchor="middle">1</text><circle class="box" cx="112.0" cy="218" r="14"/><text class="ink" x="112.0" y="222" font-size="11" text-anchor="middle">1</text><circle class="box" cx="148.0" cy="218" r="14"/><text class="ink" x="148.0" y="222" font-size="11" text-anchor="middle">6</text><circle class="box" cx="184.0" cy="218" r="14"/><text class="ink" x="184.0" y="222" font-size="11" text-anchor="middle">15</text><circle class="box" cx="220.0" cy="218" r="14"/><text class="ink" x="220.0" y="222" font-size="11" text-anchor="middle">20</text><circle class="box" cx="256.0" cy="218" r="14"/><text class="ink" x="256.0" y="222" font-size="11" text-anchor="middle">15</text><circle class="box" cx="292.0" cy="218" r="14"/><text class="ink" x="292.0" y="222" font-size="11" text-anchor="middle">6</text><circle class="box" cx="328.0" cy="218" r="14"/><text class="ink" x="328.0" y="222" font-size="11" text-anchor="middle">1</text><text class="dim" x="22" y="30" font-size="10" text-anchor="start">n = 0</text><text class="dim" x="22" y="62" font-size="10" text-anchor="start">n = 1</text><text class="dim" x="22" y="94" font-size="10" text-anchor="start">n = 2</text><text class="dim" x="22" y="126" font-size="10" text-anchor="start">n = 3</text><text class="dim" x="22" y="158" font-size="10" text-anchor="start">n = 4</text><text class="dim" x="22" y="190" font-size="10" text-anchor="start">n = 5</text><text class="dim" x="22" y="222" font-size="10" text-anchor="start">n = 6</text><text class="ink" x="220" y="256" font-size="11" text-anchor="middle">each number is the sum of the two above it; row 4, position 2 is C(4, 2) = 6</text></svg>
  <figcaption>The first seven rows of Pascal's triangle. The green 6 is the sum of the two orange 3's above it. The numbers in row n are C(n, 0), C(n, 1), …, C(n, n); they add up to 2ⁿ.</figcaption>
</figure>

**The number of subsets.** A set with $n$ elements has $2^n$ subsets: for
each element there are two options, "take" or "leave". That is why a row of
Pascal's triangle adds up to $2^n$.

## Which formula?

Ask four questions in turn: how many objects to choose from ($n$), how many
are chosen ($k$), **does order matter**, **can the same object be chosen
again**?

| Order matters? | Repetition? | Count | Example |
|---|---|---|---|
| yes | yes | $n^k$ | a PIN |
| yes | no | $P(n, k) = \dfrac{n!}{(n - k)!}$ | the top three in a race |
| no | no | $\binom{n}{k}$ | a committee |
| no | yes | $\binom{n + k - 1}{k}$ | $5$ scoops from $3$ flavours |

The last row is the less common case: choosing $5$ scoops from $3$ flavours
with repetition allowed gives $\binom{7}{5} = 21$ ways.

**The order test:** swap the chosen items. If the result changes (first and
second place swapped) order matters; if it does not (the team is the same
team) it does not.

## A bridge to probability

If all outcomes are equally likely:

$$
P(\text{event}) = \frac{\text{number of outcomes in the event}}{\text{number of all outcomes}}
$$

A bag has $3$ red and $2$ blue balls; $2$ balls are drawn at random. The
probability that both are red is $\frac{\binom{3}{2}}{\binom{5}{2}} =
\frac{3}{10}$. In a $6$-from-$49$ lottery the jackpot probability is
$\frac{1}{\binom{49}{6}} = \frac{1}{13{,}983{,}816}$. The next section,
Introduction to Probability, starts from this bridge.

## Counting in machine learning

**Grid search.** Trying every combination of hyperparameters is the
multiplication principle: $3 \cdot 4 \cdot 5 = 60$ settings. With $5$-fold
cross-validation each setting is trained $5$ times: $300$ trainings. Each
new hyperparameter multiplies the count; that is why random search is
preferred for large searches.

**Feature selection.** Finding the best subset of $20$ features by trying
them all means $2^{20} \approx 10^6$ models; with $50$ features
$2^{50} \approx 10^{15}$, impossible. That is why greedy methods that add
or remove one feature at a time exist.

**Pair comparisons.** Comparing each of $n$ examples with every other takes
$\binom{n}{2} = \frac{n(n - 1)}{2}$ comparisons. For $1000$ examples
$499{,}500$; when the number of examples doubles, the work quadruples.

**Shuffling.** The data is reshuffled every epoch; $1000$ examples have
$1000!$ different orders, so the chance of two epochs seeing the same order
is practically zero.

## Common mistakes

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Wrong</h4>
      <p>$P(10, 3) = 720$ for a committee</p>
      <p>$0! = 0$</p>
      <p>$5! = 120$ for "KAYAK"</p>
      <p>$\binom{n}{k} = \dfrac{n!}{k!}$</p>
    </div>
    <div class="ok">
      <h4>Right</h4>
      <p>order does not matter: $\binom{10}{3} = 120$</p>
      <p>$0! = 1$</p>
      <p>divide for repeated letters: $30$</p>
      <p>$\dfrac{n!}{k! \, (n - k)!}$</p>
    </div>
  </div>
  <figcaption>First decide whether order matters; if there are identical objects, divide by the rearrangements among them.</figcaption>
</figure>

- **Mixing up adding and multiplying.** "This or that" adds, "first this,
  then that" multiplies.
- **Counting the same case twice.** Draw a tree and count a small example
  by hand; compare with what the formula gives.

## Summary

- One from separate groups: add. Step by step: multiply.
- $n! = n \cdot (n - 1) \cdots 1$, $0! = 1$.
- Ordered choice $P(n, k) = \frac{n!}{(n - k)!}$; ordered with repetition
  $n^k$.
- Unordered choice $\binom{n}{k} = \frac{n!}{k!(n - k)!}$;
  $P(n, k) = \binom{n}{k} \cdot k!$.
- $\binom{n}{k} = \binom{n}{n - k}$; Pascal's triangle; a set with $n$
  elements has $2^n$ subsets.
- With identical objects, divide by their arrangements among themselves.
- Probability = matching / all; grid search, feature selection and pair
  comparisons are counting questions.
