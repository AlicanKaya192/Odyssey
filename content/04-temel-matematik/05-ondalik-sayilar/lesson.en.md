# Decimals and Rounding

Fractions described a part of a whole. **Decimals** do the same job with
place value: instead of $\dfrac{3}{4}$ we write $0.75$. Measurements,
money, probabilities and nearly every number a computer works out are
decimals. In this section we will link decimals to fractions, do the four
operations, and learn to **round** properly.

Prerequisite: the Fractions section.

## Places after the decimal point

With natural numbers each place was $10$ times the one to its right. After
the decimal point the pattern continues: each place is **one tenth** of
the one to its left.

<figure class="fig">
<svg viewBox="0 0 400 156" width="400"><rect class="box" x="40" y="44" width="70" height="50"/><text class="ink" x="75.0" y="78" font-size="24" text-anchor="middle">3</text><text class="dim" x="75.0" y="36" font-size="11" text-anchor="middle">ones</text><text class="ink" x="121" y="82" font-size="28" text-anchor="middle">.</text><rect class="box" x="132" y="44" width="70" height="50"/><text class="ink" x="167.0" y="78" font-size="24" text-anchor="middle">7</text><text class="dim" x="167.0" y="36" font-size="11" text-anchor="middle">tenths</text><rect class="box" x="202" y="44" width="70" height="50"/><text class="ink" x="237.0" y="78" font-size="24" text-anchor="middle">5</text><text class="dim" x="237.0" y="36" font-size="11" text-anchor="middle">hundredths</text><rect class="box" x="272" y="44" width="70" height="50"/><text class="ink" x="307.0" y="78" font-size="24" text-anchor="middle">2</text><text class="dim" x="307.0" y="36" font-size="11" text-anchor="middle">thousandths</text><rect class="curve" x="129" y="41" width="216" height="56" rx="4"/><text class="dim" x="237.0" y="120" font-size="11" text-anchor="middle">×1/10 · ×1/100 · ×1/1000</text><text class="ink" x="191" y="144" font-size="13" text-anchor="middle">3.752 = 3 + 7/10 + 5/100 + 2/1000</text></svg>
  <figcaption>In $3.752$, $3$ is in the ones place, $7$ in the tenths, $5$ in the hundredths and $2$ in the thousandths. Each place to the right of the point is worth one tenth of the one before it.</figcaption>
</figure>

$$
3.752 = 3 + \frac{7}{10} + \frac{5}{100} + \frac{2}{1\,000}
$$

**Point or comma?** English and **every programming language** use a
point: `3.75`. Many other languages, Turkish among them, use a comma:
$3{,}75$. In Python, `3,75` means two separate numbers ($3$ and $75$). This
lesson uses a point in English; you can type either in the answer boxes.

**Zeros on the right do not change the value:** $0.5 = 0.50 = 0.500$.
That is because $\dfrac{5}{10} = \dfrac{50}{100}$.

## Converting between decimals and fractions

**Decimal to fraction:** write a denominator with as many zeros as there
are digits after the point, then simplify.

$$
0.36 = \frac{36}{100} = \frac{9}{25}, \qquad 2.125 = \frac{2\,125}{1\,000} = \frac{17}{8}
$$

**Fraction to decimal:** divide the numerator by the denominator. For
$\dfrac{7}{8}$:

$$
7 \div 8 = 0.875
$$

In long division we carry on by putting zeros after the $7$: $70 \div 8 =
8$ remainder $6$; $60 \div 8 = 7$ remainder $4$; $40 \div 8 = 5$
remainder $0$.

If the denominator easily expands to a power of $10$, no division is
needed: $\dfrac{3}{25} = \dfrac{12}{100} = 0.12$.

### Terminating and repeating decimals

$\dfrac{1}{3} = 0.333\dots$ never ends: dividing $1$ by $3$ always leaves
remainder $1$. Such numbers are called **repeating decimals**, and the
repeating part is written with a bar over it: $0.\overline{3}$.

