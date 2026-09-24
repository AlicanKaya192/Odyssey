# Factoring

In the previous section we expanded products: $(x + 2)(x + 3) = x^2 + 5x +
6$. Factoring is the **reverse**: writing a sum as the factors that give it
when multiplied. Why would we want that? Because the product form says
much more: when an expression is zero, how a fraction simplifies and how
a calculation can be shortened are all read from the factors. It is also
the quickest way to solve quadratic equations.

Prerequisite: Algebraic Expressions and Identities, Divisibility (GCD).

## Taking out a common factor

Take out the factor common to every term. For coefficients use the
**GCD**, for letters the **smallest exponent**:

$$
6x^2 + 9x = 3x(2x + 3)
$$

The GCD of $6$ and $9$ is $3$; what $x^2$ and $x$ share is $x$. The inside
of the bracket is each term divided by $3x$: $6x^2 \div 3x = 2x$, $9x \div
3x = 3$.

**Take it all out:** $6x^2 + 9x = 3(2x^2 + 3x)$ is true but unfinished;
there is still a common $x$ inside the bracket.

**Checking is always easy:** expand the bracket again; you should get back
to the start.

### Grouping

If four terms have no common factor all at once, group them in pairs:

$$
\begin{aligned}
ax + ay + bx + by &= a(x + y) + b(x + y) \\
&= (a + b)(x + y)
\end{aligned}
$$

In the second line $(x + y)$ became a **common factor** of the two terms
and was taken out.

## Patterns from the identities

The identities of the Algebraic Expressions section, read backwards,
become factoring patterns:

| Pattern | Factors | Example |
|---|---|---|
| $a^2 - b^2$ | $(a - b)(a + b)$ | $x^2 - 49 = (x - 7)(x + 7)$ |
| $a^2 + 2ab + b^2$ | $(a + b)^2$ | $x^2 + 10x + 25 = (x + 5)^2$ |
| $a^2 - 2ab + b^2$ | $(a - b)^2$ | $9x^2 - 12x + 4 = (3x - 2)^2$ |

**Recognise a difference of squares:** two terms, both perfect squares,
with a minus between them. $4x^2 - 25 = (2x)^2 - 5^2 = (2x - 5)(2x + 5)$.

**A sum of squares** (such as $x^2 + 9$) does not factor with real numbers.
$(x + 3)^2 = x^2 + 6x + 9$ has a $6x$ in the middle.

## Trinomials: x² + bx + c

Expanding $(x + p)(x + q)$ gives

$$
(x + p)(x + q) = x^2 + (p + q)x + pq
$$

So to factor $x^2 + bx + c$ we look for two numbers $p$ and $q$ **whose
product is $c$ and whose sum is $b$**.

<figure class="fig">
<svg viewBox="0 0 480 206" width="480"><line class="curve3" x1="58" y1="38" x2="182" y2="162"/><line class="curve3" x1="182" y1="38" x2="58" y2="162"/><text class="ink" x="120" y="60" font-size="16" text-anchor="middle">6</text><text class="dim" x="120" y="76" font-size="10" text-anchor="middle">product</text><text class="ink" x="120" y="146" font-size="16" text-anchor="middle">5</text><text class="dim" x="120" y="160" font-size="10" text-anchor="middle">sum</text><circle class="dot" opacity="0.3" cx="76" cy="100" r="18"/><text class="ink" x="76" y="106" font-size="16" text-anchor="middle">2</text><circle class="dot" opacity="0.3" cx="164" cy="100" r="18"/><text class="ink" x="164" y="106" font-size="16" text-anchor="middle">3</text><text class="ink" x="120" y="192" font-size="12" text-anchor="middle">x² + 5x + 6 = (x + 2)(x + 3)</text><line class="curve3" x1="298" y1="38" x2="422" y2="162"/><line class="curve3" x1="422" y1="38" x2="298" y2="162"/><text class="ink" x="360" y="60" font-size="16" text-anchor="middle">−12</text><text class="dim" x="360" y="76" font-size="10" text-anchor="middle">product</text><text class="ink" x="360" y="146" font-size="16" text-anchor="middle">−1</text><text class="dim" x="360" y="160" font-size="10" text-anchor="middle">sum</text><circle class="dot" opacity="0.3" cx="316" cy="100" r="18"/><text class="ink" x="316" y="106" font-size="16" text-anchor="middle">−4</text><circle class="dot" opacity="0.3" cx="404" cy="100" r="18"/><text class="ink" x="404" y="106" font-size="16" text-anchor="middle">3</text><text class="ink" x="360" y="192" font-size="12" text-anchor="middle">x² − x − 12 = (x − 4)(x + 3)</text></svg>
  <figcaption>The diamond method: write the product ($c$) at the top and the sum ($b$) at the bottom; on the two sides, find the numbers whose product is the top and whose sum is the bottom. Left: $2 \cdot 3 = 6$, $2 + 3 = 5$. Right: $(-4) \cdot 3 = -12$, $-4 + 3 = -1$.</figcaption>
