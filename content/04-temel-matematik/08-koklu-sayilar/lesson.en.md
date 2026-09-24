# Roots

Squaring a number meant multiplying it by itself: $7^2 = 49$. The **square
root** asks the reverse: which number has square $49$? Roots are
everywhere in distances, in finding a side from an area, and in
statistics: the length of a vector, the standard deviation and a model's
root mean squared error (RMSE) are all worked out with a square root. In
this section we will see the square root, the root rules, simplifying
and fractional exponents.

Prerequisite: the Exponents section.

## What is a square root?

For $a \ge 0$, $\sqrt{a}$ is **the non-negative number whose square is
$a$**:

$$
\sqrt{49} = 7 \quad\text{because}\quad 7^2 = 49 \text{ and } 7 \ge 0
$$

$(-7)^2$ is also $49$, but $\sqrt{49}$ stands for a single number: the
positive one. If you are asked for "the numbers whose square is $49$",
there are two: if $x^2 = 49$ then $x = 7$ or $x = -7$, briefly $x = \pm 7$.

**The square root of a negative number** does not exist among the real
numbers: no real number has a negative square. $\sqrt{-4}$ is undefined.

The geometric meaning of the square root: **the side of a square with
area $a$**.

<figure class="fig">
<svg viewBox="0 0 420 176" width="420"><line class="grid" x1="40" y1="20" x2="40" y2="160"/><line class="grid" x1="40" y1="20" x2="180" y2="20"/><line class="grid" x1="110" y1="20" x2="110" y2="160"/><line class="grid" x1="40" y1="90" x2="180" y2="90"/><line class="grid" x1="180" y1="20" x2="180" y2="160"/><line class="grid" x1="40" y1="160" x2="180" y2="160"/><rect class="curve3" x="40" y="20" width="140" height="140"/><polygon class="dot" opacity="0.35" points="40,90 110,20 180,90 110,160"/><polygon class="curve" points="40,90 110,20 180,90 110,160"/><polygon class="dot2" opacity="0.35" points="40,90 40,20 110,20"/><polygon class="dot2" opacity="0.35" points="110,20 180,20 180,90"/><polygon class="dot2" opacity="0.35" points="180,90 180,160 110,160"/><polygon class="dot2" opacity="0.35" points="110,160 40,160 40,90"/><text class="ink" x="91.0" y="73.0" font-size="15" text-anchor="middle">√2</text><rect class="curve3" x="204" y="42" width="14" height="14"/><text class="ink" x="226" y="54" font-size="12" text-anchor="start">area 4, side 2</text><rect class="dot" opacity="0.35" x="204" y="72" width="14" height="14"/><text class="ink" x="226" y="84" font-size="12" text-anchor="start">area 2, side √2</text><rect class="dot2" opacity="0.35" x="204" y="102" width="14" height="14"/><text class="ink" x="226" y="114" font-size="12" text-anchor="start">4 × corner triangle = 2</text><text class="dim" x="226" y="144" font-size="11" text-anchor="start">half of the big square</text></svg>
  <figcaption>The $2 \times 2$ square has area $4$. The tilted square joining the midpoints of its sides is exactly half of it: the four orange corner triangles together make another tilted square. The tilted square has area $2$, so its side is $\sqrt{2}$.</figcaption>
</figure>

### Perfect squares

| $n$ | $n^2$ | $n$ | $n^2$ | $n$ | $n^2$ |
|---|---|---|---|---|---|
| $1$ | $1$ | $6$ | $36$ | $11$ | $121$ |
| $2$ | $4$ | $7$ | $49$ | $12$ | $144$ |
| $3$ | $9$ | $8$ | $64$ | $13$ | $169$ |
| $4$ | $16$ | $9$ | $81$ | $14$ | $196$ |
| $5$ | $25$ | $10$ | $100$ | $15$ | $225$ |

Knowing this table is half of working quickly with roots.

## Roots that do not come out exactly

Which number is $\sqrt{2}$? $1^2 = 1 < 2 < 4 = 2^2$, so it is between $1$
and $2$. $1.4^2 = 1.96$ and $1.5^2 = 2.25$: between $1.4$ and $1.5$.
Narrowing further, $\sqrt{2} = 1.414\,21\dots$

The decimal form of $\sqrt{2}$ neither ends nor repeats; it equals no
fraction. Such numbers are called **irrational**. The square root of any
natural number that is not a perfect square is irrational.