When does the decimal form of a fraction end? When, in simplest form,
**the denominator's prime factors are only $2$ and $5$**, because $10 = 2
\cdot 5$ and the denominator can then be expanded to a power of $10$.
$\dfrac{7}{8}$ ends ($8 = 2^3$); $\dfrac{1}{3}$, $\dfrac{5}{6}$ and
$\dfrac{2}{7}$ do not.

**Turning a repeating decimal into a fraction:** let $x = 0.\overline{4} =
0.444\dots$ Multiplying by $10$ leaves the repeating part unchanged:

$$
\begin{aligned}
10x &= 4.444\dots \\
x &= 0.444\dots
\end{aligned}
$$

Subtracting one from the other, the endless tails cancel: $9x = 4$, so $x
= \dfrac{4}{9}$. A curious result: $0.\overline{9} = \dfrac{9}{9} = 1$.

## Comparing

Make the number of digits after the point equal by adding zeros on the
right, then compare like whole numbers:

$$
0.5 \;\;?\;\; 0.45 \quad\Rightarrow\quad 0.50 > 0.45
$$

**Longer is not larger.** $0.45$ has more digits, but $0.5$ is larger:
five tenths are more than four tenths.

## The four operations

**Addition and subtraction:** line up the points; fill missing places
with zeros.

$$
12.45 + 8.9 = 12.45 + 8.90 = 21.35
$$

**Multiplication:** ignore the points and multiply as whole numbers; the
result has as many digits after the point as the factors have **in
total**.

$$
3.75 \cdot 0.4: \quad 375 \cdot 4 = 1\,500, \quad 2 + 1 = 3 \text{ places} \quad\Rightarrow\quad 1.500 = 1.5
$$

Why? $3.75 = \dfrac{375}{100}$ and $0.4 = \dfrac{4}{10}$; the product has
denominator $1\,000$.

**Division:** move the point of **both numbers** the same number of places
to the right, until the divisor is a whole number. That multiplies the
dividend and the divisor by the same number ($10$, $100$, …), so the
quotient does not change.

$$
1.2 \div 0.05 = 120 \div 5 = 24
$$

**Multiplying and dividing by $10$, $100$, $1\,000$:** just move the
point by the number of zeros. $3.752 \cdot 100 = 375.2$ and $3.752 \div
100 = 0.03752$.

## Rounding

Rounding a number to a given place means choosing the **nearest** number
at that place.

<figure class="fig">
<svg viewBox="0 0 420 206" width="420"><line class="line" x1="32" y1="70" x2="388" y2="70"/><line class="line" x1="40" y1="60" x2="40" y2="80"/><line class="line" x1="74" y1="65" x2="74" y2="75"/><line class="line" x1="108" y1="65" x2="108" y2="75"/><line class="line" x1="142" y1="65" x2="142" y2="75"/><line class="line" x1="176" y1="65" x2="176" y2="75"/><line class="line" x1="210" y1="65" x2="210" y2="75"/><line class="line" x1="244" y1="65" x2="244" y2="75"/><line class="line" x1="278" y1="65" x2="278" y2="75"/><line class="line" x1="312" y1="65" x2="312" y2="75"/><line class="line" x1="346" y1="65" x2="346" y2="75"/><line class="line" x1="380" y1="60" x2="380" y2="80"/><text class="ink" x="40" y="98" font-size="13" text-anchor="middle">2.71</text><text class="ink" x="380" y="98" font-size="13" text-anchor="middle">2.72</text><line class="curve3" stroke-dasharray="4 3" x1="210" y1="40" x2="210" y2="82"/><text class="dim" x="210" y="98" font-size="11" text-anchor="middle">2.715</text><text class="dim" x="210" y="34" font-size="11" text-anchor="middle">midpoint</text><circle class="dot" cx="312" cy="70" r="6"/><text class="ink" x="312" y="54" font-size="13" text-anchor="middle">2.718</text><line class="curve2" x1="312" y1="116" x2="374" y2="116"/><polygon class="dot2" points="380,116 371,111 371,121"/><text class="ink" x="346" y="134" font-size="11" text-anchor="middle">0.002</text><line class="curve3" x1="312" y1="150" x2="46" y2="150"/><polygon class="dim" points="40,150 49,145 49,155"/><text class="dim" x="176" y="168" font-size="11" text-anchor="middle">0.008</text><text class="ink" x="210" y="194" font-size="13" text-anchor="middle">2.718 is closer to 2.72</text></svg>
  <figcaption>$2.718$ lies between $2.71$ and $2.72$. It is $0.002$ from $2.72$ and $0.008$ from $2.71$; rounded to two places it becomes $2.72$. Every number past the midpoint ($2.715$) rounds up.</figcaption>
