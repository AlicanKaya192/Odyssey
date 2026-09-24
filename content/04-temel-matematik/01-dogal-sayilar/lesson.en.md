# Natural Numbers and Order of Operations

The numbers we learned to count with are the foundation of mathematics:
$0, 1, 2, 3, \dots$ In this section we look at them once more, this time
asking "why is it like this?": how we write numbers (place value), the
rules of the four operations, division with remainder and, most
importantly, the **order of operations**: which operation is done first in
an expression.

The order of operations looks like a small rule, but it matters a lot. If
two people calculate the same expression in different orders they get two
different results; the rule makes sure everyone gets the same one.
Computers and calculators follow this rule too.

Prerequisite: the Reading Mathematics section.

## Writing numbers: place value

With ten **digits** ($0, 1, 2, \dots, 9$) we can write infinitely many
**numbers**. The idea that makes this possible is **place value**: a
digit's value depends on **where it stands** in the number.

<figure class="fig">
<svg viewBox="0 0 420 154" width="420"><rect class="box" x="14" y="58" width="56" height="48"/><text class="ink" x="42.0" y="91" font-size="24" text-anchor="middle">3</text><text class="dim" x="42.0" y="49" font-size="10" text-anchor="middle">millions</text><rect class="box" x="70" y="58" width="56" height="48"/><text class="ink" x="98.0" y="91" font-size="24" text-anchor="middle">7</text><text class="dim" x="98.0" y="36" font-size="10" text-anchor="middle">hundred</text><text class="dim" x="98.0" y="49" font-size="10" text-anchor="middle">thousands</text><rect class="box" x="126" y="58" width="56" height="48"/><text class="ink" x="154.0" y="91" font-size="24" text-anchor="middle">0</text><text class="dim" x="154.0" y="36" font-size="10" text-anchor="middle">ten</text><text class="dim" x="154.0" y="49" font-size="10" text-anchor="middle">thousands</text><rect class="box" x="182" y="58" width="56" height="48"/><text class="ink" x="210.0" y="91" font-size="24" text-anchor="middle">5</text><text class="dim" x="210.0" y="49" font-size="10" text-anchor="middle">thousands</text><rect class="box" x="238" y="58" width="56" height="48"/><text class="ink" x="266.0" y="91" font-size="24" text-anchor="middle">8</text><text class="dim" x="266.0" y="49" font-size="10" text-anchor="middle">hundreds</text><rect class="box" x="294" y="58" width="56" height="48"/><text class="ink" x="322.0" y="91" font-size="24" text-anchor="middle">1</text><text class="dim" x="322.0" y="49" font-size="10" text-anchor="middle">tens</text><rect class="box" x="350" y="58" width="56" height="48"/><text class="ink" x="378.0" y="91" font-size="24" text-anchor="middle">2</text><text class="dim" x="378.0" y="49" font-size="10" text-anchor="middle">ones</text><rect class="curve" x="67" y="55" width="62" height="54" rx="4"/><text class="ink" x="210.0" y="140" font-size="12" text-anchor="middle">The place value of 7: 7 × 100 000 = 700 000</text></svg>
  <figcaption>In the number $3\,705\,812$ every digit has a place. The 7 is in the hundred thousands place, so its value is not 7 but 700 000. The 0 says there is nothing in that place, but it holds the position.</figcaption>
</figure>

Each place is **10 times** the one to its right. That is why our system is
called the **decimal system**. A number is its digits multiplied by their
place values and added up:

$$
3\,705\,812 = 3 \cdot 1\,000\,000 + 7 \cdot 100\,000 + 0 \cdot 10\,000 + 5 \cdot 1\,000 + 8 \cdot 100 + 1 \cdot 10 + 2
$$

**Digit versus number:** $7$ is a digit and also a number; $705$ is a
number made of three digits. "How many digits?" asks how many digits the
number is written with: $3\,705\,812$ has seven digits.

**The job of zero:** $705$ and $75$ are different numbers. The $0$ in
$705$ says the tens place is empty and keeps the $7$ in the hundreds
place. Without zero we could not tell these two numbers apart in writing.

**Reading large numbers:** group the digits in threes from the right:
$3\,705\,812$ is "three million seven hundred five thousand eight hundred
twelve". In this course the groups are separated by a small space;
English also uses commas ($3{,}705{,}812$) and Turkish uses dots
($3.705.812$).

## The four operations and their names

| Operation | Parts | Example |
|---|---|---|
| Addition | addend $+$ addend $=$ **sum** | $8 + 5 = 13$ |
| Subtraction | minuend $-$ subtrahend $=$ **difference** | $13 - 5 = 8$ |
| Multiplication | factor $\times$ factor $=$ **product** | $4 \cdot 6 = 24$ |
| Division | dividend $\div$ divisor $=$ **quotient** | $24 \div 6 = 4$ |

