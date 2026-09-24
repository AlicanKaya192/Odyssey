# Exponents

Multiplication was repeated addition. An **exponent** is repeated
multiplication: instead of $2 \cdot 2 \cdot 2 \cdot 2 \cdot 2$ we write
$2^5$. Exponents are the language for writing very large and very small
numbers, and for describing growth that "doubles at every step". A
language model's $10^{11}$ parameters, a learning rate of $10^{-3}$, a
byte that can hold $2^8 = 256$ values: all are described with exponents.

Prerequisite: the Integers and Fractions sections.

## What is an exponent?

If $n$ is a positive whole number,

$$
a^n = \underbrace{a \cdot a \cdot \ldots \cdot a}_{n \text{ times}}
$$

$a$ is called the **base** and $n$ the **exponent**; $a^n$ is read "$a$ to
the power $n$". $a^2$ is "$a$ squared", $a^3$ "$a$ cubed".

$$
2^5 = 32, \qquad 10^3 = 1\,000, \qquad \left(\frac{2}{3}\right)^2 = \frac{4}{9}, \qquad (-3)^3 = -27
$$

### Exponential growth is very fast

<figure class="fig">
<svg viewBox="0 0 440 228" width="440"><rect class="dot" opacity="0.5" x="40" y="198.8" width="34" height="1.2" rx="3"/><text class="ink" x="57.0" y="192.8" font-size="11" text-anchor="middle">1</text><text class="dim" x="57.0" y="216" font-size="11" text-anchor="middle">0</text><circle class="dot2" cx="57.0" cy="200.0" r="4"/><rect class="dot" opacity="0.5" x="88" y="197.5" width="34" height="2.5" rx="3"/><text class="ink" x="105.0" y="191.5" font-size="11" text-anchor="middle">2</text><text class="dim" x="105.0" y="216" font-size="11" text-anchor="middle">1</text><circle class="dot2" cx="105.0" cy="197.5" r="4"/><rect class="dot" opacity="0.5" x="136" y="195.0" width="34" height="5.0" rx="3"/><text class="ink" x="153.0" y="189.0" font-size="11" text-anchor="middle">4</text><text class="dim" x="153.0" y="216" font-size="11" text-anchor="middle">2</text><circle class="dot2" cx="153.0" cy="195.0" r="4"/><rect class="dot" opacity="0.5" x="184" y="190.0" width="34" height="10.0" rx="3"/><text class="ink" x="201.0" y="184.0" font-size="11" text-anchor="middle">8</text><text class="dim" x="201.0" y="216" font-size="11" text-anchor="middle">3</text><circle class="dot2" cx="201.0" cy="192.5" r="4"/><rect class="dot" opacity="0.5" x="232" y="180.0" width="34" height="20.0" rx="3"/><text class="ink" x="249.0" y="174.0" font-size="11" text-anchor="middle">16</text><text class="dim" x="249.0" y="216" font-size="11" text-anchor="middle">4</text><circle class="dot2" cx="249.0" cy="190.0" r="4"/><rect class="dot" opacity="0.5" x="280" y="160.0" width="34" height="40.0" rx="3"/><text class="ink" x="297.0" y="154.0" font-size="11" text-anchor="middle">32</text><text class="dim" x="297.0" y="216" font-size="11" text-anchor="middle">5</text><circle class="dot2" cx="297.0" cy="187.5" r="4"/><rect class="dot" opacity="0.5" x="328" y="120.0" width="34" height="80.0" rx="3"/><text class="ink" x="345.0" y="114.0" font-size="11" text-anchor="middle">64</text><text class="dim" x="345.0" y="216" font-size="11" text-anchor="middle">6</text><circle class="dot2" cx="345.0" cy="185.0" r="4"/><rect class="dot" opacity="0.5" x="376" y="40.0" width="34" height="160.0" rx="3"/><text class="ink" x="393.0" y="34.0" font-size="11" text-anchor="middle">128</text><text class="dim" x="393.0" y="216" font-size="11" text-anchor="middle">7</text><circle class="dot2" cx="393.0" cy="182.5" r="4"/><polyline class="curve2" fill="none" points="57.0,200.0 105.0,197.5 153.0,195.0 201.0,192.5 249.0,190.0 297.0,187.5 345.0,185.0 393.0,182.5"/><line class="line" x1="32" y1="200" x2="424" y2="200"/><text class="dim" x="428" y="216" font-size="11" text-anchor="start">n</text><rect class="dot" opacity="0.5" x="40" y="14" width="12" height="12" rx="2"/><text class="ink" x="58" y="24" font-size="12" text-anchor="start">2ⁿ: doubles at each step</text><circle class="dot2" cx="46" cy="42" r="4"/><text class="ink" x="58" y="46" font-size="12" text-anchor="start">2n: adds 2 at each step</text></svg>
  <figcaption>The purple bars are $2^n$: they double at each step. The orange line is $2n$: it grows by $2$ at each step. At $n = 7$ one is $128$ and the other $14$. At first there seems to be no difference, but doubling soon leaves any addition behind.</figcaption>
