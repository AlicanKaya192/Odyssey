The short version of everything in the lesson. Come back here when you get stuck on a question.

## Set notation

| Notation | Meaning |
|---|---|
| $x \in A$ / $x \notin A$ | element / not an element |
| $\emptyset$ | the empty set |
| $n(A)$ | number of elements |
| $A \subseteq B$ | subset |
| $A \cup B$ | union (or) |
| $A \cap B$ | intersection (and) |
| $A \setminus B$ | difference |
| $A'$ | complement |

## Counting rules

$$
n(A \cup B) = n(A) + n(B) - n(A \cap B)
$$

$$
n(A') = n(U) - n(A), \qquad n(A \setminus B) = n(A) - n(A \cap B)
$$

A set with $n$ elements has $2^n$ subsets ($\emptyset$ and itself included).

## Truth table

| $p$ | $q$ | $p \wedge q$ | $p \vee q$ | $p \Rightarrow q$ |
|---|---|---|---|---|
| $1$ | $1$ | $1$ | $1$ | $1$ |
| $1$ | $0$ | $0$ | $1$ | $0$ |
| $0$ | $1$ | $0$ | $1$ | $1$ |
| $0$ | $0$ | $0$ | $0$ | $1$ |

## De Morgan

| Logic | Sets |
|---|---|
| $\neg(p \wedge q) = \neg p \vee \neg q$ | $(A \cap B)' = A' \cup B'$ |
| $\neg(p \vee q) = \neg p \wedge \neg q$ | $(A \cup B)' = A' \cap B'$ |

## Practical tips

- Fill a Venn diagram **from the inside out**: first the intersection, then the "only" regions, last "neither".
- "At least one" is the union, "both" the intersection, "neither" the complement of the union.
- $p \Rightarrow q$ is equivalent to $\neg q \Rightarrow \neg p$ (the contrapositive); the converse ($q \Rightarrow p$) is not.
- In pandas use `&`, `|`, `~`; put every condition in brackets.
