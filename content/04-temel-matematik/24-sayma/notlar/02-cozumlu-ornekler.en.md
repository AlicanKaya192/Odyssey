A worked example for each method in the lesson, step by step. Try each question yourself first, then read the solution.

## 1. Add or multiply?

**Question:** A shelf has $5$ novels and $3$ poetry books. How many ways
are there to choose one book? To choose a novel **and** a poetry book?

One: $5 + 3 = 8$. Both, step by step: $5 \cdot 3 = 15$.

## 2. A password

**Question:** How many passwords consist of $2$ capital letters (a $26$
letter alphabet) followed by $3$ digits?

Each place is independent and repetition is allowed:
$26 \cdot 26 \cdot 10 \cdot 10 \cdot 10 = 676{,}000$.

## 3. Simplifying factorials

**Question:** What is $\dfrac{6!}{4!}$?

$\frac{6 \cdot 5 \cdot 4!}{4!} = 30$. There is no need to expand the
factorials all the way.

## 4. A permutation

**Question:** In how many ways can $3$ of $7$ books be arranged side by side
on a shelf?

Order matters: $P(7, 3) = 7 \cdot 6 \cdot 5 = 210$.

## 5. Identical letters

**Question:** How many different arrangements can be written with the
letters of "ANANAS"?

$6$ letters; A three times, N twice: $\frac{6!}{3! \cdot 2!} =
\frac{720}{12} = 60$.

## 6. A combination

**Question:** In how many ways can a project team of $4$ be chosen from a
class of $12$?

Order does not matter: $\binom{12}{4} = \frac{12 \cdot 11 \cdot 10 \cdot
9}{4 \cdot 3 \cdot 2 \cdot 1} = 495$.

## 7. A choice with conditions

**Question:** In how many ways can a team of $2$ men and $2$ women be formed
from $6$ men and $4$ women?

Men $\binom{6}{2} = 15$, women $\binom{4}{2} = 6$; two steps, multiply:
$90$.

## 8. At least one

**Question:** How many different subgroups with at least one person can be
chosen from a group of $5$?

All subsets $2^5 = 32$; without the empty set, $31$.

## 9. Probability

**Question:** A bag has $4$ red and $6$ blue balls; $3$ balls are drawn.
What is the probability of exactly $2$ red?

Matching: $\binom{4}{2} \cdot \binom{6}{1} = 6 \cdot 6 = 36$. All:
$\binom{10}{3} = 120$. $P = \frac{36}{120} = 0.3$.

## 10. Grid search

**Question:** $4$ learning rates, $3$ layer counts and $2$ activation
functions are tried with $5$-fold cross-validation. How many trainings are
done?

$4 \cdot 3 \cdot 2 = 24$ settings, each $5$ times: $120$ trainings.