Multiplication is **repeated addition**: $4 \cdot 6 = 6 + 6 + 6 + 6$.
Division is the reverse of multiplication: $24 \div 6$ asks "which number
times $6$ gives $24$?".

## Properties of the operations

These properties are the source of calculation shortcuts and the rules we
will use constantly when working with letters in algebra.

| Property | Rule | Example |
|---|---|---|
| Commutative | $a + b = b + a$ and $a \cdot b = b \cdot a$ | $7 \cdot 4 = 4 \cdot 7$ |
| Associative | $(a + b) + c = a + (b + c)$, $(ab)c = a(bc)$ | $(25 \cdot 4) \cdot 7 = 25 \cdot (4 \cdot 7)$ |
| Distributive | $a(b + c) = ab + ac$ | $7 \cdot 13 = 7 \cdot 10 + 7 \cdot 3$ |
| Identity | $a + 0 = a$, $a \cdot 1 = a$ | $58 \cdot 1 = 58$ |
| Zero product | $a \cdot 0 = 0$ | $1\,000 \cdot 0 = 0$ |

**Subtraction and division are not commutative:** $8 - 5 = 3$ but $5 - 8
= -3$; $12 \div 4 = 3$ but $4 \div 12 = \tfrac{1}{3}$. They are not
associative either: $(12 - 5) - 2 = 5$ but $12 - (5 - 2) = 9$.

### Why is the distributive property true?

<figure class="fig">
<svg viewBox="0 0 380 212" width="380"><rect class="dot" opacity="0.22" x="60" y="30" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="60" y="50" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="60" y="70" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="60" y="90" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="60" y="110" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="60" y="130" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="60" y="150" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="80" y="30" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="80" y="50" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="80" y="70" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="80" y="90" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="80" y="110" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="80" y="130" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="80" y="150" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="100" y="30" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="100" y="50" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="100" y="70" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="100" y="90" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="100" y="110" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="100" y="130" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="100" y="150" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="120" y="30" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="120" y="50" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="120" y="70" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="120" y="90" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="120" y="110" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="120" y="130" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="120" y="150" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="140" y="30" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="140" y="50" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="140" y="70" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="140" y="90" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="140" y="110" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="140" y="130" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="140" y="150" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="160" y="30" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="160" y="50" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="160" y="70" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="160" y="90" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="160" y="110" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="160" y="130" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="160" y="150" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="180" y="30" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="180" y="50" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="180" y="70" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="180" y="90" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="180" y="110" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="180" y="130" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="180" y="150" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="200" y="30" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="200" y="50" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="200" y="70" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="200" y="90" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="200" y="110" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="200" y="130" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="200" y="150" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="220" y="30" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="220" y="50" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="220" y="70" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="220" y="90" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="220" y="110" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="220" y="130" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="220" y="150" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="240" y="30" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="240" y="50" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="240" y="70" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="240" y="90" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="240" y="110" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="240" y="130" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="240" y="150" width="18" height="18" rx="2"/><rect class="dot2" opacity="0.22" x="260" y="30" width="18" height="18" rx="2"/><rect class="dot2" opacity="0.22" x="260" y="50" width="18" height="18" rx="2"/><rect class="dot2" opacity="0.22" x="260" y="70" width="18" height="18" rx="2"/><rect class="dot2" opacity="0.22" x="260" y="90" width="18" height="18" rx="2"/><rect class="dot2" opacity="0.22" x="260" y="110" width="18" height="18" rx="2"/><rect class="dot2" opacity="0.22" x="260" y="130" width="18" height="18" rx="2"/><rect class="dot2" opacity="0.22" x="260" y="150" width="18" height="18" rx="2"/><rect class="dot2" opacity="0.22" x="280" y="30" width="18" height="18" rx="2"/><rect class="dot2" opacity="0.22" x="280" y="50" width="18" height="18" rx="2"/><rect class="dot2" opacity="0.22" x="280" y="70" width="18" height="18" rx="2"/><rect class="dot2" opacity="0.22" x="280" y="90" width="18" height="18" rx="2"/><rect class="dot2" opacity="0.22" x="280" y="110" width="18" height="18" rx="2"/><rect class="dot2" opacity="0.22" x="280" y="130" width="18" height="18" rx="2"/><rect class="dot2" opacity="0.22" x="280" y="150" width="18" height="18" rx="2"/><rect class="dot2" opacity="0.22" x="300" y="30" width="18" height="18" rx="2"/><rect class="dot2" opacity="0.22" x="300" y="50" width="18" height="18" rx="2"/><rect class="dot2" opacity="0.22" x="300" y="70" width="18" height="18" rx="2"/><rect class="dot2" opacity="0.22" x="300" y="90" width="18" height="18" rx="2"/><rect class="dot2" opacity="0.22" x="300" y="110" width="18" height="18" rx="2"/><rect class="dot2" opacity="0.22" x="300" y="130" width="18" height="18" rx="2"/><rect class="dot2" opacity="0.22" x="300" y="150" width="18" height="18" rx="2"/><rect class="curve" x="57" y="27" width="202" height="144" rx="4"/><rect class="curve2" x="259" y="27" width="62" height="144" rx="4"/><text class="ink" x="160" y="106.0" font-size="14" text-anchor="middle">7 × 10 = 70</text><text class="ink" x="290.0" y="106.0" font-size="14" text-anchor="middle">21</text><text class="ink" x="46" y="105.0" font-size="14" text-anchor="middle">7</text><text class="ink" x="160" y="18" font-size="13" text-anchor="middle">10</text><text class="ink" x="290.0" y="18" font-size="13" text-anchor="middle">3</text><text class="ink" x="190.0" y="198" font-size="13" text-anchor="middle">7 × 13 = 7 × 10 + 7 × 3 = 70 + 21 = 91</text></svg>
  <figcaption>A rectangle with $7$ rows and $13$ columns has $7 \cdot 13$ squares. Splitting it into parts of $10$ and $3$ columns gives $7 \cdot 10 = 70$ purple and $7 \cdot 3 = 21$ orange squares: $91$ in total.</figcaption>