</figure>

$2^{10} = 1\,024 \approx 10^3$. That is why $1$ kilobyte on a computer is
roughly $1\,000$ bytes. $2^{20} \approx 10^6$, $2^{30} \approx 10^9$.

## The exponent rules

Instead of memorising the rules you can see each one by writing it out;
they all come from the definition.

**Multiplying with the same base: add the exponents.**

$$
a^m \cdot a^n = a^{m + n} \qquad 2^3 \cdot 2^4 = (2 \cdot 2 \cdot 2)(2 \cdot 2 \cdot 2 \cdot 2) = 2^7
$$

**Dividing with the same base: subtract the exponents.**

$$
\frac{a^m}{a^n} = a^{m - n} \qquad \frac{2^5}{2^2} = \frac{2 \cdot 2 \cdot 2 \cdot \cancel{2} \cdot \cancel{2}}{\cancel{2} \cdot \cancel{2}} = 2^3
$$

**A power of a power: multiply the exponents.**

$$
(a^m)^n = a^{m \cdot n} \qquad (2^3)^2 = 2^3 \cdot 2^3 = 2^6
$$

**A power of a product or quotient: it spreads over each factor.**

$$
(ab)^n = a^n b^n, \qquad \left(\frac{a}{b}\right)^n = \frac{a^n}{b^n}
$$

$(2 \cdot 5)^3 = 2^3 \cdot 5^3 = 8 \cdot 125 = 1\,000$; indeed $10^3$.

**A power of a sum does not spread!** $(a + b)^2 \neq a^2 + b^2$. For
example $(1 + 2)^2 = 9$ but $1^2 + 2^2 = 5$. The rule is only for
multiplication and division.

## Zero and negative exponents

If an exponent only meant "how many times we multiplied", $2^0$ or
$2^{-1}$ would be meaningless. But for the rules to keep working, the
values of these exponents are fixed **automatically**.

