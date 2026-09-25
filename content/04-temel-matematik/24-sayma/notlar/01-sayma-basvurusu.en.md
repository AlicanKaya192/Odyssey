A short version of everything in the lesson. Come back here when you get stuck on a question.

## Two principles

| Principle | When | Operation |
|---|---|---|
| addition | **one** from separate groups ("this or that") | add |
| multiplication | choosing **step by step** ("first this, then that") | multiply |

## Formulas

| Name | Formula | Meaning |
|---|---|---|
| factorial | $n! = n(n - 1) \cdots 1$, $0! = 1$ | arrangements of $n$ objects |
| permutation | $P(n, k) = \dfrac{n!}{(n - k)!}$ | choosing $k$ in order |
| combination | $\binom{n}{k} = \dfrac{n!}{k!(n - k)!}$ | choosing $k$ without order |
| ordered with repetition | $n^k$ | PIN, password |
| unordered with repetition | $\binom{n + k - 1}{k}$ | several of the same kind |
| arrangements with identical objects | $\dfrac{n!}{a! \, b! \cdots}$ | "KAYAK": $\frac{5!}{2!2!}$ |

$P(n, k) = \binom{n}{k} \cdot k!$

## Properties of combinations

- $\binom{n}{0} = \binom{n}{n} = 1$, $\binom{n}{1} = n$
- $\binom{n}{k} = \binom{n}{n - k}$
- Pascal: $\binom{n}{k} = \binom{n - 1}{k - 1} + \binom{n - 1}{k}$
- $\binom{n}{0} + \binom{n}{1} + \dots + \binom{n}{n} = 2^n$
- $\binom{n}{2} = \frac{n(n - 1)}{2}$: the number of pairs

## Which formula?

1. Does order matter? Swap the chosen items; if the result changes, yes.
2. Is repetition allowed? Can the same object be chosen twice?
3. Are there identical objects? If so, divide by their arrangements among
   themselves.

## Probability

With equally likely outcomes, $P = \dfrac{\text{matching outcomes}}{\text{all outcomes}}$.

## Practical tips

- For "at least one", use the complement: subtract "none" from all.
- For groups with conditions (2 men, 2 women), choose each group
  separately, then multiply.
- If unsure, count a small example by hand and compare with the formula.
