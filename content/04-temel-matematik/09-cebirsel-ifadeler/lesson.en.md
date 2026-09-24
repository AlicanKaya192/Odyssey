# Algebraic Expressions and Identities

So far we have always calculated with particular numbers. Algebra lets us
put a **letter** in place of a number and write rules that hold "whatever
the number is". A machine learning model is written this way: in $\hat{y}
= wx + b$, $x$ is the input that changes from example to example, and $w$
and $b$ are the numbers the model learns. In this section we will read,
simplify and multiply algebraic expressions, and meet equalities that are
always true: **identities**.

Prerequisite: the Reading Mathematics, Integers and Exponents sections.

## The parts of an expression

$$
3x^2 - 5x + 7
$$

| Part | In this expression |
|---|---|
| **Variable** | $x$: a letter whose value can change |
| **Term** | $3x^2$, $-5x$, $7$: the pieces separated by $+$ and $-$ |
| **Coefficient** | $3$ and $-5$: the number in front of the letter (with its sign) |
| **Constant term** | $7$: the term without a letter |
| **Degree** | $2$: the highest exponent |

A term's sign belongs to it: the coefficient of $-5x$ is $-5$, not $5$.
If there is no number in front of the letter, the coefficient is $1$: $x =
1 \cdot x$, $-x = -1 \cdot x$.

## Evaluating

To find the value of an expression, put the number in place of the letter
**inside brackets**. For $x = -2$:

$$
3x^2 - 5x + 7 = 3(-2)^2 - 5(-2) + 7 = 12 + 10 + 7 = 29
$$

Writing it without brackets ($3 \cdot -2^2$) confuses both the sign and the
exponent.

## Like terms

Terms whose letters and exponents are **exactly the same** are called
**like terms**. Only like terms add; their coefficients add and the letter
part stays as it is:

$$
3x + 5y - x + 2y = (3 - 1)x + (5 + 2)y = 2x + 7y
$$

Why? $3x - x$ means "take one $x$ away from three $x$s": the distributive
property in reverse, $3x - 1x = (3 - 1)x$.

- $2x$ and $2x^2$ are not like terms (different exponents).
- $xy$ and $yx$ are like terms (order does not matter in multiplication).
- $3x + 2y$ does not simplify further; it is **not** $5xy$.

## Distributing: opening brackets

The factor in front of a bracket multiplies **every** term inside:

$$
3(2x - 5) = 6x - 15
$$

**A minus sign is a factor too:** $-(x - 4) = -1 \cdot (x - 4) = -x + 4$.
The sign of every term inside changes.

$$
\begin{aligned}
3(2x - 5) - 2(x - 4) &= 6x - 15 - 2x + 8 \\
&= 4x - 7
\end{aligned}
$$

## Multiplication

**Monomials:** multiply the coefficients and add the exponents of the
same letters.

$$
(3x^2)(4x^3) = 12x^5, \qquad (-2ab)(5a) = -10a^2 b
$$

**Binomial times binomial:** every term multiplies every term of the
other; four products appear.

<figure class="fig">
<svg viewBox="0 0 440 250" width="440"><rect class="dot" opacity="0.35" x="120" y="34" width="120" height="120"/><rect class="curve3" x="120" y="34" width="120" height="120"/><text class="ink" x="180.0" y="99.0" font-size="16" text-anchor="middle">x²</text><rect class="dot2" opacity="0.35" x="240" y="34" width="78" height="120"/><rect class="curve3" x="240" y="34" width="78" height="120"/><text class="ink" x="279.0" y="99.0" font-size="14" text-anchor="middle">3x</text><rect class="dot2" opacity="0.35" x="120" y="154" width="120" height="52"/><rect class="curve3" x="120" y="154" width="120" height="52"/><text class="ink" x="180.0" y="185.0" font-size="14" text-anchor="middle">2x</text><rect class="dot3" opacity="0.35" x="240" y="154" width="78" height="52"/><rect class="curve3" x="240" y="154" width="78" height="52"/><text class="ink" x="279.0" y="185.0" font-size="14" text-anchor="middle">6</text><text class="ink" x="180.0" y="24" font-size="14" text-anchor="middle">x</text><text class="ink" x="279.0" y="24" font-size="14" text-anchor="middle">3</text><text class="ink" x="108" y="99.0" font-size="14" text-anchor="middle">x</text><text class="ink" x="108" y="185" font-size="14" text-anchor="middle">2</text><text class="ink" x="220" y="236" font-size="13" text-anchor="middle">(x + 3)(x + 2) = x² + 3x + 2x + 6 = x² + 5x + 6</text></svg>
  <figcaption>The area of a rectangle with sides $x + 3$ and $x + 2$ is the sum of four pieces: one $x^2$, two pieces of $x$ times a number ($3x$ and $2x$) and one constant ($6$). No piece is skipped in the multiplication.</figcaption>
</figure>

$$
(x + 3)(x + 2) = x \cdot x + x \cdot 2 + 3 \cdot x + 3 \cdot 2 = x^2 + 5x + 6
$$

Watch the signs:

$$
(2x + 3)(x - 4) = 2x^2 - 8x + 3x - 12 = 2x^2 - 5x - 12
$$

## Identities

Some products come up so often that their results are worth knowing by
heart:

| Identity | Example |
|---|---|
| $(a + b)^2 = a^2 + 2ab + b^2$ | $(x + 5)^2 = x^2 + 10x + 25$ |
| $(a - b)^2 = a^2 - 2ab + b^2$ | $(2x - 3)^2 = 4x^2 - 12x + 9$ |
| $(a + b)(a - b) = a^2 - b^2$ | $(x + 4)(x - 4) = x^2 - 16$ |

