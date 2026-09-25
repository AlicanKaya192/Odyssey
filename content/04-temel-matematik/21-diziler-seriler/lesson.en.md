# Sequences, Series and Sigma Notation

A **sequence** is numbers in order: $2, 4, 6, 8, \dots$ A **series** is
their sum: $2 + 4 + 6 + 8 + \dots$ Long sums are written briefly with the
capital Greek letter sigma, $\Sigma$. Machine learning formulas are full of
Σ: the mean, the loss function, the product of two vectors and the
denominator of softmax are all sums. In this section we will see
sequences, two important kinds (arithmetic and geometric), how to read and
write Σ notation, and how sums are computed by shortcuts. We will also see
that the sum of infinitely many numbers can be a finite number.

Prerequisites: Natural Numbers and Order of Operations, Functions,
Exponential Functions and Growth.

## What is a sequence?

A sequence is a function that assigns a number to each natural number: the
1st term, the 2nd term, the 3rd term… The $n$th term is written $a_n$; the
small $n$ is called the **index**.

A sequence can be given in two ways:

- **By a general term:** if $a_n = 2n + 1$, then $a_1 = 3$, $a_2 = 5$,
  $a_{10} = 21$. You can go straight to any term.
- **From the previous one (recursively):** $a_1 = 3$ and
  $a_{n+1} = a_n + 2$. The same sequence, but for $a_{10}$ you need the
  nine terms before it.

A famous recursive sequence is **Fibonacci**: $F_1 = F_2 = 1$ and each term
is the sum of the two before it, $F_{n+2} = F_{n+1} + F_n$. The terms are
$1, 1, 2, 3, 5, 8, 13, 21, \dots$

## Arithmetic sequences

Each term is found by **adding the same number** to the previous one. This
number is called the **common difference** and written $d$.

$$
a_n = a_1 + (n - 1) d
$$

In $5, 8, 11, 14, \dots$, $a_1 = 5$ and $d = 3$. The twentieth term:
$a_{20} = 5 + 19 \cdot 3 = 62$. From the first term to the twentieth there
are $19$ steps, not $20$; that is why the formula has $(n - 1)$.

**From two terms.** If $a_4 = 17$ and $a_{10} = 41$, it grew by $24$ over
the $6$ steps between: $d = \frac{24}{6} = 4$. Going back,
$a_1 = 17 - 3 \cdot 4 = 5$.

An arithmetic sequence is the values of a **line** from The Coordinate
Plane and Lines at whole numbers: $a_n = dn + (a_1 - d)$, with slope $d$.

## Geometric sequences

Each term is found by **multiplying the previous one by the same number**.
This number is called the **common ratio** and written $r$.

$$
a_n = a_1 \cdot r^{n - 1}
$$

In $3, 6, 12, 24, \dots$, $a_1 = 3$ and $r = 2$. The eighth term:
$a_8 = 3 \cdot 2^7 = 384$. A geometric sequence is the values of the
**exponential function** of the previous section at whole numbers.

