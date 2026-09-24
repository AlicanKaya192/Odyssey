# Integers and Negative Numbers

With natural numbers we could not do $5 - 8$: taking $8$ from $5$ does
not give a natural number. But life is full of such situations: the
temperature drops below zero, an account goes into the red, a lift goes
below the ground floor. To describe them we extend the numbers **to the
left of zero** too: negative numbers.

In this section we will see integers on the number line, define absolute
value, and learn the sign rules of the four operations together with
**why** they are the way they are. In machine learning, errors, slopes
and weights take negative values all the time; being able to apply these
rules automatically matters.

Prerequisite: the Natural Numbers and Order of Operations section.

## Integers and the number line

The **integers** are the natural numbers together with their negatives:

$$
\mathbb{Z} = \{\dots, -3, -2, -1, 0, 1, 2, 3, \dots\}
$$

The letter $\mathbb{Z}$ comes from the German *Zahlen*, "numbers". Zero
is neither positive nor negative; it is the border between the two sides.

<figure class="fig">
<svg viewBox="0 0 460 138" width="460"><path class="curve2" d="M 230 66 L 230 44 L 110 44 L 110 66"/><text class="ink" x="170.0" y="36" font-size="12" text-anchor="middle">|−4| = 4</text><path class="curve" d="M 230 66 L 230 44 L 350 44 L 350 66"/><text class="ink" x="290.0" y="36" font-size="12" text-anchor="middle">|4| = 4</text><line class="line" x1="10" y1="78" x2="450" y2="78"/><line class="line" x1="20" y1="72" x2="20" y2="84"/><text class="dim" x="20" y="102" font-size="11" text-anchor="middle">−7</text><line class="line" x1="50" y1="72" x2="50" y2="84"/><text class="dim" x="50" y="102" font-size="11" text-anchor="middle">−6</text><line class="line" x1="80" y1="72" x2="80" y2="84"/><text class="dim" x="80" y="102" font-size="11" text-anchor="middle">−5</text><line class="line" x1="110" y1="72" x2="110" y2="84"/><text class="dim" x="110" y="102" font-size="11" text-anchor="middle">−4</text><line class="line" x1="140" y1="72" x2="140" y2="84"/><text class="dim" x="140" y="102" font-size="11" text-anchor="middle">−3</text><line class="line" x1="170" y1="72" x2="170" y2="84"/><text class="dim" x="170" y="102" font-size="11" text-anchor="middle">−2</text><line class="line" x1="200" y1="72" x2="200" y2="84"/><text class="dim" x="200" y="102" font-size="11" text-anchor="middle">−1</text><line class="line" x1="230" y1="69" x2="230" y2="87"/><text class="ink" x="230" y="102" font-size="11" text-anchor="middle">0</text><line class="line" x1="260" y1="72" x2="260" y2="84"/><text class="dim" x="260" y="102" font-size="11" text-anchor="middle">1</text><line class="line" x1="290" y1="72" x2="290" y2="84"/><text class="dim" x="290" y="102" font-size="11" text-anchor="middle">2</text><line class="line" x1="320" y1="72" x2="320" y2="84"/><text class="dim" x="320" y="102" font-size="11" text-anchor="middle">3</text><line class="line" x1="350" y1="72" x2="350" y2="84"/><text class="dim" x="350" y="102" font-size="11" text-anchor="middle">4</text><line class="line" x1="380" y1="72" x2="380" y2="84"/><text class="dim" x="380" y="102" font-size="11" text-anchor="middle">5</text><line class="line" x1="410" y1="72" x2="410" y2="84"/><text class="dim" x="410" y="102" font-size="11" text-anchor="middle">6</text><line class="line" x1="440" y1="72" x2="440" y2="84"/><text class="dim" x="440" y="102" font-size="11" text-anchor="middle">7</text><circle class="dot2" cx="110" cy="78" r="5"/><circle class="dot" cx="350" cy="78" r="5"/><text class="dim" x="65.0" y="126" font-size="11" text-anchor="middle">← negatives</text><text class="dim" x="395.0" y="126" font-size="11" text-anchor="middle">positives →</text><text class="ink" x="230" y="126" font-size="12" text-anchor="middle">opposites: −4 and 4</text></svg>
  <figcaption>On the number line, the right of zero is positive and the left is negative. $-4$ and $4$ are the same distance from zero but on opposite sides: they are called opposites. Both have distance $4$ from zero, that is, absolute value $4$.</figcaption>
</figure>

**Ordering:** On the number line the number further right is larger. So

$$
-5 < -2 < 0 < 3
$$