<figure class="fig">
<svg viewBox="0 0 542 126" width="542"><rect class="box" x="14" y="30" width="58" height="58" rx="6"/><text class="ink" x="43.0" y="54" font-size="16" text-anchor="middle">2³</text><text class="ink" x="43.0" y="76" font-size="14" text-anchor="middle">8</text><text class="dim" x="87.0" y="52" font-size="12" text-anchor="middle">÷2</text><text class="dim" x="87.0" y="68" font-size="14" text-anchor="middle">→</text><rect class="box" x="102" y="30" width="58" height="58" rx="6"/><text class="ink" x="131.0" y="54" font-size="16" text-anchor="middle">2²</text><text class="ink" x="131.0" y="76" font-size="14" text-anchor="middle">4</text><text class="dim" x="175.0" y="52" font-size="12" text-anchor="middle">÷2</text><text class="dim" x="175.0" y="68" font-size="14" text-anchor="middle">→</text><rect class="box" x="190" y="30" width="58" height="58" rx="6"/><text class="ink" x="219.0" y="54" font-size="16" text-anchor="middle">2¹</text><text class="ink" x="219.0" y="76" font-size="14" text-anchor="middle">2</text><text class="dim" x="263.0" y="52" font-size="12" text-anchor="middle">÷2</text><text class="dim" x="263.0" y="68" font-size="14" text-anchor="middle">→</text><rect class="box" x="278" y="30" width="58" height="58" rx="6"/><rect class="curve" x="278" y="30" width="58" height="58" rx="6"/><text class="ink" x="307.0" y="54" font-size="16" text-anchor="middle">2⁰</text><text class="ink" x="307.0" y="76" font-size="14" text-anchor="middle">1</text><text class="dim" x="351.0" y="52" font-size="12" text-anchor="middle">÷2</text><text class="dim" x="351.0" y="68" font-size="14" text-anchor="middle">→</text><rect class="box" x="366" y="30" width="58" height="58" rx="6"/><text class="ink" x="395.0" y="54" font-size="16" text-anchor="middle">2⁻¹</text><text class="ink" x="395.0" y="76" font-size="14" text-anchor="middle">1/2</text><text class="dim" x="439.0" y="52" font-size="12" text-anchor="middle">÷2</text><text class="dim" x="439.0" y="68" font-size="14" text-anchor="middle">→</text><rect class="box" x="454" y="30" width="58" height="58" rx="6"/><text class="ink" x="483.0" y="54" font-size="16" text-anchor="middle">2⁻²</text><text class="ink" x="483.0" y="76" font-size="14" text-anchor="middle">1/4</text><text class="ink" x="263.0" y="114" font-size="12" text-anchor="middle">each time the exponent drops by 1, the value halves</text></svg>
  <figcaption>Each time the exponent drops by $1$, the value halves. Continuing the pattern gives $2^0 = 1$, $2^{-1} = \tfrac{1}{2}$, $2^{-2} = \tfrac{1}{4}$. The definitions are not arbitrary; they continue the pattern.</figcaption>
</figure>

**The zeroth power.** From the division rule: $\dfrac{a^n}{a^n} = a^{n -
n} = a^0$. But a number divided by itself is $1$. So

$$
a^0 = 1 \qquad (a \neq 0)
$$

**A negative exponent.** Again from the division rule: $\dfrac{a^0}{a^n}
= a^{0 - n} = a^{-n}$, and that is $\dfrac{1}{a^n}$:

$$
a^{-n} = \frac{1}{a^n} \qquad 2^{-3} = \frac{1}{8}, \qquad 10^{-2} = \frac{1}{100} = 0.01
$$

**A negative exponent does not make the number negative;** it takes the
reciprocal. $2^{-3}$ is a positive number: $\tfrac{1}{8}$.

For fractions, a negative exponent flips the fraction:

$$
\left(\frac{2}{3}\right)^{-2} = \left(\frac{3}{2}\right)^2 = \frac{9}{4}
$$

All the rules hold for zero and negative exponents too:

$$
\frac{2^3 \cdot 2^5}{2^{10}} = \frac{2^8}{2^{10}} = 2^{-2} = \frac{1}{4}
$$

## Making different bases the same

If the bases differ, the rules cannot be applied directly: $2^3 \cdot
3^2$ does not combine. But if the bases are powers of the same number,
convert them to the same base first:

$$
\frac{4^3 \cdot 8^2}{2^{10}} = \frac{(2^2)^3 \cdot (2^3)^2}{2^{10}} = \frac{2^6 \cdot 2^6}{2^{10}} = 2^{2} = 4
$$

**Simple exponential equations** are solved the same way: if $2^x = 32$,
write $32 = 2^5$ and get $x = 5$. With the same base, the exponents must
be equal.

## Negative bases and brackets

Remember from the Integers section: the brackets decide the base.

$$
(-2)^4 = 16, \qquad -2^4 = -16, \qquad (-2)^3 = -8
$$

An even power of a negative base is positive, an odd power negative.

## Scientific notation