</figure>

**The rule:** look at the digit just to the right of the place you are
rounding to. If it is $5$ or more, round up; if less, round down; drop
the digits on the right.

| Number | One place | Two places | Three places |
|---|---|---|---|
| $2.718\,28$ | $2.7$ | $2.72$ | $2.718$ |
| $0.654\,9$ | $0.7$ | $0.65$ | $0.655$ |
| $9.996$ | $10.0$ | $10.00$ | $9.996$ |

As in the last row, rounding can carry into the next place: rounding
$9.996$ to two places gives $9.99 + 0.01 = 10.00$.

**Leave rounding to the end.** Rounding at intermediate steps makes errors
pile up. Rounding $2.449$ to one place by going first to $2.45$ and then to
$2.5$ is wrong; looking directly, the digit after the tenths is $4$:
$2.4$.

**Truncating is not rounding.** **Truncating** $2.718$ to two places
(dropping the rest) gives $2.71$; rounding gives $2.72$.

## Decimals in machine learning

**A computer cannot hold every decimal exactly.** Type `0.1 + 0.2` in
Python and you get `0.30000000000000004`. The computer stores numbers in
binary, and in binary $0.1$ is a repeating decimal, like $\dfrac{1}{3}$
in base ten: it needs infinitely many digits and is cut off somewhere.
That is why decimals are not compared with `==`; instead we check
whether they are "close enough".

**Reporting metrics.** If accuracy comes out as $0.873\,46$, it is usually
written rounded, as $0.873$ or $87.3\%$. But the calculation itself uses
the exact value; rounding is only for display.

**Small numbers.** Values such as a learning rate can be $0.001$ or
$0.000\,1$; counting the zeros after the point matters, because each zero
changes the value tenfold.

## Common mistakes

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Wrong</h4>
      <p>$0.45 > 0.5$</p>
      <p>$0.3 \cdot 0.2 = 0.6$</p>
      <p>$1.2 \div 0.05 = 0.24$</p>
      <p>$2.449 \to 2.45 \to 2.5$</p>
    </div>
    <div class="ok">
      <h4>Right</h4>
      <p>$0.50 > 0.45$</p>
      <p>$0.3 \cdot 0.2 = 0.06$</p>
      <p>$1.2 \div 0.05 = 120 \div 5 = 24$</p>
      <p>$2.449 \to 2.4$</p>
    </div>
  </div>
  <figcaption>Watch the number of places: in a product they add up, and in division both points move.</figcaption>
</figure>

- **Thinking more digits means larger.** Equalise the places with zeros,
  then compare.
- **Putting the point in the wrong place in a product.** $0.3 \cdot 0.2$:
  $3 \cdot 2 = 6$ with $2$ places in total, $0.06$. Check: both numbers
  are less than $1$, so the product must be smaller than each.
- **Rounding in a chain.** Round once, looking at the place you want.

## Summary

- Places after the point: tenths, hundredths, thousandths; each is a tenth of the one to its left.
- Programming uses a point, many languages a comma: `3.75` and $3{,}75$ are the same number.
- Decimal → fraction: put a power of $10$ in the denominator, simplify. Fraction → decimal: divide the numerator by the denominator.
- If the denominator (in simplest form) has only $2$s and $5$s, the decimal ends; otherwise it repeats.
- $0.\overline{4} = \dfrac{4}{9}$: cancel the repeating part with $10x - x$.
- When comparing, equalise the places; longer is not larger.
- Multiplication: the numbers of places add up. Division: move both points by the same amount.
- Rounding: if the next digit is $5$ or more, round up; round once, at the end.