<figure class="fig">
<svg viewBox="0 0 460 140" width="460"><line class="line" x1="20" y1="88" x2="440" y2="88"/><line class="line" x1="30" y1="80" x2="30" y2="96"/><text class="ink" x="30" y="112" font-size="13" text-anchor="middle">0</text><text class="dim" x="30" y="128" font-size="11" text-anchor="middle">√0</text><line class="line" x1="110" y1="80" x2="110" y2="96"/><text class="ink" x="110" y="112" font-size="13" text-anchor="middle">1</text><text class="dim" x="110" y="128" font-size="11" text-anchor="middle">√1</text><line class="line" x1="190" y1="80" x2="190" y2="96"/><text class="ink" x="190" y="112" font-size="13" text-anchor="middle">2</text><text class="dim" x="190" y="128" font-size="11" text-anchor="middle">√4</text><line class="line" x1="270" y1="80" x2="270" y2="96"/><text class="ink" x="270" y="112" font-size="13" text-anchor="middle">3</text><text class="dim" x="270" y="128" font-size="11" text-anchor="middle">√9</text><line class="line" x1="350" y1="80" x2="350" y2="96"/><text class="ink" x="350" y="112" font-size="13" text-anchor="middle">4</text><text class="dim" x="350" y="128" font-size="11" text-anchor="middle">√16</text><line class="line" x1="430" y1="80" x2="430" y2="96"/><text class="ink" x="430" y="112" font-size="13" text-anchor="middle">5</text><text class="dim" x="430" y="128" font-size="11" text-anchor="middle">√25</text><line class="curve3" x1="143.1" y1="82" x2="143.1" y2="74"/><circle class="dot" cx="143.1" cy="88" r="5"/><text class="ink" x="143.1" y="54" font-size="13" text-anchor="middle">√2</text><text class="dim" x="143.1" y="68" font-size="10" text-anchor="middle">≈ 1.414</text><line class="curve3" x1="168.6" y1="82" x2="168.6" y2="48"/><circle class="dot" cx="168.6" cy="88" r="5"/><text class="ink" x="168.6" y="28" font-size="13" text-anchor="middle">√3</text><text class="dim" x="168.6" y="42" font-size="10" text-anchor="middle">≈ 1.732</text><line class="curve3" x1="208.9" y1="82" x2="208.9" y2="74"/><circle class="dot" cx="208.9" cy="88" r="5"/><text class="ink" x="208.9" y="54" font-size="13" text-anchor="middle">√5</text><text class="dim" x="208.9" y="68" font-size="10" text-anchor="middle">≈ 2.236</text><line class="curve3" x1="283.0" y1="82" x2="283.0" y2="48"/><circle class="dot" cx="283.0" cy="88" r="5"/><text class="ink" x="283.0" y="28" font-size="13" text-anchor="middle">√10</text><text class="dim" x="283.0" y="42" font-size="10" text-anchor="middle">≈ 3.162</text><line class="curve3" x1="387.8" y1="82" x2="387.8" y2="74"/><circle class="dot" cx="387.8" cy="88" r="5"/><text class="ink" x="387.8" y="54" font-size="13" text-anchor="middle">√20</text><text class="dim" x="387.8" y="68" font-size="10" text-anchor="middle">≈ 4.472</text></svg>
  <figcaption>The roots of perfect squares land on whole numbers ($\sqrt{4} = 2$, $\sqrt{9} = 3$). The roots in between sit between the perfect squares: $\sqrt{10}$ is just to the right of $\sqrt{9} = 3$; $\sqrt{20}$ is between $\sqrt{16} = 4$ and $\sqrt{25} = 5$, nearer to $4$.</figcaption>
</figure>

**Estimating:** what is $\sqrt{200}$? $14^2 = 196$ and $15^2 = 225$; $200$
is very close to $196$, so $\sqrt{200}$ is just above $14$: $14.14\dots$

## The root rules

Roots spread over multiplication and division:

$$
\sqrt{a \cdot b} = \sqrt{a} \cdot \sqrt{b}, \qquad \sqrt{\frac{a}{b}} = \frac{\sqrt{a}}{\sqrt{b}} \qquad (a, b \ge 0,\; b \neq 0)
$$

$$
\sqrt{4 \cdot 9} = \sqrt{36} = 6 = 2 \cdot 3 = \sqrt{4} \cdot \sqrt{9}
$$

But they **do not spread over addition**:

$$
\sqrt{9 + 16} = \sqrt{25} = 5, \qquad \sqrt{9} + \sqrt{16} = 3 + 4 = 7
$$

This is the other face of the mistake $(a + b)^2 \neq a^2 + b^2$.

**A root and a square cancel:** $(\sqrt{a})^2 = a$ ($a \ge 0$). In the
other order, careful: $\sqrt{x^2} = |x|$. For example $\sqrt{(-5)^2} =
\sqrt{25} = 5$, not $-5$.

## Simplifying roots

Split the number under the root using its **largest perfect-square
factor**, and take the perfect square outside:

$$
\sqrt{50} = \sqrt{25 \cdot 2} = \sqrt{25} \cdot \sqrt{2} = 5\sqrt{2}
$$

$$
\sqrt{72} = \sqrt{36 \cdot 2} = 6\sqrt{2}, \qquad \sqrt{48} = \sqrt{16 \cdot 3} = 4\sqrt{3}
$$

You can also go through prime factors: $72 = 2^3 \cdot 3^2 = (2 \cdot 3)^2
\cdot 2$; each pair comes outside as one factor.

**Addition and subtraction:** only **like roots** combine, just like $5x +
3x = 8x$.

$$
5\sqrt{2} + 3\sqrt{2} = 8\sqrt{2}, \qquad \sqrt{2} + \sqrt{3} \text{ does not combine}
$$

Simplifying first reveals hidden likeness: $\sqrt{50} + \sqrt{8} =
5\sqrt{2} + 2\sqrt{2} = 7\sqrt{2}$.