Very large and very small numbers are written in the form $a \times
10^n$, where $1 \le a < 10$ and $n$ is a whole number.

| Number | Scientific notation |
|---|---|
| $300\,000$ | $3 \times 10^5$ |
| $175\,000\,000\,000$ | $1.75 \times 10^{11}$ |
| $0.004$ | $4 \times 10^{-3}$ |
| $0.000\,025$ | $2.5 \times 10^{-5}$ |

$n$ says how many places the point has moved: positive for a large
number, negative for a number less than $1$.

**Multiplying and dividing in scientific notation:** handle the
coefficients and the powers of $10$ separately.

$$
(3 \times 10^4)(2 \times 10^{-7}) = (3 \cdot 2) \times 10^{4 + (-7)} = 6 \times 10^{-3}
$$

If the coefficient goes past $10$, fix it: $(5 \times 10^3)(4 \times
10^2) = 20 \times 10^5 = 2 \times 10^6$.

**On a computer**, $6 \times 10^{-3}$ is usually written `6e-3`; in Python
`0.006 == 6e-3` is true.

## Exponents in machine learning

**Small values** such as a learning rate are usually chosen as negative
powers of $10$: $10^{-2}$, $10^{-3}$, $10^{-4}$. Trying them, each step
makes the value $10$ times smaller.

**Model size** is described in scientific notation: $1.75 \times 10^{11}$
parameters, that is, $175$ billion.

**Binary.** $8$ bits can hold $2^8 = 256$ different values; each pixel of
an image is often a number from $0$ to $255$.

**Number of trials.** Trying $3$ values for each of $5$ settings and
training every combination means training $3^5 = 243$ models. With $10$
settings it becomes $3^{10} = 59\,049$; that is why trying every
combination is often impossible.

## Common mistakes

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Wrong</h4>
      <p>$2^3 \cdot 2^4 = 4^7$</p>
      <p>$(2^3)^2 = 2^9$</p>
      <p>$2^{-3} = -8$</p>
      <p>$(a + b)^2 = a^2 + b^2$</p>
      <p>$3^0 = 0$</p>
    </div>
    <div class="ok">
      <h4>Right</h4>
      <p>$2^3 \cdot 2^4 = 2^7$ (the base stays)</p>
      <p>$(2^3)^2 = 2^6$ (exponents multiply)</p>
      <p>$2^{-3} = \dfrac{1}{8}$</p>
      <p>$(1 + 2)^2 = 9 \neq 5$</p>
      <p>$3^0 = 1$</p>
    </div>
  </div>
  <figcaption>In multiplication the exponents add and the base stays; in a power of a power the exponents multiply.</figcaption>
</figure>

- **Multiplying the bases.** In $2^3 \cdot 2^4$ the base stays $2$; bases
  are not multiplied.
- **Applying exponent rules to addition.** $2^3 + 2^4 \neq 2^7$: $8 + 16 =
  24$. The rules are only for multiplication and division. (But $2^3 +
  2^3 = 2 \cdot 2^3 = 2^4$, because we add the same thing twice.)
- **Thinking a negative exponent means a negative number.** A negative
  exponent takes the reciprocal.

## Summary

- $a^n$: multiply $a$ by itself $n$ times. Base $a$, exponent $n$.
- $a^m a^n = a^{m+n}$, $\dfrac{a^m}{a^n} = a^{m-n}$, $(a^m)^n = a^{mn}$, $(ab)^n = a^n b^n$.
- $a^0 = 1$, $a^{-n} = \dfrac{1}{a^n}$ ($a \neq 0$); a negative exponent takes the reciprocal, it does not change the sign.
- A power of a sum does not spread: $(a + b)^2 \neq a^2 + b^2$.
- Convert different bases to the same base where possible: $4 = 2^2$, $8 = 2^3$.
- Scientific notation: $a \times 10^n$, $1 \le a < 10$; handle coefficients and powers of $10$ separately.
- $2^{10} \approx 10^3$; exponential growth soon overtakes any linear growth.