<figure class="fig">
<svg viewBox="0 0 440 244" width="440"><line class="grid" x1="40.0" y1="230.0" x2="40.0" y2="20.0"/><line class="grid" x1="80.0" y1="230.0" x2="80.0" y2="20.0"/><line class="grid" x1="120.0" y1="230.0" x2="120.0" y2="20.0"/><line class="grid" x1="160.0" y1="230.0" x2="160.0" y2="20.0"/><line class="grid" x1="200.0" y1="230.0" x2="200.0" y2="20.0"/><line class="grid" x1="240.0" y1="230.0" x2="240.0" y2="20.0"/><line class="grid" x1="280.0" y1="230.0" x2="280.0" y2="20.0"/><line class="grid" x1="320.0" y1="230.0" x2="320.0" y2="20.0"/><line class="grid" x1="360.0" y1="230.0" x2="360.0" y2="20.0"/><line class="grid" x1="400.0" y1="230.0" x2="400.0" y2="20.0"/><line class="grid" x1="40.0" y1="230.0" x2="400.0" y2="230.0"/><line class="grid" x1="40.0" y1="206.7" x2="400.0" y2="206.7"/><line class="grid" x1="40.0" y1="183.3" x2="400.0" y2="183.3"/><line class="grid" x1="40.0" y1="160.0" x2="400.0" y2="160.0"/><line class="grid" x1="40.0" y1="136.7" x2="400.0" y2="136.7"/><line class="grid" x1="40.0" y1="113.3" x2="400.0" y2="113.3"/><line class="grid" x1="40.0" y1="90.0" x2="400.0" y2="90.0"/><line class="grid" x1="40.0" y1="66.7" x2="400.0" y2="66.7"/><line class="grid" x1="40.0" y1="43.3" x2="400.0" y2="43.3"/><line class="grid" x1="40.0" y1="20.0" x2="400.0" y2="20.0"/><line class="line" x1="40.0" y1="230.0" x2="400.0" y2="230.0"/><line class="line" x1="40.0" y1="230.0" x2="40.0" y2="20.0"/><text class="dim" x="80.0" y="243.0" font-size="9" text-anchor="middle">1</text><text class="dim" x="120.0" y="243.0" font-size="9" text-anchor="middle">2</text><text class="dim" x="160.0" y="243.0" font-size="9" text-anchor="middle">3</text><text class="dim" x="200.0" y="243.0" font-size="9" text-anchor="middle">4</text><text class="dim" x="240.0" y="243.0" font-size="9" text-anchor="middle">5</text><text class="dim" x="280.0" y="243.0" font-size="9" text-anchor="middle">6</text><text class="dim" x="320.0" y="243.0" font-size="9" text-anchor="middle">7</text><text class="dim" x="360.0" y="243.0" font-size="9" text-anchor="middle">8</text><text class="dim" x="35.0" y="186.3" font-size="9" text-anchor="end">4</text><text class="dim" x="35.0" y="139.7" font-size="9" text-anchor="end">8</text><text class="dim" x="35.0" y="93.0" font-size="9" text-anchor="end">12</text><text class="dim" x="35.0" y="46.3" font-size="9" text-anchor="end">16</text><circle class="dot2" cx="80.0" cy="206.7" r="4.5"/><circle class="dot" cx="80.0" cy="218.3" r="4.5"/><circle class="dot2" cx="120.0" cy="183.3" r="4.5"/><circle class="dot" cx="120.0" cy="212.5" r="4.5"/><circle class="dot2" cx="160.0" cy="160.0" r="4.5"/><circle class="dot" cx="160.0" cy="203.8" r="4.5"/><circle class="dot2" cx="200.0" cy="136.7" r="4.5"/><circle class="dot" cx="200.0" cy="190.6" r="4.5"/><circle class="dot2" cx="240.0" cy="113.3" r="4.5"/><circle class="dot" cx="240.0" cy="170.9" r="4.5"/><circle class="dot2" cx="280.0" cy="90.0" r="4.5"/><circle class="dot" cx="280.0" cy="141.4" r="4.5"/><circle class="dot2" cx="320.0" cy="66.7" r="4.5"/><circle class="dot" cx="320.0" cy="97.1" r="4.5"/><circle class="dot2" cx="360.0" cy="43.3" r="4.5"/><circle class="dot" cx="360.0" cy="30.7" r="4.5"/><line class="curve2" x1="56.0" y1="34.0" x2="76.0" y2="34.0"/><text class="ink" x="80.0" y="38.0" font-size="11" text-anchor="start">arithmetic: 2, 4, 6, … (+2 each step)</text><line class="curve" x1="56.0" y1="57.3" x2="76.0" y2="57.3"/><text class="ink" x="80.0" y="61.3" font-size="11" text-anchor="start">geometric: 1, 1.5, 2.25, … (×1.5 each step)</text><text class="dim" x="400.0" y="224.0" font-size="11" text-anchor="end">n</text></svg>
  <figcaption>The arithmetic sequence rises by the same amount at each step; its points lie on a line. The geometric sequence grows by the same factor at each step; it starts behind and then speeds up.</figcaption>
</figure>

If $r$ is negative the signs alternate ($1, -2, 4, -8, \dots$); if
$0 < r < 1$ the terms shrink: $80, 40, 20, 10, \dots$

## Sigma notation

The way to write a long sum briefly:

$$
\sum_{i=1}^{n} a_i = a_1 + a_2 + \dots + a_n
$$

Read it as "the sum of the $a_i$ for $i$ from $1$ to $n$".

| Part | Meaning |
|---|---|
| $\Sigma$ | add up |
| $i$ | the counter (index) |
| $i = 1$ below | the counter starts here |
| $n$ above | the counter ends here (included) |
| $a_i$ | the term added at each step |

**Read it by expanding.** Give the counter each value in turn, write the
terms, add them:

$$
\sum_{i=1}^{4} i^2 = 1 + 4 + 9 + 16 = 30
\qquad
\sum_{k=0}^{3} 2^k = 1 + 2 + 4 + 8 = 15
$$

**The number of terms** is the upper limit minus the lower limit plus one:
$\sum_{k=0}^{3}$ has four terms, $\sum_{i=3}^{7}$ has five.

**The counter's name does not matter.** $\sum_{i=1}^{4} i^2$ and
$\sum_{k=1}^{4} k^2$ are the same sum; the counter only lives inside the
sum.

**Rules.** These just restate addition and the distributive property:

| Rule | Why |
|---|---|
| $\sum (a_i + b_i) = \sum a_i + \sum b_i$ | terms can be added in any order |
| $\sum c \cdot a_i = c \sum a_i$ | a common factor comes out |
| $\sum_{i=1}^{n} c = n \cdot c$ | $c$ is added $n$ times |

**Watch out:** A product does not go inside: $\sum a_i b_i \neq \left(
\sum a_i \right) \left( \sum b_i \right)$. For $a = (1, 2)$, $b = (3, 4)$
the left side is $3 + 8 = 11$ and the right side $3 \cdot 7 = 21$.

## The sum of an arithmetic series

The story goes that Gauss found $1 + 2 + \dots + 100$ at school in a
minute: pair the first with the last, $1 + 100 = 2 + 99 = \dots = 101$;
there are $50$ pairs, so the sum is $50 \cdot 101 = 5050$.

<figure class="fig">
<svg viewBox="0 0 440 240" width="440"><rect class="dot" opacity="0.55" x="130" y="20" width="27" height="27" rx="3"/><rect class="dot2" opacity="0.55" x="160" y="20" width="27" height="27" rx="3"/><rect class="dot2" opacity="0.55" x="190" y="20" width="27" height="27" rx="3"/><rect class="dot2" opacity="0.55" x="220" y="20" width="27" height="27" rx="3"/><rect class="dot2" opacity="0.55" x="250" y="20" width="27" height="27" rx="3"/><rect class="dot2" opacity="0.55" x="280" y="20" width="27" height="27" rx="3"/><rect class="dot" opacity="0.55" x="130" y="50" width="27" height="27" rx="3"/><rect class="dot" opacity="0.55" x="160" y="50" width="27" height="27" rx="3"/><rect class="dot2" opacity="0.55" x="190" y="50" width="27" height="27" rx="3"/><rect class="dot2" opacity="0.55" x="220" y="50" width="27" height="27" rx="3"/><rect class="dot2" opacity="0.55" x="250" y="50" width="27" height="27" rx="3"/><rect class="dot2" opacity="0.55" x="280" y="50" width="27" height="27" rx="3"/><rect class="dot" opacity="0.55" x="130" y="80" width="27" height="27" rx="3"/><rect class="dot" opacity="0.55" x="160" y="80" width="27" height="27" rx="3"/><rect class="dot" opacity="0.55" x="190" y="80" width="27" height="27" rx="3"/><rect class="dot2" opacity="0.55" x="220" y="80" width="27" height="27" rx="3"/><rect class="dot2" opacity="0.55" x="250" y="80" width="27" height="27" rx="3"/><rect class="dot2" opacity="0.55" x="280" y="80" width="27" height="27" rx="3"/><rect class="dot" opacity="0.55" x="130" y="110" width="27" height="27" rx="3"/><rect class="dot" opacity="0.55" x="160" y="110" width="27" height="27" rx="3"/><rect class="dot" opacity="0.55" x="190" y="110" width="27" height="27" rx="3"/><rect class="dot" opacity="0.55" x="220" y="110" width="27" height="27" rx="3"/><rect class="dot2" opacity="0.55" x="250" y="110" width="27" height="27" rx="3"/><rect class="dot2" opacity="0.55" x="280" y="110" width="27" height="27" rx="3"/><rect class="dot" opacity="0.55" x="130" y="140" width="27" height="27" rx="3"/><rect class="dot" opacity="0.55" x="160" y="140" width="27" height="27" rx="3"/><rect class="dot" opacity="0.55" x="190" y="140" width="27" height="27" rx="3"/><rect class="dot" opacity="0.55" x="220" y="140" width="27" height="27" rx="3"/><rect class="dot" opacity="0.55" x="250" y="140" width="27" height="27" rx="3"/><rect class="dot2" opacity="0.55" x="280" y="140" width="27" height="27" rx="3"/><rect class="dot" opacity="0.55" x="20" y="186" width="14" height="14" rx="2"/><text class="ink" x="40" y="197" font-size="12" text-anchor="start">1 + 2 + 3 + 4 + 5</text><rect class="dot2" opacity="0.55" x="220" y="186" width="14" height="14" rx="2"/><text class="ink" x="240" y="197" font-size="12" text-anchor="start">the same, turned around</text><text class="ink" x="220" y="226" font-size="13" text-anchor="middle">2 · S = 5 · 6 = 30, so S = 15</text><text class="dim" x="120" y="39" font-size="11" text-anchor="end">1</text><text class="dim" x="120" y="69" font-size="11" text-anchor="end">2</text><text class="dim" x="120" y="99" font-size="11" text-anchor="end">3</text><text class="dim" x="120" y="129" font-size="11" text-anchor="end">4</text><text class="dim" x="120" y="159" font-size="11" text-anchor="end">5</text></svg>
  <figcaption>The purple squares are 1 + 2 + 3 + 4 + 5. The same staircase turned around and placed next to it (orange) makes a rectangle of 5 rows and 6 columns. The rectangle is twice the sum.</figcaption>