**Multiplication:** coefficients multiply with coefficients, roots with
roots:

$$
2\sqrt{3} \cdot 4\sqrt{3} = (2 \cdot 4) \cdot (\sqrt{3} \cdot \sqrt{3}) = 8 \cdot 3 = 24
$$

## Clearing a root from the denominator

In a number like $\dfrac{6}{\sqrt{3}}$ we prefer no root in the
denominator. Multiply top and bottom by $\sqrt{3}$ (the value does not
change, $\frac{\sqrt{3}}{\sqrt{3}} = 1$):

$$
\frac{6}{\sqrt{3}} = \frac{6 \cdot \sqrt{3}}{\sqrt{3} \cdot \sqrt{3}} = \frac{6\sqrt{3}}{3} = 2\sqrt{3}
$$

The result is the same number but easier to compare and to add.

## Other roots and fractional exponents

**Cube root:** $\sqrt[3]{a}$ is the number whose cube is $a$. $\sqrt[3]{8}
= 2$, $\sqrt[3]{125} = 5$. Odd roots exist for negative numbers too:
$\sqrt[3]{-27} = -3$, because $(-3)^3 = -27$.

In general $\sqrt[n]{a}$ is the number whose $n$th power is $a$:
$\sqrt[4]{16} = 2$, $\sqrt[5]{32} = 2$.

**Fractional exponents:** for the exponent rules to keep working, what
must $a^{1/2}$ be? $(a^{1/2})^2 = a^{1/2 \cdot 2} = a^1 = a$. The number
whose square is $a$: $\sqrt{a}$.

$$
a^{1/n} = \sqrt[n]{a}, \qquad a^{m/n} = \left(\sqrt[n]{a}\right)^m
$$

$$
8^{2/3} = \left(\sqrt[3]{8}\right)^2 = 2^2 = 4, \qquad 16^{-1/2} = \frac{1}{\sqrt{16}} = \frac{1}{4}
$$

In a fractional exponent the denominator gives the degree of the root and
the numerator the power. Taking the root first keeps the numbers small.

## Roots in machine learning

**Length and distance.** The length of the vector $(3, 4)$ is $\sqrt{3^2 +
4^2} = \sqrt{25} = 5$. The distance between two points is the basis of
methods such as nearest neighbours.

**RMSE.** The square root of the mean of the squared errors: squaring
frees the errors from their signs, and the root brings back the original
unit. If the errors are $3, -1, 2, -2$,

$$
\sqrt{\frac{9 + 1 + 4 + 4}{4}} = \sqrt{4.5} \approx 2.12
$$

**Scaling.** In the attention mechanism, scores are divided by
$\sqrt{d}$; with $d = 64$, by $\sqrt{64} = 8$.

## Common mistakes

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Wrong</h4>
      <p>$\sqrt{9 + 16} = 3 + 4$</p>
      <p>$\sqrt{49} = \pm 7$</p>
      <p>$\sqrt{2} + \sqrt{3} = \sqrt{5}$</p>
      <p>$\sqrt{(-5)^2} = -5$</p>
    </div>
    <div class="ok">
      <h4>Right</h4>
      <p>$\sqrt{25} = 5$</p>
      <p>$\sqrt{49} = 7$; but $x^2 = 49 \Rightarrow x = \pm 7$</p>
      <p>No combining: $\sqrt{2} + \sqrt{3} \approx 3.15$, $\sqrt{5} \approx 2.24$</p>
      <p>$\sqrt{(-5)^2} = \lvert -5 \rvert = 5$</p>
    </div>
  </div>
  <figcaption>Roots spread over multiplication and division but not over addition; the $\sqrt{\;}$ sign always means the non-negative root.</figcaption>
</figure>

- **Spreading a root over a sum.** $\sqrt{a + b} \neq \sqrt{a} + \sqrt{b}$.
- **Giving the $\sqrt{\;}$ sign two values.** $\sqrt{49}$ is just $7$; the
  $\pm$ appears when solving an equation.
- **Stopping halfway when simplifying.** $\sqrt{72} = 2\sqrt{18}$ is true
  but not finished; use the largest perfect-square factor ($36$):
  $6\sqrt{2}$.

## Summary

- $\sqrt{a}$: the non-negative number whose square is $a$ ($a \ge 0$). If $x^2 = a$, then $x = \pm\sqrt{a}$.
- In geometry, the side of a square with area $a$. Roots of non-perfect squares are irrational.
- $\sqrt{ab} = \sqrt{a}\sqrt{b}$, $\sqrt{a/b} = \sqrt{a}/\sqrt{b}$; but $\sqrt{a + b} \neq \sqrt{a} + \sqrt{b}$.
- $(\sqrt{a})^2 = a$, $\sqrt{x^2} = |x|$.
- Simplifying: take the largest perfect-square factor outside. Only like roots add.
- Clear a root from a denominator by multiplying top and bottom by it.
- $a^{1/n} = \sqrt[n]{a}$, $a^{m/n} = (\sqrt[n]{a})^m$.
- RMSE, standard deviation, vector length: all are a square root.