</figure>

**Example:** $x^2 + 5x + 6$. Integer pairs with product $6$: $1 \cdot 6$,
$2 \cdot 3$ (and their negatives). The one with sum $5$: $2$ and $3$.

$$
x^2 + 5x + 6 = (x + 2)(x + 3)
$$

<figure class="fig">
<svg viewBox="0 0 420 266" width="420"><rect class="dot" opacity="0.35" x="130" y="48" width="110" height="110"/><rect class="curve3" x="130" y="48" width="110" height="110"/><text class="ink" x="185.0" y="108.0" font-size="16" text-anchor="middle">x²</text><rect class="dot2" opacity="0.35" x="240" y="48" width="24" height="110"/><rect class="curve3" x="240" y="48" width="24" height="110"/><text class="ink" x="252.0" y="108.0" font-size="13" text-anchor="middle">x</text><rect class="dot2" opacity="0.35" x="264" y="48" width="24" height="110"/><rect class="curve3" x="264" y="48" width="24" height="110"/><text class="ink" x="276.0" y="108.0" font-size="13" text-anchor="middle">x</text><rect class="dot2" opacity="0.35" x="288" y="48" width="24" height="110"/><rect class="curve3" x="288" y="48" width="24" height="110"/><text class="ink" x="300.0" y="108.0" font-size="13" text-anchor="middle">x</text><rect class="dot2" opacity="0.35" x="130" y="158" width="110" height="24"/><rect class="curve3" x="130" y="158" width="110" height="24"/><text class="ink" x="185.0" y="175.0" font-size="13" text-anchor="middle">x</text><rect class="dot2" opacity="0.35" x="130" y="182" width="110" height="24"/><rect class="curve3" x="130" y="182" width="110" height="24"/><text class="ink" x="185.0" y="199.0" font-size="13" text-anchor="middle">x</text><rect class="dot3" opacity="0.35" x="240" y="158" width="24" height="24"/><rect class="curve3" x="240" y="158" width="24" height="24"/><rect class="dot3" opacity="0.35" x="264" y="158" width="24" height="24"/><rect class="curve3" x="264" y="158" width="24" height="24"/><rect class="dot3" opacity="0.35" x="288" y="158" width="24" height="24"/><rect class="curve3" x="288" y="158" width="24" height="24"/><rect class="dot3" opacity="0.35" x="240" y="182" width="24" height="24"/><rect class="curve3" x="240" y="182" width="24" height="24"/><rect class="dot3" opacity="0.35" x="264" y="182" width="24" height="24"/><rect class="curve3" x="264" y="182" width="24" height="24"/><rect class="dot3" opacity="0.35" x="288" y="182" width="24" height="24"/><rect class="curve3" x="288" y="182" width="24" height="24"/><line class="curve" x1="130" y1="34" x2="312" y2="34"/><text class="ink" x="221.0" y="26" font-size="14" text-anchor="middle">x + 3</text><line class="curve" x1="116" y1="48" x2="116" y2="206"/><text class="ink" x="108" y="132.0" font-size="14" text-anchor="end">x + 2</text><text class="dim" x="221.0" y="234" font-size="11" text-anchor="middle">pieces: one x², five x, six units</text><text class="ink" x="221.0" y="254" font-size="13" text-anchor="middle">x² + 5x + 6 = (x + 3)(x + 2)</text></svg>
  <figcaption>The same job with area: arrange one $x^2$ square, five $x$ strips and six unit squares into a rectangle with no gaps, and the sides come out as $x + 3$ and $x + 2$. Factoring means finding the sides of a rectangle whose area is known.</figcaption>
</figure>

**A tip for the signs:**

| $c$ | $b$ | $p$ and $q$ |
|---|---|---|
| positive | positive | both positive |
| positive | negative | both negative |
| negative | any | opposite signs; the larger takes the sign of $b$ |

$x^2 - x - 12$: product $-12$ (opposite signs), sum $-1$ (the larger is
negative). $-4$ and $3$: $(x - 4)(x + 3)$.