</figure>

The same idea fits every arithmetic series: write the sum twice, once in
reverse; each column makes $a_1 + a_n$ and there are $n$ columns.

$$
S_n = \frac{n \, (a_1 + a_n)}{2}
$$

A special case, the sum of the first $n$ natural numbers:

$$
\sum_{i=1}^{n} i = \frac{n(n + 1)}{2}
$$

The sum of $5, 8, 11, \dots, 62$ ($20$ terms) is
$\frac{20 \cdot 67}{2} = 670$.

The sum of the first $n$ squares has a formula too:
$\sum_{i=1}^{n} i^2 = \frac{n(n + 1)(2n + 1)}{6}$. For $n = 4$,
$\frac{4 \cdot 5 \cdot 9}{6} = 30$, the number we found above by
expanding.

## The sum of a geometric series

$S = a_1 + a_1 r + a_1 r^2 + \dots + a_1 r^{n-1}$. Multiplying both sides by
$r$ shifts the terms one place; subtracting $rS$ from $S$ cancels all the
terms in the middle:

$$
\begin{aligned}
S - rS &= a_1 - a_1 r^n \\
S &= a_1 \cdot \frac{1 - r^n}{1 - r} \qquad (r \neq 1)
\end{aligned}
$$

$1 + 2 + 4 + \dots + 2^9$: $a_1 = 1$, $r = 2$, $n = 10$ terms;
$\frac{1 - 2^{10}}{1 - 2} = \frac{-1023}{-1} = 1023$. In binary this is ten
$1$'s in a row, $1111111111_2 = 1023$.

The sum of $3, 6, 12, \dots, 384$ ($8$ terms) is
$3 \cdot \frac{1 - 2^8}{1 - 2} = 3 \cdot 255 = 765$.

## Infinite geometric series

$\frac{1}{2} + \frac{1}{4} + \frac{1}{8} + \dots$ has infinitely many
terms, but its sum is not infinite.

<figure class="fig">
<svg viewBox="0 0 440 114" width="440"><rect class="box" x="20" y="30" width="400" height="44"/><rect class="dot" opacity="0.6" x="20" y="30" width="198.5" height="44" rx="2"/><text class="ink" x="120.0" y="57.0" font-size="13" text-anchor="middle">½</text><rect class="dot2" opacity="0.6" x="220.0" y="30" width="98.5" height="44" rx="2"/><text class="ink" x="270.0" y="57.0" font-size="13" text-anchor="middle">¼</text><rect class="dot" opacity="0.6" x="320.0" y="30" width="48.5" height="44" rx="2"/><text class="ink" x="345.0" y="57.0" font-size="13" text-anchor="middle">⅛</text><rect class="dot2" opacity="0.6" x="370.0" y="30" width="23.5" height="44" rx="2"/><text class="ink" x="382.5" y="57.0" font-size="10" text-anchor="middle">1/16</text><rect class="dot" opacity="0.6" x="395.0" y="30" width="11.0" height="44" rx="2"/><rect class="dot2" opacity="0.6" x="407.5" y="30" width="4.8" height="44" rx="2"/><rect class="dot" opacity="0.6" x="413.8" y="30" width="1.6" height="44" rx="2"/><text class="dim" x="20" y="22" font-size="11" text-anchor="start">0</text><text class="dim" x="420" y="22" font-size="11" text-anchor="end">1</text><text class="ink" x="220.0" y="100" font-size="12" text-anchor="middle">the total approaches 1 but never passes it</text></svg>
  <figcaption>Half of a strip of length 1, then half of what is left, then half of that… At each step the gap left over halves; the pieces fill the strip but never overflow it.</figcaption>