</figure>

The distributive property is the most powerful tool of mental arithmetic:

$$
\begin{aligned}
99 \cdot 7 &= (100 - 1) \cdot 7 = 700 - 7 = 693 \\
25 \cdot 44 &= 25 \cdot 4 \cdot 11 = 100 \cdot 11 = 1\,100 \\
38 \cdot 25 + 62 \cdot 25 &= (38 + 62) \cdot 25 = 100 \cdot 25 = 2\,500
\end{aligned}
$$

In the last line we used the property **backwards**: we took the common
factor ($25$) out. In algebra this will be called **factoring out**.

### Division by zero is undefined

What could $12 \div 0$ be? Division was the reverse of multiplication:
"which number times $0$ gives $12$?" None; every number times $0$ is $0$.
That is why division by zero is **undefined**: it has no result. $0 \div
12 = 0$ is fine: $0 \cdot 12 = 0$.

## Division with remainder

Not every division comes out exactly. Sharing $1\,000$ pens equally among
$37$ students gives each $27$ pens with $1$ pen left over:

$$
1\,000 = 37 \cdot 27 + 1
$$

In general, dividing $a$ by $b$ means writing $a$ as:

$$
a = b \cdot q + r, \qquad 0 \le r < b
$$

$q$ is the **quotient**, $r$ the **remainder**. The remainder is always
smaller than the divisor; otherwise we could divide once more.

**Check:** Multiply the quotient by the divisor and add the remainder;
you must get the dividend: $37 \cdot 27 + 1 = 999 + 1 = 1\,000$ ✓.

Remainders come up often in daily life: which day of the week is it $100$
days from now? $100 = 7 \cdot 14 + 2$: $14$ whole weeks and $2$ days. If
today is Monday, in $100$ days it is Wednesday.

## Order of operations

What is the value of this expression?

$$
2 + 3 \cdot 4
$$

Going left to right gives $5 \cdot 4 = 20$; multiplying first gives $2 +
12 = 14$. Both cannot be right; mathematics has settled on a rule:
**multiplication before addition**. The correct answer is $14$.

The whole rule in four steps:

<figure class="fig">
  <div class="flow">
    <span class="node acc"><b>1. Brackets</b><br>inside out</span>
    <span class="arrow">→</span>
    <span class="node"><b>2. Exponents</b><br>and roots</span>
    <span class="arrow">→</span>
    <span class="node"><b>3. Multiply, divide</b><br>left to right</span>
    <span class="arrow">→</span>
    <span class="node"><b>4. Add, subtract</b><br>left to right</span>
  </div>
  <figcaption>First the inside of brackets, then exponents, then multiplication and division, and finally addition and subtraction. Operations on the same step (multiplication with division, addition with subtraction) are done in order from left to right.</figcaption>
</figure>

An **exponent** is repeated multiplication: $4^2 = 4 \cdot 4 = 16$, $2^3
= 2 \cdot 2 \cdot 2 = 8$. We will study them in the Exponents section;
here knowing their priority is enough.

### Examples

**Multiplication before addition:**

$$
2 + 3 \cdot 4^2 = 2 + 3 \cdot 16 = 2 + 48 = 50
$$