## Trinomials: ax² + bx + c

If the coefficient of $x^2$ is not $1$, use the **$ac$ method**: find two
numbers with product $a \cdot c$ and sum $b$, split the middle term with
them, then group.

$$
2x^2 + 7x + 3
$$

$a \cdot c = 6$, sum $7$: $6$ and $1$.

$$
\begin{aligned}
2x^2 + 7x + 3 &= 2x^2 + 6x + x + 3 \\
&= 2x(x + 3) + 1(x + 3) \\
&= (2x + 1)(x + 3)
\end{aligned}
$$

**Check:** $(2x + 1)(x + 3) = 2x^2 + 6x + x + 3$ ✓.

## Where to start?

<figure class="fig">
  <div class="flow">
    <span class="node acc"><b>1. Common factor</b><br>is there one?</span>
    <span class="arrow">→</span>
    <span class="node"><b>2. Pattern</b><br>identities</span>
    <span class="arrow">→</span>
    <span class="node"><b>3. Trinomial</b><br>product–sum</span>
    <span class="arrow">→</span>
    <span class="node"><b>4. Check</b><br>expand again</span>
  </div>
  <figcaption>Always take out the common factor first; what is left often turns into a pattern or a simple trinomial. At the end, expand the factors and see that you get back to the start.</figcaption>
</figure>

$$
\begin{aligned}
3x^3 - 12x &= 3x(x^2 - 4) \\
&= 3x(x - 2)(x + 2)
\end{aligned}
$$

## Simplifying fractions

In fractions, cancelling is only done between **factors**. First factor
the top and the bottom:

$$
\frac{x^2 - 9}{x^2 + 5x + 6} = \frac{(x - 3)(x + 3)}{(x + 2)(x + 3)} = \frac{x - 3}{x + 2}
$$

This equality holds except at $x = -3$ and $x = -2$: at those values the
original fraction's denominator is zero.

## When a product is zero

If the product of two numbers is zero, at least one of them is zero. So
the places where a factored expression is zero can be read off at once:

$$
(x - 2)(x + 5) = 0 \quad\Rightarrow\quad x = 2 \text{ or } x = -5
$$

In the Quadratic Equations section this idea will be our main method.

## Factoring in machine learning

**Fewer operations.** $w x_1 + w x_2 + w x_3$ takes three multiplications
and two additions; $w(x_1 + x_2 + x_3)$ takes two additions and **one**
multiplication. In calculations repeated millions of times, taking out a
common factor saves real time.

**Zeros.** The points where a model changes its behaviour are often where
some expression is zero. In a factored expression those points are visible
without any calculation.

## Common mistakes

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Wrong</h4>
      <p>$x^2 - 9 = (x - 3)^2$</p>
      <p>$x^2 + 9 = (x + 3)^2$</p>
      <p>$\dfrac{x + 3}{3} = x$</p>
      <p>$6x^2 + 9x = 3(2x^2 + 3x)$ (done)</p>
    </div>
    <div class="ok">
      <h4>Right</h4>
      <p>$x^2 - 9 = (x - 3)(x + 3)$</p>
      <p>$x^2 + 9$ does not factor</p>
      <p>$\dfrac{x + 3}{3}$ does not cancel; $3$ is a term</p>
      <p>$6x^2 + 9x = 3x(2x + 3)$</p>
    </div>
  </div>
  <figcaption>Test every result by expanding the factors; cancel only between factors.</figcaption>
</figure>

- **Sign errors.** Factoring $x^2 - x - 12$ as $(x + 4)(x - 3)$ makes the
  middle term $+x$. Expanding again catches it at once.
- **Cancelling a term of a sum.** In $\dfrac{x + 3}{x + 5}$ the $x$s do not
  cancel; both are terms.

## Summary

- Factoring is the reverse of expanding; test the result by expanding it.
- Common factor first: GCD for coefficients, smallest exponent for letters; take it all out.
- Grouping four terms: $ax + ay + bx + by = (a + b)(x + y)$.
- $a^2 - b^2 = (a - b)(a + b)$; $a^2 \pm 2ab + b^2 = (a \pm b)^2$; $a^2 + b^2$ does not factor.
- $x^2 + bx + c$: two numbers with product $c$ and sum $b$.
- $ax^2 + bx + c$: split the middle term with numbers of product $ac$ and sum $b$, then group.
- In a fraction, cancel only between factors; values that make the denominator zero are excluded.
- If $AB = 0$, then $A = 0$ or $B = 0$.