</figure>

The sum of the first $n$ terms is called a **partial sum**:
$S_n = 1 - \left( \frac{1}{2} \right)^n$. As $n$ grows,
$\left( \frac{1}{2} \right)^n$ goes to zero and $S_n$ approaches $1$.

<figure class="fig">
<svg viewBox="0 0 440 224" width="440"><line class="grid" x1="50.0" y1="210.0" x2="50.0" y2="20.0"/><line class="grid" x1="88.9" y1="210.0" x2="88.9" y2="20.0"/><line class="grid" x1="127.8" y1="210.0" x2="127.8" y2="20.0"/><line class="grid" x1="166.7" y1="210.0" x2="166.7" y2="20.0"/><line class="grid" x1="205.6" y1="210.0" x2="205.6" y2="20.0"/><line class="grid" x1="244.4" y1="210.0" x2="244.4" y2="20.0"/><line class="grid" x1="283.3" y1="210.0" x2="283.3" y2="20.0"/><line class="grid" x1="322.2" y1="210.0" x2="322.2" y2="20.0"/><line class="grid" x1="361.1" y1="210.0" x2="361.1" y2="20.0"/><line class="grid" x1="400.0" y1="210.0" x2="400.0" y2="20.0"/><line class="grid" x1="50.0" y1="210.0" x2="400.0" y2="210.0"/><line class="grid" x1="50.0" y1="166.8" x2="400.0" y2="166.8"/><line class="grid" x1="50.0" y1="123.6" x2="400.0" y2="123.6"/><line class="grid" x1="50.0" y1="80.5" x2="400.0" y2="80.5"/><line class="grid" x1="50.0" y1="37.3" x2="400.0" y2="37.3"/><line class="line" x1="50.0" y1="210.0" x2="400.0" y2="210.0"/><line class="line" x1="50.0" y1="210.0" x2="50.0" y2="20.0"/><text class="dim" x="88.9" y="223.0" font-size="9" text-anchor="middle">1</text><text class="dim" x="127.8" y="223.0" font-size="9" text-anchor="middle">2</text><text class="dim" x="166.7" y="223.0" font-size="9" text-anchor="middle">3</text><text class="dim" x="205.6" y="223.0" font-size="9" text-anchor="middle">4</text><text class="dim" x="244.4" y="223.0" font-size="9" text-anchor="middle">5</text><text class="dim" x="283.3" y="223.0" font-size="9" text-anchor="middle">6</text><text class="dim" x="322.2" y="223.0" font-size="9" text-anchor="middle">7</text><text class="dim" x="361.1" y="223.0" font-size="9" text-anchor="middle">8</text><text class="dim" x="45.0" y="169.8" font-size="9" text-anchor="end">0.25</text><text class="dim" x="45.0" y="126.6" font-size="9" text-anchor="end">0.5</text><text class="dim" x="45.0" y="83.5" font-size="9" text-anchor="end">0.75</text><text class="dim" x="45.0" y="40.3" font-size="9" text-anchor="end">1</text><line class="curve3" stroke-dasharray="5 4" x1="50.0" y1="37.3" x2="400.0" y2="37.3"/><rect class="dot" opacity="0.75" x="80.3" y="123.6" width="17.1" height="86.4"/><rect class="dot" opacity="0.75" x="119.2" y="80.5" width="17.1" height="129.5"/><rect class="dot" opacity="0.75" x="158.1" y="58.9" width="17.1" height="151.1"/><rect class="dot" opacity="0.75" x="197.0" y="48.1" width="17.1" height="161.9"/><rect class="dot" opacity="0.75" x="235.9" y="42.7" width="17.1" height="167.3"/><rect class="dot" opacity="0.75" x="274.8" y="40.0" width="17.1" height="170.0"/><rect class="dot" opacity="0.75" x="313.7" y="38.6" width="17.1" height="171.4"/><rect class="dot" opacity="0.75" x="352.6" y="37.9" width="17.1" height="172.1"/><text class="ink" x="400.0" y="31.3" font-size="11" text-anchor="end">limit: 1</text><text class="dim" x="56.0" y="30.0" font-size="10" text-anchor="start">partial sum Sₙ</text><text class="dim" x="400.0" y="204.0" font-size="11" text-anchor="end">n</text></svg>
  <figcaption>The partial sums are 0.5, 0.75, 0.875, 0.9375… Each bar closes half of the gap between the previous one and 1. The limit is 1.</figcaption>