First the exponent ($4^2 = 16$), then the multiplication, finally the
addition.

**Multiplication and division have equal priority: left to right.**

$$
8 \div 2 \cdot 4 = 4 \cdot 4 = 16
$$

It is **not** $8 \div (2 \cdot 4) = 1$. There is no rule "multiplication
before division"; both are on the same step and done left to right.

**Addition and subtraction are also left to right.**

$$
10 - 4 + 3 = 6 + 3 = 9
$$

It is **not** $10 - (4 + 3) = 3$.

**Brackets change everything:**

$$
18 - 2 \cdot (3 + 4) + 12 \div 3 = 18 - 2 \cdot 7 + 4 = 18 - 14 + 4 = 8
$$

Step by step: the bracket ($3 + 4 = 7$), multiplication and division
($2 \cdot 7 = 14$, $12 \div 3 = 4$), and finally addition and subtraction
left to right.

**Nested brackets: inside out.**

$$
\begin{aligned}
5 \cdot [20 - (2 + 3) \cdot 3] &= 5 \cdot [20 - 5 \cdot 3] \\
&= 5 \cdot [20 - 15] \\
&= 5 \cdot 5 = 25
\end{aligned}
$$

### Splitting into terms: a safe method

In a long expression, first split at the **$+$ and $-$ signs outside the
brackets**. Work out each piece (term) separately, then add:

$$
\underbrace{18}_{18} \; - \; \underbrace{2 \cdot (3 + 4)}_{14} \; + \; \underbrace{12 \div 3}_{4} = 18 - 14 + 4 = 8
$$

This method applies the order of operations automatically, because
multiplication and division always stay inside one term.

## Estimation and rounding

To tell whether a result is **reasonable**, round the numbers and
calculate roughly. The rough value of $38 \cdot 51$ is $40 \cdot 50 =
2\,000$; the true result is $1\,938$. Had you got $19\,380$ or $193$, you
would know at once that you had made a mistake.

Rounding whole numbers to the nearest ten or hundred: $738 \approx 740$
(nearest ten), $738 \approx 700$ (nearest hundred). If the next digit is
$5$ or more, round up; otherwise round down. We will round decimals in
their own section.

## Natural numbers in machine learning

**Counting parameters.** If a neural network layer connects $784$ inputs
to $128$ neurons, it has $784 \cdot 128$ weights plus one constant per
neuron, so $128$ constant terms:

$$
784 \cdot 128 + 128 = 100\,352 + 128 = 100\,480
$$

Shorter with the distributive property: $128 \cdot (784 + 1) = 128 \cdot
785$. In large language models this number reaches billions.

**Division with remainder and batches.** If a data set of $10\,000$
examples is processed in batches of $32$:

$$
10\,000 = 32 \cdot 312 + 16
$$

There are $312$ full batches and a last batch of $16$ examples; one pass
(epoch) takes $313$ steps.

## Common mistakes

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Wrong</h4>
      <p>$2 + 3 \cdot 4 = 20$</p>
      <p>$8 \div 2 \cdot 4 = 1$</p>
      <p>$10 - 4 + 3 = 3$</p>
      <p>$12 \div 0 = 0$</p>
    </div>
    <div class="ok">
      <h4>Right</h4>
      <p>Multiply first: $2 + 12 = 14$</p>
      <p>Left to right: $4 \cdot 4 = 16$</p>
      <p>Left to right: $6 + 3 = 9$</p>
      <p>Division by zero is undefined</p>
    </div>
  </div>
  <figcaption>Operations on the same step always go from left to right.</figcaption>
</figure>

- **Thinking "multiplication before division, addition before
  subtraction".** Each pair has equal priority and is done left to right.
- **Leaving a remainder larger than the divisor.** For $50 \div 7$,
  "quotient 6, remainder 8" is wrong; $8 \ge 7$, so divide once more:
  quotient $7$, remainder $1$.
- **Mixing up place value.** The $7$ in $3\,705\,812$ is worth
  $700\,000$, not $7\,000$.

## Summary

- Decimal system: each place is 10 times the one to its right; a digit's value depends on its place.
- Sum, difference, product, quotient; multiplication is repeated addition, division reverses multiplication.
- Commutative and associative for addition and multiplication, not for subtraction and division.
- Distributive: $a(b + c) = ab + ac$; the basis of mental arithmetic and factoring out.
- Division by zero is undefined; $0 \div a = 0$.
- Division with remainder: $a = bq + r$, $0 \le r < b$; check with $bq + r$.
- Order of operations: brackets → exponents → multiply/divide (left to right) → add/subtract (left to right).
- Split long expressions into terms at the $+$ and $-$ outside brackets.
- Compare the result with a rough estimate.