With negatives, intuition can work backwards: $-5$ is **smaller** than
$-2$, because it is further left. Think of temperature: $-5$ degrees is
colder than $-2$ degrees.

## Opposites and absolute value

The **opposite** of a number is the number on the other side of zero on
the number line: the opposite of $3$ is $-3$, the opposite of $-7$ is
$7$. A number plus its opposite is always $0$:

$$
a + (-a) = 0
$$

The minus sign also means "take the opposite". That is why

$$
-(-5) = 5
$$

"The opposite of $-5$" is $5$. Two minuses side by side cancel.

The **absolute value** $|a|$ is a number's **distance** from zero. A
distance cannot be negative:

$$
|7| = 7, \qquad \lvert -7 \rvert = 7, \qquad |0| = 0
$$

The distance between two numbers is also written with absolute value:
the distance between $a$ and $b$ is $|a - b|$. For example, from $-3$
to $5$ is $\lvert -3 - 5 \rvert = \lvert -8 \rvert = 8$ units.

## Addition

On the number line, addition is a **walk**: for $a + b$, start at $a$
and take $|b|$ steps, to the right if $b$ is positive and to the left if
it is negative.

<figure class="fig">
<svg viewBox="0 0 460 216" width="460"><text class="ink" x="230" y="18" font-size="13" text-anchor="middle">−3 + 5 = 2</text><text class="dim" x="230" y="34" font-size="11" text-anchor="middle">go to −3, then 5 steps right</text><line class="curve2" x1="230" y1="46" x2="147" y2="46"/><polygon class="dot2" points="140,46 150,41 150,51"/><line class="curve" x1="140" y1="58" x2="283" y2="58"/><polygon class="dot" points="290,58 280,53 280,63"/><line class="line" x1="10" y1="70" x2="450" y2="70"/><line class="line" x1="20" y1="64" x2="20" y2="76"/><text class="dim" x="20" y="94" font-size="11" text-anchor="middle">−7</text><line class="line" x1="50" y1="64" x2="50" y2="76"/><text class="dim" x="50" y="94" font-size="11" text-anchor="middle">−6</text><line class="line" x1="80" y1="64" x2="80" y2="76"/><text class="dim" x="80" y="94" font-size="11" text-anchor="middle">−5</text><line class="line" x1="110" y1="64" x2="110" y2="76"/><text class="dim" x="110" y="94" font-size="11" text-anchor="middle">−4</text><line class="line" x1="140" y1="64" x2="140" y2="76"/><text class="dim" x="140" y="94" font-size="11" text-anchor="middle">−3</text><line class="line" x1="170" y1="64" x2="170" y2="76"/><text class="dim" x="170" y="94" font-size="11" text-anchor="middle">−2</text><line class="line" x1="200" y1="64" x2="200" y2="76"/><text class="dim" x="200" y="94" font-size="11" text-anchor="middle">−1</text><line class="line" x1="230" y1="61" x2="230" y2="79"/><text class="ink" x="230" y="94" font-size="11" text-anchor="middle">0</text><line class="line" x1="260" y1="64" x2="260" y2="76"/><text class="dim" x="260" y="94" font-size="11" text-anchor="middle">1</text><line class="line" x1="290" y1="64" x2="290" y2="76"/><text class="dim" x="290" y="94" font-size="11" text-anchor="middle">2</text><line class="line" x1="320" y1="64" x2="320" y2="76"/><text class="dim" x="320" y="94" font-size="11" text-anchor="middle">3</text><line class="line" x1="350" y1="64" x2="350" y2="76"/><text class="dim" x="350" y="94" font-size="11" text-anchor="middle">4</text><line class="line" x1="380" y1="64" x2="380" y2="76"/><text class="dim" x="380" y="94" font-size="11" text-anchor="middle">5</text><line class="line" x1="410" y1="64" x2="410" y2="76"/><text class="dim" x="410" y="94" font-size="11" text-anchor="middle">6</text><line class="line" x1="440" y1="64" x2="440" y2="76"/><text class="dim" x="440" y="94" font-size="11" text-anchor="middle">7</text><circle class="dot3" cx="290" cy="70" r="5"/><text class="ink" x="230" y="128" font-size="13" text-anchor="middle">2 − 6 = 2 + (−6) = −4</text><text class="dim" x="230" y="144" font-size="11" text-anchor="middle">go to 2, then 6 steps left</text><line class="curve" x1="230" y1="156" x2="283" y2="156"/><polygon class="dot" points="290,156 280,151 280,161"/><line class="curve2" x1="290" y1="168" x2="117" y2="168"/><polygon class="dot2" points="110,168 120,163 120,173"/><line class="line" x1="10" y1="180" x2="450" y2="180"/><line class="line" x1="20" y1="174" x2="20" y2="186"/><text class="dim" x="20" y="204" font-size="11" text-anchor="middle">−7</text><line class="line" x1="50" y1="174" x2="50" y2="186"/><text class="dim" x="50" y="204" font-size="11" text-anchor="middle">−6</text><line class="line" x1="80" y1="174" x2="80" y2="186"/><text class="dim" x="80" y="204" font-size="11" text-anchor="middle">−5</text><line class="line" x1="110" y1="174" x2="110" y2="186"/><text class="dim" x="110" y="204" font-size="11" text-anchor="middle">−4</text><line class="line" x1="140" y1="174" x2="140" y2="186"/><text class="dim" x="140" y="204" font-size="11" text-anchor="middle">−3</text><line class="line" x1="170" y1="174" x2="170" y2="186"/><text class="dim" x="170" y="204" font-size="11" text-anchor="middle">−2</text><line class="line" x1="200" y1="174" x2="200" y2="186"/><text class="dim" x="200" y="204" font-size="11" text-anchor="middle">−1</text><line class="line" x1="230" y1="171" x2="230" y2="189"/><text class="ink" x="230" y="204" font-size="11" text-anchor="middle">0</text><line class="line" x1="260" y1="174" x2="260" y2="186"/><text class="dim" x="260" y="204" font-size="11" text-anchor="middle">1</text><line class="line" x1="290" y1="174" x2="290" y2="186"/><text class="dim" x="290" y="204" font-size="11" text-anchor="middle">2</text><line class="line" x1="320" y1="174" x2="320" y2="186"/><text class="dim" x="320" y="204" font-size="11" text-anchor="middle">3</text><line class="line" x1="350" y1="174" x2="350" y2="186"/><text class="dim" x="350" y="204" font-size="11" text-anchor="middle">4</text><line class="line" x1="380" y1="174" x2="380" y2="186"/><text class="dim" x="380" y="204" font-size="11" text-anchor="middle">5</text><line class="line" x1="410" y1="174" x2="410" y2="186"/><text class="dim" x="410" y="204" font-size="11" text-anchor="middle">6</text><line class="line" x1="440" y1="174" x2="440" y2="186"/><text class="dim" x="440" y="204" font-size="11" text-anchor="middle">7</text><circle class="dot3" cx="110" cy="180" r="5"/></svg>
  <figcaption>Addition is walking along the number line. $-3 + 5$: start at $-3$ and walk $5$ steps right to reach $2$. Subtraction is adding the opposite: $2 - 6$ means walking $6$ steps left from $2$ and reaching $-4$.</figcaption>