</figure>

The general rule: if $-1 < r < 1$ then $r^n \to 0$ and the $r^n$ in the
formula drops out:

$$
\sum_{k=0}^{\infty} a_1 r^k = \frac{a_1}{1 - r} \qquad (-1 < r < 1)
$$

- $\frac{1}{2} + \frac{1}{4} + \dots = \frac{1/2}{1 - 1/2} = 1$.
- $0.333\dots = \frac{3}{10} + \frac{3}{100} + \dots =
  \frac{3/10}{1 - 1/10} = \frac{1}{3}$.
- If $r \geq 1$ or $r \leq -1$ the terms do not shrink and the sum does
  not settle at a number: $1 + 2 + 4 + \dots$ grows without limit. An
  arithmetic series (with $d \neq 0$) always grows without limit too.

## Sigma in machine learning

**The mean.** The mean of $n$ numbers is

$$
\bar{x} = \frac{1}{n} \sum_{i=1}^{n} x_i
$$

**The loss function.** Mean squared error (MSE), for true values $y_i$ and
predictions $\hat{y}_i$:

$$
\text{MSE} = \frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2
$$

For $y = (3, 5, 8)$ and $\hat{y} = (2, 5, 10)$ the differences are
$1, 0, -2$; their squares $1, 0, 4$; $\text{MSE} = \frac{5}{3}$.

**A weighted sum.** A neuron's input is $\sum_{i} w_i x_i + b$: each
feature is multiplied by its own weight and added up. This is exactly the
dot product from Linear Algebra.

**Future rewards.** In reinforcement learning, an agent getting reward $1$
at every step discounts its future rewards with $\gamma = 0.9$:
$1 + 0.9 + 0.9^2 + \dots = \frac{1}{1 - 0.9} = 10$. An infinite geometric
series gives an infinite future a finite value.

**Moving averages.** Methods such as momentum and Adam add up old gradients
with weights $(1 - \beta), (1 - \beta)\beta, (1 - \beta)\beta^2, \dots$
These weights are a geometric series and they add up to
$\frac{1 - \beta}{1 - \beta} = 1$.

## Common mistakes

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Wrong</h4>
      <p>$a_{20} = a_1 + 20d$</p>
      <p>$\sum_{i=3}^{7}$: $4$ terms</p>
      <p>$\sum a_i b_i = \sum a_i \cdot \sum b_i$</p>
      <p>$1 + 2 + 4 + \dots = \dfrac{1}{1 - 2} = -1$</p>
    </div>
    <div class="ok">
      <h4>Right</h4>
      <p>$a_{20} = a_1 + 19d$</p>
      <p>$7 - 3 + 1 = 5$ terms</p>
      <p>a product does not go inside a sum</p>
      <p>$r = 2$: the sum grows without limit</p>
    </div>
  </div>
  <figcaption>The number of terms and the number of steps differ by one; the infinite sum formula only holds when −1 &lt; r &lt; 1.</figcaption>
</figure>

- **Taking the ratio upside down.** The common ratio is next over
  previous: in $80, 40, 20$, $r = \frac{40}{80} = \frac{1}{2}$, not $2$.
- **Forgetting the factor in front of Σ.** If $\frac{1}{n} \sum$ is
  written, the division comes after the whole sum.

## Summary

- A sequence is numbers in order, $a_n$; it is defined by a general term
  or from the previous term.
- Arithmetic: $a_n = a_1 + (n - 1)d$, sum $\frac{n(a_1 + a_n)}{2}$.
- Geometric: $a_n = a_1 r^{n-1}$, sum $a_1 \frac{1 - r^n}{1 - r}$.
- $\sum_{i=1}^{n} i = \frac{n(n + 1)}{2}$.
- In Σ the counter runs from the lower limit to the upper limit; there are
  rules for sums and constant factors, but a product does not go inside.
- If $-1 < r < 1$ the infinite geometric series is $\frac{a_1}{1 - r}$.
- The mean, MSE, a weighted sum, discounted reward and moving averages are
  all Σ.
