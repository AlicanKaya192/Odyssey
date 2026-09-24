# Sets and Logic

Two basic languages of mathematics: **sets** describe grouping objects, and
**logic** describes reasoning with true–false sentences. Filtering the
rows of a data set, making sure training and test data do not overlap, or
measuring how accurate a model is are all done in these two languages.
Every filter you write in pandas with `&`, `|` and `~` is one of the
operations in this section.

Prerequisite: Reading Mathematics.

## Sets and elements

A **set** is a collection of well-defined objects. Its elements are written
in curly brackets; order and repetition do not matter:

$$
A = \{1, 2, 3\} = \{3, 1, 2\} = \{1, 1, 2, 3\}
$$

| Notation | Meaning | Example |
|---|---|---|
| $x \in A$ | $x$ is an element of $A$ | $2 \in \{1, 2, 3\}$ |
| $x \notin A$ | $x$ is not an element of $A$ | $5 \notin \{1, 2, 3\}$ |
| $\emptyset$ | the empty set | $\{\}$ |
| $n(A)$ or $\lvert A \rvert$ | the number of elements | $n(\{1, 2, 3\}) = 3$ |
| $A \subseteq B$ | every element of $A$ is in $B$ | $\{1, 2\} \subseteq \{1, 2, 3\}$ |

Sets can also be written with a **rule**: $\{x \mid x \text{ even and } 0
< x < 10\} = \{2, 4, 6, 8\}$. The sign "$\mid$" is read "such that".

### Number sets

<figure class="fig">
<svg viewBox="0 0 480 260" width="480"><ellipse class="curve3" cx="240" cy="130" rx="215" ry="115"/><text class="ink" x="240" y="31" font-size="12" text-anchor="middle">ℝ real</text><ellipse class="dot2" opacity="0.18" cx="240" cy="130" rx="160" ry="88"/><ellipse class="curve2" cx="240" cy="130" rx="160" ry="88"/><text class="ink" x="240" y="58" font-size="12" text-anchor="middle">ℚ rational</text><ellipse class="dot" opacity="0.18" cx="240" cy="130" rx="108" ry="62"/><ellipse class="curve" cx="240" cy="130" rx="108" ry="62"/><text class="ink" x="240" y="84" font-size="12" text-anchor="middle">ℤ integers</text><ellipse class="dot3" opacity="0.18" cx="240" cy="130" rx="58" ry="36"/><ellipse class="curve4" cx="240" cy="130" rx="58" ry="36"/><text class="ink" x="240" y="110" font-size="12" text-anchor="middle">ℕ natural</text><text class="ink" x="226" y="140" font-size="13" text-anchor="middle">0</text><text class="ink" x="254" y="140" font-size="13" text-anchor="middle">5</text><text class="ink" x="320" y="136" font-size="13" text-anchor="middle">−3</text><text class="ink" x="108" y="136" font-size="13" text-anchor="middle">1/2</text><text class="ink" x="372" y="136" font-size="13" text-anchor="middle">0.75</text><text class="ink" x="52" y="136" font-size="13" text-anchor="middle">√2</text><text class="ink" x="428" y="136" font-size="13" text-anchor="middle">π</text></svg>
  <figcaption>The numbers so far are nested sets: every natural number is an integer, every integer is a rational number (a fraction), every rational number is a real number. $\sqrt{2}$ and $\pi$ are real but not rational.</figcaption>
</figure>

$$
\mathbb{N} \subset \mathbb{Z} \subset \mathbb{Q} \subset \mathbb{R}
$$

## Set operations

<figure class="fig">
<svg viewBox="0 0 460 262" width="460"><rect class="box" x="20" y="20" width="420" height="230" rx="8"/><text class="dim" x="36" y="42" font-size="11" text-anchor="start">U: 30 students</text><circle class="dot" opacity="0.25" cx="180" cy="140" r="85"/><circle class="dot2" opacity="0.25" cx="280" cy="140" r="85"/><circle class="curve" cx="180" cy="140" r="85"/><circle class="curve2" cx="280" cy="140" r="85"/><text class="ink" x="160" y="47" font-size="12" text-anchor="middle">Python (18)</text><text class="ink" x="300" y="47" font-size="12" text-anchor="middle">SQL (12)</text><text class="ink" x="140" y="144" font-size="20" text-anchor="middle">11</text><text class="dim" x="140" y="162" font-size="10" text-anchor="middle">Python only</text><text class="ink" x="230.0" y="144" font-size="20" text-anchor="middle">7</text><text class="dim" x="230.0" y="162" font-size="10" text-anchor="middle">both</text><text class="ink" x="320" y="144" font-size="20" text-anchor="middle">5</text><text class="dim" x="320" y="162" font-size="10" text-anchor="middle">SQL only</text><text class="ink" x="400" y="230" font-size="18" text-anchor="middle">7</text><text class="dim" x="400" y="244" font-size="10" text-anchor="middle">neither</text></svg>
  <figcaption>Of $30$ students, $18$ know Python, $12$ know SQL and $7$ know both. The Venn diagram has four regions: Python only ($11$), both ($7$), SQL only ($5$) and neither ($7$). The total is $11 + 7 + 5 + 7 = 30$.</figcaption>
</figure>

| Operation | Notation | Meaning |
|---|---|---|
| Union | $A \cup B$ | in $A$ **or** in $B$ (or both) |
| Intersection | $A \cap B$ | in **both** $A$ and $B$ |
| Difference | $A \setminus B$ | in $A$ but not in $B$ |
| Complement | $A'$ | in the universal set but not in $A$ |