</figure>

This walk turns into two rules:

| Case | Rule | Example |
|---|---|---|
| Same signs | add the absolute values, keep the common sign | $-4 + (-6) = -10$ |
| Different signs | subtract the smaller absolute value from the larger, take the sign of the larger | $-9 + 4 = -5$ |

In the second row $\lvert -9 \rvert = 9$ is larger, $9 - 4 = 5$, and the result
takes the sign of $-9$. A debt picture helps: you owe $9$ pounds and pay
back $4$; you still owe $5$.

## Subtraction: adding the opposite

Instead of memorising subtraction of integers as a separate operation, we
**turn it into addition**:

$$
a - b = a + (-b)
$$

That way every subtraction becomes an addition, and the two rules above
are enough:

$$
\begin{aligned}
3 - 8 &= 3 + (-8) = -5 \\
-2 - 6 &= -2 + (-6) = -8 \\
5 - (-4) &= 5 + 4 = 9 \\
-7 - (-10) &= -7 + 10 = 3
\end{aligned}
$$

**Subtracting a negative number is adding its positive.** If the
temperature went from $-3$ degrees up to $5$ degrees, the change is
$5 - (-3) = 8$ degrees.

## Multiplication and division: sign rules

First multiply or divide the absolute values, then decide the sign:

| | positive | negative |
|---|---|---|
| **positive** | $+$ | $-$ |
| **negative** | $-$ | $+$ |

**Same signs give positive, different signs give negative:**

$$
(-3) \cdot 4 = -12, \qquad (-3) \cdot (-4) = 12, \qquad (-20) \div 5 = -4, \qquad (-20) \div (-5) = 4
$$

The rule is the same for division, because division reverses
multiplication: $(-20) \div (-5) = 4$, because $4 \cdot (-5) = -20$.

