A short version of everything in the lesson. Come back here when you get stuck on a question.

## Concepts

| Concept | Meaning | Die example |
|---|---|---|
| sample space $S$ | all outcomes | $\{1, \dots, 6\}$ |
| event | a subset of $S$ | even: $\{2, 4, 6\}$ |
| complement $A'$ | not $A$ | odd: $\{1, 3, 5\}$ |
| disjoint | cannot happen together, $A \cap B = \varnothing$ | "1" and "6" |
| independent | one does not affect the other | two separate dice |

## Rules

| Rule | Formula |
|---|---|
| equally likely outcomes | $P(A) = \dfrac{n(A)}{n(S)}$ |
| bounds | $0 \leq P(A) \leq 1$, $P(S) = 1$ |
| complement | $P(A') = 1 - P(A)$ |
| union | $P(A \cup B) = P(A) + P(B) - P(A \cap B)$ |
| disjoint union | $P(A \cup B) = P(A) + P(B)$ |
| independent intersection | $P(A \cap B) = P(A) \, P(B)$ |
| conditional | $P(B \mid A) = \dfrac{P(A \cap B)}{P(A)}$ |

## Trees

- Each branch carries the probability of that step; second branches are
  conditional probabilities.
- **Multiply** along a path, **add** the paths that make up the event.
- All paths add up to $1$.
- Without replacement the second step's probabilities change; with
  replacement they do not.

## Practical tips

- When you see "at least one", look at the complement:
  $1 - P(\text{none})$.
- "Or" means union, "and" means intersection.
- Ask about independence before multiplying.
- $P(B \mid A)$ and $P(A \mid B)$ differ: which group does the denominator
  count?
- Make sure the outcomes really are equally likely.