<figure class="fig">
<svg viewBox="0 0 490 278" width="490"><rect class="dot" opacity="0.35" x="150" y="30" width="130" height="130"/><rect class="curve3" x="150" y="30" width="130" height="130"/><text class="ink" x="215.0" y="100.0" font-size="16" text-anchor="middle">a²</text><rect class="dot2" opacity="0.35" x="280" y="30" width="60" height="130"/><rect class="curve3" x="280" y="30" width="60" height="130"/><text class="ink" x="310.0" y="100.0" font-size="14" text-anchor="middle">ab</text><rect class="dot2" opacity="0.35" x="150" y="160" width="130" height="60"/><rect class="curve3" x="150" y="160" width="130" height="60"/><text class="ink" x="215.0" y="195.0" font-size="14" text-anchor="middle">ab</text><rect class="dot3" opacity="0.35" x="280" y="160" width="60" height="60"/><rect class="curve3" x="280" y="160" width="60" height="60"/><text class="ink" x="310.0" y="195.0" font-size="14" text-anchor="middle">b²</text><text class="ink" x="215.0" y="20" font-size="14" text-anchor="middle">a</text><text class="ink" x="310.0" y="20" font-size="14" text-anchor="middle">b</text><text class="ink" x="138" y="100.0" font-size="14" text-anchor="middle">a</text><text class="ink" x="138" y="195.0" font-size="14" text-anchor="middle">b</text><text class="ink" x="245.0" y="248" font-size="13" text-anchor="middle">(a + b)² = a² + ab + ab + b² = a² + 2ab + b²</text><text class="dim" x="245.0" y="266" font-size="11" text-anchor="middle">the two ab rectangles must not be forgotten</text></svg>
  <figcaption>The area of a square with side $a + b$ is made of four pieces: $a^2$, $b^2$ and <b>two</b> $ab$s. Writing $(a + b)^2 = a^2 + b^2$ forgets the two rectangles.</figcaption>
</figure>

**Identity versus equation.** $(a + b)^2 = a^2 + 2ab + b^2$ is true for
**every** $a$ and $b$; that is called an identity. $2x + 1 = 7$ is true only
for $x = 3$; that is an equation.

**A quick test:** if you are not sure whether an equality is an identity,
put in a number. For $(a + b)^2 = a^2 + b^2$ take $a = 1$, $b = 2$: the left
is $9$, the right $5$. A single counterexample is enough: not an identity.
(But holding for a few numbers does **not prove** it is one; for a proof,
expand and simplify.)

### Mental arithmetic with identities

$$
\begin{aligned}
99^2 &= (100 - 1)^2 = 10\,000 - 200 + 1 = 9\,801 \\
51 \cdot 49 &= (50 + 1)(50 - 1) = 2\,500 - 1 = 2\,499
\end{aligned}
$$

## Algebraic expressions in machine learning

**A linear model.** A model with two inputs is
$\hat{y} = w_1 x_1 + w_2 x_2 + b$. With inputs $x_1 = 3$, $x_2 = -1$ and
weights $w_1 = 2$, $w_2 = 5$, $b = 1$, we get $\hat{y} = 6 - 5 + 1 = 2$:
evaluating an expression.

**Expanding the squared error.** For a single example the error is $(y -
wx)^2$. Expanding it with the identity gives

$$
(y - wx)^2 = y^2 - 2wxy + w^2 x^2
$$

an expression of degree two in the weight $w$. This expansion is the first
step to understanding how a model finds the best $w$.

## Common mistakes

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Wrong</h4>
      <p>$(a + b)^2 = a^2 + b^2$</p>
      <p>$-(x - 4) = -x - 4$</p>
      <p>$3x + 2y = 5xy$</p>
      <p>$x^2 + x^2 = x^4$</p>
      <p>$2x \cdot 3x = 6x$</p>
    </div>
    <div class="ok">
      <h4>Right</h4>
      <p>$(a + b)^2 = a^2 + 2ab + b^2$</p>
      <p>$-(x - 4) = -x + 4$</p>
      <p>$3x + 2y$ does not simplify</p>
      <p>$x^2 + x^2 = 2x^2$</p>
      <p>$2x \cdot 3x = 6x^2$</p>
    </div>
  </div>
  <figcaption>In addition only like terms combine and the exponent does not change; in multiplication the exponents add.</figcaption>
</figure>

- **Distributing a minus to the first term only.** In $-(x - 4)$ the minus
  goes to every term.
- **Adding exponents in addition.** $x^2 + x^2$ is two lots of $x^2$:
  $2x^2$. Exponents add only in multiplication.
- **Forgetting brackets when substituting.** For $x = -3$, $x^2 = (-3)^2 =
  9$.

## Summary

- An expression is made of terms; each term has a coefficient (with its sign) and a letter part.
- When substituting, write the number in brackets.
- Only like terms (same letters, same exponents) add: their coefficients add.
- Distributing: $a(b + c) = ab + ac$; $-(b - c) = -b + c$.
- Binomial times binomial gives four products: $(a + b)(c + d) = ac + ad + bc + bd$.
- $(a \pm b)^2 = a^2 \pm 2ab + b^2$; $(a + b)(a - b) = a^2 - b^2$.
- An identity holds for every value; a single counterexample shows it is not one.