### Why is minus times minus plus?

Let us see it through a pattern. Multiply $-3$ by $3, 2, 1, 0$ in turn:

$$
\begin{aligned}
(-3) \cdot 3 &= -9 \\
(-3) \cdot 2 &= -6 \\
(-3) \cdot 1 &= -3 \\
(-3) \cdot 0 &= 0
\end{aligned}
$$

Each time the multiplier drops by $1$, the result **rises** by $3$. If
the pattern continues, $(-3) \cdot (-1) = 3$ and $(-3) \cdot (-2) = 6$.
Any other answer would break the distributive property: $(-3) \cdot (2
+ (-2)) = (-3) \cdot 0 = 0$ must hold, and that only works if $(-3)(-2)
= 6$.

**With many factors**, count the minuses: an even number of minuses
gives a positive result, an odd number gives a negative one.

$$
(-1) \cdot (-2) \cdot (-3) = -6, \qquad (-1) \cdot (-2) \cdot (-3) \cdot (-4) = 24
$$

## Powers of negative numbers

Here the brackets are everything:

$$
(-2)^2 = (-2) \cdot (-2) = 4, \qquad -2^2 = -(2 \cdot 2) = -4
$$

In $-2^2$ the exponent belongs only to the $2$; the minus is applied last
(exponents come first in the order of operations). For a negative
number:

- an **even** power is positive: $(-2)^4 = 16$,
- an **odd** power is negative: $(-2)^3 = -8$.

That is why $(-1)^n$ is $1$ when $n$ is even and $-1$ when it is odd; it
is often used in mathematics to alternate signs.

## Order of operations with negatives

The rule does not change; just watch the signs:

$$
\begin{aligned}
-8 + 3 \cdot (-2) - (-5) &= -8 + (-6) + 5 \\
&= -14 + 5 = -9
\end{aligned}
$$

The steps: the multiplication ($3 \cdot (-2) = -6$), turn subtracting a
negative into addition ($-(-5) = +5$), then add left to right.

## Negative numbers in machine learning

**Error.** A model's error is often the true value minus the prediction:
$e = y - \hat{y}$. If the model predicted too high, the error is
negative; too low, and it is positive. True value $20$, prediction $23$:
$e = 20 - 23 = -3$.

**Errors can cancel out.** A model with errors $-3, 2, 4, -3$ has an
error sum of $0$, yet it did not get a single prediction right! That is
why errors are added either as absolute values ($|{-3}| + |2| + |4| +
|{-3}| = 12$) or as squares. The square of a negative number is positive,
so squares do not cancel either.

**Direction.** Model training has rules like "if the slope is negative,
increase the weight; if positive, decrease it": a number's sign carries
**direction** information.

## Common mistakes

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Wrong</h4>
      <p>$-5 > -2$</p>
      <p>$-2^2 = 4$</p>
      <p>$5 - (-3) = 2$</p>
      <p>$(-4)(-5) = -20$</p>
    </div>
    <div class="ok">
      <h4>Right</h4>
      <p>$-5 < -2$ (further left)</p>
      <p>$-2^2 = -4$, but $(-2)^2 = 4$</p>
      <p>$5 - (-3) = 5 + 3 = 8$</p>
      <p>$(-4)(-5) = 20$</p>
    </div>
  </div>
  <figcaption>With negatives, most mistakes come from signs and brackets.</figcaption>
</figure>

- **Applying "two minuses make a plus" to addition.** $-3 + (-4)$ is not
  $7$ but $-7$: when two numbers with the same sign are added, the sign
  is kept. "Minus times minus is plus" is only for multiplication and
  division.
- **Treating absolute value as "delete the minus" inside an expression.**
  $|3 - 8| = \lvert -5 \rvert = 5$; work out the inside first, then take the absolute
  value. $|3| - |8| = -5$ is something else.

## Summary

- Integers: $\dots, -2, -1, 0, 1, 2, \dots$; on the number line, further right is larger.
- Opposite: $a + (-a) = 0$; $-(-a) = a$.
- Absolute value is distance from zero: $|a| \ge 0$; the distance between $a$ and $b$ is $|a - b|$.
- Addition: same sign → add, keep the sign; different signs → subtract, sign of the larger.
- Subtraction is adding the opposite: $a - b = a + (-b)$.
- Multiplication and division: same signs $+$, different signs $-$; with many factors, count the minuses.
- $(-2)^2 = 4$ but $-2^2 = -4$; an even power of a negative is positive, an odd power negative.
- Errors carry a sign; to stop them cancelling when added, take absolute values or squares.