For $A = \{1, 2, 3, 4\}$, $B = \{3, 4, 5\}$:

$$
A \cup B = \{1, 2, 3, 4, 5\}, \quad A \cap B = \{3, 4\}, \quad A \setminus B = \{1, 2\}
$$

Sets with an empty intersection are called **disjoint**: $A \cap B =
\emptyset$.

### The size of a union

When adding up the elements of two sets, the common elements are counted
**twice**; they must be subtracted once:

$$
n(A \cup B) = n(A) + n(B) - n(A \cap B)
$$

In the example in the figure: $18 + 12 - 7 = 23$ students know at least one,
and $30 - 23 = 7$ know neither.

## Logic: statements

A **statement** is a sentence that is either true or false. "$3 > 2$" is
true, "$2 + 2 = 5$" is false. Sentences that depend on who says them, such
as "this question is hard", are not statements.

Statements combine with connectives. Let $p$ and $q$ be two statements
($1$ true, $0$ false):

| $p$ | $q$ | $p \wedge q$ (and) | $p \vee q$ (or) | $\neg p$ (not) | $p \Rightarrow q$ (if–then) |
|---|---|---|---|---|---|
| $1$ | $1$ | $1$ | $1$ | $0$ | $1$ |
| $1$ | $0$ | $0$ | $1$ | $0$ | $0$ |
| $0$ | $1$ | $0$ | $1$ | $1$ | $1$ |
| $0$ | $0$ | $0$ | $0$ | $1$ | $1$ |

- **and** ($\wedge$): true if both are true.
- **or** ($\vee$): true if at least one is true. In mathematics "or" is
  **inclusive**: it is true when both are true as well.
- **if–then** ($\Rightarrow$): false only when the premise is true and the
  conclusion false. "If it rains, the ground gets wet" is not broken on a
  day when it does not rain.

**The converse is not the same.** $p \Rightarrow q$ can be true while $q
\Rightarrow p$ is false: "if a number is divisible by $4$, it is even" is
true; "if a number is even, it is divisible by $4$" is false ($6$).

## Sets and logic are one language

| Logic | Sets |
|---|---|
| and ($\wedge$) | intersection ($\cap$) |
| or ($\vee$) | union ($\cup$) |
| not ($\neg$) | complement ($'$) |
| if–then ($\Rightarrow$) | subset ($\subseteq$) |

**De Morgan's laws:** the negation of "and" is the "or" of the negations:

$$
\neg(p \wedge q) = \neg p \vee \neg q, \qquad (A \cap B)' = A' \cup B'
$$

$$
\neg(p \vee q) = \neg p \wedge \neg q, \qquad (A \cup B)' = A' \cap B'
$$

The negation of "knows both Python and SQL" is "does not know Python **or**
does not know SQL"; not "knows neither".

## Sets and logic in machine learning

**Filtering data.** In pandas, `df[(df["age"] > 30) & (df["city"] == "Ankara")]`
takes the intersection of two conditions, `|` the union, `~` the complement.
The brackets are essential: `&` is applied before the comparisons.

**Training and test must be disjoint.** If the intersection of the training
set and the test set is not empty, the model has seen the questions before
the exam; the measured success does not reflect reality. This is called
**data leakage**.

**Measures of accuracy.** If $P$ is the set the model calls spam and $S$
the set that really is spam:

$$
\text{precision} = \frac{n(P \cap S)}{n(P)}, \qquad \text{recall} = \frac{n(P \cap S)}{n(S)}
$$

Precision answers "how much of what I called spam really is spam?"; recall
answers "how much of the real spam did I catch?".

## Common mistakes

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Wrong</h4>
      <p>$n(A \cup B) = n(A) + n(B)$</p>
      <p>$\neg(p \wedge q) = \neg p \wedge \neg q$</p>
      <p>$p \Rightarrow q$ so $q \Rightarrow p$</p>
      <p>"or" = one but not both</p>
    </div>
    <div class="ok">
      <h4>Right</h4>
      <p>$n(A) + n(B) - n(A \cap B)$</p>
      <p>$\neg p \vee \neg q$</p>
      <p>The converse must be proved separately</p>
      <p>"or" includes both</p>
    </div>
  </div>
  <figcaption>The intersection gets counted twice; "not" turns "and" into "or" as it moves inside.</figcaption>
</figure>

- **Counting repeated elements.** $\{1, 1, 2\}$ has $2$ elements.
- **Mixing up $\in$ and $\subseteq$.** $2 \in \{1, 2\}$ but $\{2\} \subseteq
  \{1, 2\}$; an element and a set are different things.

## Summary

- A set: a collection where order and repetition do not matter; $\in$, $\notin$, $\emptyset$, $\subseteq$.
- $\mathbb{N} \subset \mathbb{Z} \subset \mathbb{Q} \subset \mathbb{R}$.
- Union is "or", intersection "and", difference "but not", complement "not".
- $n(A \cup B) = n(A) + n(B) - n(A \cap B)$.
- A statement is true or false; $\wedge$, $\vee$, $\neg$, $\Rightarrow$ are defined by truth tables.
- $p \Rightarrow q$ is false only when $p$ is true and $q$ false; its converse is a separate statement.
- De Morgan: $\neg(p \wedge q) = \neg p \vee \neg q$, $(A \cup B)' = A' \cap B'$.
- Data filters, data leakage and precision–recall are written in the language of sets.
