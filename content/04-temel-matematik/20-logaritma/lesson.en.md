# Logarithms

Logarithms are everywhere in machine learning: in the formula that measures
a model's loss, when fixing a skewed column, when describing how fast an
algorithm is, when working out how "surprising" a probability is. Most
people remember them from school as a set of rules that were memorised and
then forgotten.

In this chapter we will not memorise the rules; we will see **where they
come from**. Once you understand that a logarithm is the answer to a single
question, every rule follows from that question on its own.

The only thing you need before starting is the **exponent**:
$2^3 = 2 \cdot 2 \cdot 2 = 8$. The exponent rules were covered in the
Exponents chapter; I will remind you of them as we go.

## A single question

Look at these three questions:

- $2^3 = \;?$ — The answer is $8$. You know the base and the exponent; you
  are looking for the **result**.
- $?^3 = 8$ — The answer is $2$. You know the exponent and the result; you
  are looking for the **base**. That is a root: $\sqrt[3]{8} = 2$.
- $2^{?} = 8$ — The answer is $3$. You know the base and the result; you
  are looking for the **exponent**.

The third question has a name. The **logarithm** is the answer to "which
power do I raise this base to in order to get this number?":

$$
\log_2 8 = 3 \quad\text{because}\quad 2^3 = 8
$$

It is read "the logarithm of 8 to base 2 is 3". In general:

$$
\log_b x = y \quad\Longleftrightarrow\quad b^y = x
$$

The two sides are **two ways of writing the same sentence**. The left one
asks "what is the exponent?", the right one answers "this is the exponent".
Whenever a logarithm expression stops you, the first thing to do is rewrite
it in the form on the right.

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>$b$ — base</span><span>The number being raised to a power. Must be positive and not 1.</span></div>
    <div class="anat-row"><span>$x$ — number (argument)</span><span>The result you want to reach. Must be positive.</span></div>
    <div class="anat-row"><span>$y$ — logarithm</span><span>The exponent you are looking for. Can be negative, zero or a fraction.</span></div>
  </div>
  <figcaption>The three parts of a logarithm. The $y$ you calculate is really an exponent.</figcaption>
</figure>

### Three inverse operations

In mathematics every operation has a partner that undoes it:

| Operation | Undone by | Example |
|---|---|---|
| Addition | Subtraction | $5 + 3 = 8$ → $8 - 3 = 5$ |
| Multiplication | Division | $5 \cdot 3 = 15$ → $15 / 3 = 5$ |
| Exponentiation | Root **or** logarithm | $2^3 = 8$ → $\sqrt[3]{8} = 2$ and $\log_2 8 = 3$ |

Exponentiation has **two** inverses because, unlike addition and
multiplication, order matters: $2^3$ is not the same as $3^2$. Undoing the
base is one job (the root), undoing the exponent is another (the logarithm).

### A few by hand

For each one, turn the question into "which power of the base gives the
number?":

- $\log_{10} 1000$: $10^{?} = 1000$. $10^3 = 1000$, so the answer is $3$.
- $\log_3 81$: $3^{?} = 81$. $3 \cdot 3 \cdot 3 \cdot 3 = 81$, so $4$.
- $\log_2 1024$: $2^{10} = 1024$, so $10$.
- $\log_5 5$: $5^{?} = 5$. Every number to the first power is itself, so $1$.
- $\log_7 1$: $7^{?} = 1$. Every non-zero number to the zeroth power is $1$,
  so $0$.

## Negative and fractional results

Because the result of a logarithm is an exponent, it can take any value an
exponent can.

A **negative exponent** means "one over": $2^{-1} = \frac{1}{2}$,
$2^{-3} = \frac{1}{8}$. So:

$$
\log_2 \tfrac{1}{8} = -3 \qquad \log_{10} 0.01 = -2
$$

This gives an important consequence: **the logarithm of a positive number
smaller than 1 is negative** (when the base is greater than 1). Because
probabilities lie between 0 and 1, the logarithm of a probability always
comes out negative. That is why the loss formulas in machine learning start
with a minus sign; we will come back to this.

A **fractional exponent** means a root: $4^{1/2} = \sqrt{4} = 2$. So
$\log_4 2 = \frac{1}{2}$.

Most logarithms are not whole numbers. What is $\log_2 3$? It is somewhere
between $2^1 = 2$ and $2^2 = 4$, so the answer lies between 1 and 2. A
calculator says $1.58496...$ and indeed $2^{1.58496} \approx 3$.

To **estimate** a logarithm, looking at the two neighbouring whole powers
helps a lot. $\log_{10} 5000$? It lies between $10^3 = 1000$ and
$10^4 = 10000$, so between 3 and 4 — and since 5000 is "closer" to 10000
than to 1000 in this sense, around 3.7. (The actual value is $3.699$.)

## What has no logarithm?

The definition gives two prohibitions. You can see both with the question
"what is the exponent?":

- **Zero has no logarithm.** There is no exponent for which $2^{?} = 0$. As
  the exponent gets smaller the result **approaches** zero
  ($2^{-10} \approx 0.001$, $2^{-100}$ is far smaller) but never reaches it.
  That is why $\log x$ goes to minus infinity as $x$ approaches zero.
- **Negative numbers have no logarithm.** Whatever power of a positive base
  you take, the result is positive. $2^{?} = -8$ is impossible.

The base itself has two conditions too: it must be positive and must not be
1. Every power of $1$ is $1$; the question $\log_1 5$ has no answer.

These prohibitions come up often when solving equations: the algebra
sometimes produces a "solution" that makes the inside of a logarithm negative,
and it has to be rejected. We will see an example of this step by step below.

## The graph: a mirror of the exponent

Let us draw $y = 2^x$ and $y = \log_2 x$ on the same axes:

<figure class="fig">
<svg viewBox="0 0 380 320" width="380"><line class="grid" x1="67" y1="290" x2="67" y2="20"/><line class="grid" x1="30" y1="260" x2="360" y2="260"/><line class="grid" x1="103" y1="290" x2="103" y2="20"/><line class="grid" x1="30" y1="230" x2="360" y2="230"/><line class="grid" x1="177" y1="290" x2="177" y2="20"/><line class="grid" x1="30" y1="170" x2="360" y2="170"/><line class="grid" x1="213" y1="290" x2="213" y2="20"/><line class="grid" x1="30" y1="140" x2="360" y2="140"/><line class="grid" x1="250" y1="290" x2="250" y2="20"/><line class="grid" x1="30" y1="110" x2="360" y2="110"/><line class="grid" x1="287" y1="290" x2="287" y2="20"/><line class="grid" x1="30" y1="80" x2="360" y2="80"/><line class="grid" x1="323" y1="290" x2="323" y2="20"/><line class="grid" x1="30" y1="50" x2="360" y2="50"/><line class="line" x1="30" y1="200" x2="360" y2="200"/><line class="line" x1="140" y1="290" x2="140" y2="20"/><text class="dim" x="67" y="215" font-size="11" text-anchor="middle">-2</text><text class="dim" x="132" y="264" font-size="11" text-anchor="end">-2</text><text class="dim" x="103" y="215" font-size="11" text-anchor="middle">-1</text><text class="dim" x="132" y="234" font-size="11" text-anchor="end">-1</text><text class="dim" x="177" y="215" font-size="11" text-anchor="middle">1</text><text class="dim" x="132" y="174" font-size="11" text-anchor="end">1</text><text class="dim" x="213" y="215" font-size="11" text-anchor="middle">2</text><text class="dim" x="132" y="144" font-size="11" text-anchor="end">2</text><text class="dim" x="250" y="215" font-size="11" text-anchor="middle">3</text><text class="dim" x="132" y="114" font-size="11" text-anchor="end">3</text><text class="dim" x="287" y="215" font-size="11" text-anchor="middle">4</text><text class="dim" x="132" y="84" font-size="11" text-anchor="end">4</text><text class="dim" x="323" y="215" font-size="11" text-anchor="middle">5</text><text class="dim" x="132" y="54" font-size="11" text-anchor="end">5</text><path class="curve3" stroke-dasharray="5 5" d="M30,290 L360,20"/><path class="curve" d="M30,196 L38,196 L46,195 L54,194 L62,193 L69,192 L77,191 L85,189 L93,188 L101,186 L109,183 L117,181 L125,178 L132,174 L140,170 L148,165 L156,159 L164,153 L172,145 L180,137 L188,126 L195,115 L203,101 L211,85 L219,66 L227,45 L235,20"/><path class="curve2" d="M145,290 L153,245 L161,224 L169,210 L178,199 L186,190 L194,183 L203,177 L211,171 L219,167 L227,162 L236,158 L244,155 L252,152 L261,148 L269,146 L277,143 L285,140 L294,138 L302,136 L310,134 L319,131 L327,130 L335,128 L343,126 L352,124 L360,122"/><circle class="dot" cx="140" cy="170" r="4"/><circle class="dot2" cx="177" cy="200" r="4"/><circle class="dot" cx="213" cy="80" r="4"/><circle class="dot2" cx="287" cy="140" r="4"/><text class="ink" x="242" y="32" font-size="13">y = 2<tspan baseline-shift="super" font-size="9">x</tspan></text><text class="ink" x="298" y="118" font-size="13">y = log₂ x</text><text class="dim" x="309" y="41" font-size="12">y = x</text></svg>
  <figcaption>Purple is $2^x$, orange is $\log_2 x$. The dashed line is $y = x$; the two curves are reflections of each other across it. The point $(2, 4)$ on $2^x$ becomes $(4, 2)$ on the logarithm.</figcaption>
</figure>

There are four things to read from the graph:

1. **The two curves mirror each other across $y = x$.** This is true of all
   inverse functions: the input of one is the output of the other. The
   point $(0, 1)$ reflects to $(1, 0)$, and $(2, 4)$ reflects to $(4, 2)$.
2. **A logarithm always passes through $(1, 0)$**, whatever the base:
   $\log_b 1 = 0$.
3. **There is a wall on the left.** The orange curve never touches $x = 0$;
   it plunges down towards infinity. The graph is saying too that zero and
   negative numbers have no logarithm.
4. **A logarithm grows very slowly.** When $x$ goes from 1 to 4, $y$ goes
   from 0 to 2; when $x$ goes from 4 to 1024, $y$ only goes from 2 to 10.
   However fast the exponential explodes, the logarithm climbs just as
   slowly.

The fourth point is the logarithm's most useful property: **it turns very
large numbers into small, manageable ones.** With $\log_{10}$ a million
becomes 6 and a billion becomes 9.

## Three special bases

In theory any positive number (except 1) can be a base. In practice three
are used, and each has its own notation.

### Base 10: the digit counter

$\log_{10}$ lines up exactly with our decimal system. $\log_{10} 100 = 2$,
$\log_{10} 1000 = 3$: **the logarithm is one less than the number of
digits.** Precisely, if $n$ is a positive whole number:

$$
\text{number of digits} = \lfloor \log_{10} n \rfloor + 1
$$

$\lfloor \cdot \rfloor$ means "round down". $\log_{10} 5000 = 3.699$, rounded
down is 3, plus one is 4: 5000 has four digits. The power of this formula is
finding the number of digits without writing the number out. How many digits
does $2^{100}$ have?

$$
\log_{10} 2^{100} = 100 \cdot \log_{10} 2 = 100 \cdot 0.30103 = 30.103
\quad\Rightarrow\quad 31 \text{ digits}
$$

(The first equality uses a rule we will see shortly.)

Some sources mean base 10 when they write a plain $\log x$ with no base.
**Careful:** in machine learning sources a plain $\log$ usually means the
next base, $e$.

### Base e: the natural logarithm

$e = 2.71828...$ is one of the most important constants in mathematics. You
can see where it comes from with an interest calculation.

You put 1 unit of money in the bank at 100% annual interest. At the end of the year
you have 2. What if the bank applies half the interest **twice** a year? After
six months you have 1.5, at the end of the year $1.5 \cdot 1.5 = 2.25$. The
more often interest is applied, the larger the result:

| Times per year | Calculation | End of year |
|---|---|---|
| 1 | $(1 + 1)^1$ | 2 |
| 12 (monthly) | $(1 + \frac{1}{12})^{12}$ | 2.613 |
| 365 (daily) | $(1 + \frac{1}{365})^{365}$ | 2.7146 |
| 1 000 000 | $(1 + \frac{1}{10^6})^{10^6}$ | 2.71828 |

The result does not run off to infinity; **it levels off at a number.** That
number is $e$. It is the natural base of everything that grows
continuously (populations, radioactive decay, continuously compounded
interest).

The logarithm to base $e$ is called the **natural logarithm** and is written
$\ln$:

$$
\ln x = \log_e x \qquad \ln e = 1 \qquad \ln 1 = 0
$$

Almost every logarithm in machine learning is a natural logarithm. The reason
becomes clear in the next module (Calculus): the derivative of $e^x$ is
itself, and the derivative of $\ln x$ is $\frac{1}{x}$. In no other base do
the derivatives come out this cleanly.

### Base 2: bits and halving

$\log_2$ is the base of computer science. It answers two questions:

- **How many times can you halve a number before you reach 1?**
  $\log_2 1024 = 10$: 1024 → 512 → ... → 1, ten steps. That is why binary
  search finds an item among a million sorted items in at most 20 steps
  ($\log_2 10^6 \approx 19.93$). What you will see as $O(\log n)$ in the
  Algorithms track is exactly this.
- **How many bits do you need to tell things apart?** To distinguish 8
  different values $\log_2 8 = 3$ bits are enough (000 to 111). It will
  return as the unit of information in the entropy chapter.

## The rules and where they come from

Every logarithm rule is an exponent rule read backwards. I will derive each
one; instead of memorising them, it is enough to understand this derivation
once.

Recall the three exponent rules:

$$
b^m \cdot b^n = b^{m+n} \qquad \frac{b^m}{b^n} = b^{m-n} \qquad (b^m)^k = b^{m \cdot k}
$$

### Rule 1: The log of a product is a sum

$$
\log_b (x \cdot y) = \log_b x + \log_b y
$$

**Why:** Let $\log_b x = m$ and $\log_b y = n$. By definition $x = b^m$ and
$y = b^n$. Multiply them:

$$
x \cdot y = b^m \cdot b^n = b^{m+n}
$$

The last equality says "to get $x \cdot y$, raise $b$ to the power $m + n$".
So $\log_b (xy) = m + n = \log_b x + \log_b y$.

**Example:** $\log_{10} 2 + \log_{10} 5 = \log_{10} 10 = 1$. Indeed
$0.30103 + 0.69897 = 1$.

This rule is **why logarithms were invented**. In the 1600s astronomers had
to multiply large numbers by hand. With a table of logarithms multiplication
turned into addition: look up the logarithms of the two numbers, add them,
and read the result back from the table. Today we use the same conversion to
stay within the limits of computer numbers.

### Rule 2: The log of a quotient is a difference

$$
\log_b \frac{x}{y} = \log_b x - \log_b y
$$

The derivation is the same: $\frac{x}{y} = \frac{b^m}{b^n} = b^{m-n}$.

A special case: $\log_b \frac{1}{x} = \log_b 1 - \log_b x = -\log_b x$. The
logarithm of a reciprocal is the negative of the logarithm.

### Rule 3: The log of a power is a product

$$
\log_b (x^k) = k \cdot \log_b x
$$

**Why:** if $x = b^m$ then $x^k = (b^m)^k = b^{m \cdot k}$. The exponent is
$k \cdot m$.

This is the rule we used for the digit count: $\log_{10} 2^{100} =
100 \cdot \log_{10} 2$. It moves the exponent to the front as a factor; in
other words, **it brings the unknown down from the exponent.** That is the
key to solving equations.

A root is also a power, so the rule covers it too:
$\log_b \sqrt{x} = \log_b x^{1/2} = \frac{1}{2}\log_b x$.

### Rule 4: Change of base

Calculators often only have $\ln$ and $\log_{10}$. How do you
calculate $\log_2 3$?

$$
\log_b x = \frac{\log_k x}{\log_k b} \qquad \text{(k is any base)}
$$

**Why:** let $\log_b x = y$, so $b^y = x$. Take the logarithm of both sides
in base $k$: $\log_k (b^y) = \log_k x$. By Rule 3,
$y \cdot \log_k b = \log_k x$. Isolate $y$:
$y = \frac{\log_k x}{\log_k b}$.

**Example:** $\log_2 3 = \frac{\ln 3}{\ln 2} = \frac{1.0986}{0.6931} = 1.585$.

This rule has another consequence: **logarithms in two bases are constant
multiples of each other.** $\log_2 x = \frac{\ln x}{\ln 2} = 1.4427 \cdot \ln x$.
Whichever base you choose, the **shape** of the curve is the same; it only
stretches vertically. That is why machine learning often does not care about
the base: the ordering and the position of the minimum do not change.

All the rules in one place:

| Rule | What it does |
|---|---|
| $\log_b (xy) = \log_b x + \log_b y$ | Product → sum |
| $\log_b (x/y) = \log_b x - \log_b y$ | Quotient → difference |
| $\log_b (x^k) = k \log_b x$ | Power → factor |
| $\log_b x = \dfrac{\ln x}{\ln b}$ | Change of base |
| $\log_b 1 = 0$ and $\log_b b = 1$ | The same in every base |
| $b^{\log_b x} = x$ and $\log_b (b^x) = x$ | Exponent and logarithm cancel out |

They all follow from the definition $\log_b x = y \iff b^y = x$.

## Common mistakes

There are four equalities that look very much like the rules but are
**wrong**. They are the ones most often mixed up, in exams and in real code.

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Wrong</h4>
      <p>$\log (x + y) = \log x + \log y$</p>
      <p>$\log (x - y) = \log x - \log y$</p>
      <p>$\dfrac{\log x}{\log y} = \log \dfrac{x}{y}$</p>
      <p>$(\log x)^2 = 2 \log x$</p>
    </div>
    <div class="ok">
      <h4>Right</h4>
      <p>$\log (x \cdot y) = \log x + \log y$</p>
      <p>$\log (x / y) = \log x - \log y$</p>
      <p>$\dfrac{\log x}{\log y} = \log_y x$ (change of base)</p>
      <p>$\log (x^2) = 2 \log x$</p>
    </div>
  </div>
  <figcaption>A logarithm opens up products and quotients; it cannot open up sums and differences.</figcaption>
</figure>

The first is easy to disprove with numbers: $\log_{10} (10 + 10) =
\log_{10} 20 = 1.301$, but $\log_{10} 10 + \log_{10} 10 = 2$. **The logarithm
of a sum has no simple expansion.**

In the fourth, the position of the brackets changes everything: $(\log x)^2$
is the square of the logarithm, $\log(x^2)$ is the logarithm of the square.

## Exponential equations

The logarithm is the tool for when the unknown is **in the exponent**. A
typical question: how many years does an investment returning 7% a year take
to double?

Each year the money is multiplied by $1.07$. After $t$ years it is $1.07^t$
times the original. We want double:

$$
1.07^t = 2
$$

The unknown is in the exponent. Take the logarithm of both sides and bring it
down with Rule 3:

$$
\ln (1.07^t) = \ln 2 \quad\Rightarrow\quad t \cdot \ln 1.07 = \ln 2
\quad\Rightarrow\quad t = \frac{\ln 2}{\ln 1.07} = \frac{0.6931}{0.0677} = 10.24
$$

About ten years. (The financiers' "rule of 72" is a shortcut for this
calculation: $72 / 7 \approx 10.3$.)

The general method is always the same:

<figure class="fig">
  <div class="flow">
    <span class="node">Isolate the power term</span>
    <span class="arrow">→</span>
    <span class="node">Take the log of both sides</span>
    <span class="arrow">→</span>
    <span class="node">Bring the exponent down (Rule 3)</span>
    <span class="arrow">→</span>
    <span class="node ok">Solve for the unknown</span>
  </div>
  <figcaption>Four steps when the unknown is in the exponent. The base of the logarithm you take does not change the answer.</figcaption>
</figure>

Let us apply the method step by step in three different situations.

### A power with a coefficient in front

**Question:** Savings of 3000 grow by 4% a year. After how many years do they
reach 4500?

$$
3000 \cdot 1.04^t = 4500
$$

**1. Isolate the power term.** Divide both sides by 3000:

$$
1.04^t = \frac{4500}{3000} = 1.5
$$

**2. Take the logarithm and bring the exponent down:**

$$
t \cdot \ln 1.04 = \ln 1.5
\quad\Rightarrow\quad
t = \frac{\ln 1.5}{\ln 1.04} = \frac{0.4055}{0.0392} \approx 10.34 \text{ years}
$$

Skipping the first step and taking the logarithm straight away is not wrong,
just longer. Rule 1 splits the product:

$$
\ln (3000 \cdot 1.04^t) = \ln 4500
\quad\Rightarrow\quad
\ln 3000 + t \ln 1.04 = \ln 4500
$$

$$
t = \frac{\ln 4500 - \ln 3000}{\ln 1.04} = \frac{8.4118 - 8.0064}{0.0392} \approx 10.34
$$

The same result. The **common mistake** is expanding $\ln(3000 \cdot 1.04^t)$
as $t \cdot \ln(3000 \cdot 1.04)$: the exponent sits only on $1.04$, not on
3000.

### A shrinking quantity

**Question:** A machine loses 20% of its value every year. After how many
years is its value halved?

Each year the value is multiplied by $0.8$:

$$
0.8^t = 0.5
\quad\Rightarrow\quad
t = \frac{\ln 0.5}{\ln 0.8} = \frac{-0.6931}{-0.2231} \approx 3.11 \text{ years}
$$

Both logarithms are negative, because $0.5$ and $0.8$ are below 1. When you
divide, the minus signs cancel and the time comes out positive. A negative
result would be a warning: it would mean you expected something shrinking to
grow, or something growing to shrink.

### Different bases on the two sides

**Question:** Solve $2^{x+1} = 5^x$.

The bases differ and we cannot turn one into the other. Take the logarithm of
both sides:

$$
\ln 2^{x+1} = \ln 5^x
\quad\Rightarrow\quad
(x + 1)\ln 2 = x \ln 5
$$

There is no exponent left; it is an ordinary linear equation. Expand the
bracket and gather the $x$ terms on one side:

$$
x \ln 2 + \ln 2 = x \ln 5
\quad\Rightarrow\quad
\ln 2 = x \ln 5 - x \ln 2 = x (\ln 5 - \ln 2)
$$

$$
x = \frac{\ln 2}{\ln 5 - \ln 2} = \frac{\ln 2}{\ln 2.5} = \frac{0.6931}{0.9163} \approx 0.7565
$$

**Check:** $2^{1.7565} \approx 3.379$ and $5^{0.7565} \approx 3.379$. Writing
$\ln 5 - \ln 2 = \ln \frac{5}{2}$ in the denominator is thanks to Rule 2.

## Logarithmic equations

This time the unknown is **inside** the logarithm. The tool works in the other
direction: using the definition to turn the logarithm into an exponent.

### A single logarithm: rewrite with the definition

If $\log_3 (x - 1) = 2$, the definition gives $3^2 = x - 1$, so $x = 10$.

**Check:** $x - 1 = 9 > 0$, the logarithm is defined. The answer is $x = 10$.

### Several logarithms: combine first

**Question:** $\log_2 x + \log_2 (x - 2) = 3$

**1. Gather into one logarithm with Rule 1:**

$$
\log_2 \big(x (x - 2)\big) = 3
$$

**2. Rewrite with the definition:**

$$
x(x - 2) = 2^3 = 8
\quad\Rightarrow\quad
x^2 - 2x - 8 = 0
$$

**3. Solve the quadratic.** Two numbers whose product is $-8$ and sum is
$-2$ are $-4$ and $2$:

$$
(x - 4)(x + 2) = 0
\quad\Rightarrow\quad
x = 4 \;\text{ or }\; x = -2
$$

**4. Check every candidate in the original equation.**

- $x = 4$: $\log_2 4 + \log_2 2 = 2 + 1 = 3$. ✓
- $x = -2$: $\log_2 (-2)$ is undefined. ✕

The algebra produced two answers but only one is valid: **$x = 4$.** The
false solution appeared in the first step, when we combined the two
logarithms. The product $x(x-2)$ is positive for $x = -2$ ($(-2)(-4) = 8$),
while $x$ and $x - 2$ on their own are negative. Combining hid the condition
set by the original equation.

### Logarithms in the same base on both sides

**Question:** $\log_5 (2x + 3) = \log_5 (x + 7)$

A logarithm is **one-to-one**: if two numbers have equal logarithms, the
numbers themselves are equal. (The curve on the graph always rises; it cannot
reach the same height from two different points.)

$$
2x + 3 = x + 7 \quad\Rightarrow\quad x = 4
$$

**Check:** $2 \cdot 4 + 3 = 11 > 0$ and $4 + 7 = 11 > 0$. Valid.

### Why checking is essential

Exponential equations cause no trouble: $b^x$ is defined for every $x$. In a
logarithmic equation, however, the inside of every logarithm must be positive,
and that condition can slip away while you apply the rules. Make it a habit:
**put every answer you find into every logarithm of the original equation and
check that it is positive.**

## Logarithmic scale

When a quantity spreads over a very wide range (from 1 to a million), the
small values get squashed against zero on an ordinary axis. On a logarithmic
scale the axis moves in **equal ratios rather than equal steps**: the
distances between 1, 10, 100 and 1000 are the same.

You meet it in daily life more than you might think:

- **Earthquake magnitude:** a magnitude 6 earthquake has 10 times the
  amplitude of a magnitude 5.
- **Sound level (decibels):** a 10 dB increase is a 10-fold increase in
  sound power.
- **pH:** pH 3 is 10 times more acidic than pH 4.

The idea is the same in all of them: **equal differences stand for equal
ratios.** On a logarithmic scale "twice as much" has the same length
everywhere.

The mathematical reason is Rule 2: $\log 100 - \log 10 = \log \frac{100}{10} = \log 10$
and $\log 1000 - \log 100 = \log 10$. Only the **ratio** decides the difference.

## Logarithms in machine learning

Everything so far leads to these five places. Each of these topics will come
back in detail in its own chapter; here it is enough to see what job the
logarithm does.

### 1. Turning products into sums

If a model gives each of 400 independent events a probability of $0.01$, the
probability of all of them happening together is the product:

$$
0.01^{400} = (10^{-2})^{400} = 10^{-800}
$$

Computers store decimal numbers with limited precision, and a number smaller
than about $10^{-308}$ **is rounded to zero**. Once the result is zero,
comparing two models is impossible: both say "zero".

The fix is Rule 1 and Rule 3:

$$
\ln \prod_{i=1}^{400} p_i = \sum_{i=1}^{400} \ln p_i
\qquad\text{here}\qquad
400 \cdot \ln 0.01 = 400 \cdot (-4.605) = -1842.07
$$

The same information, as an ordinary number. Because the logarithm is an
increasing function, a larger product also has a larger logarithm; the
answer to "which is more likely" does not change. In statistics this is
called the **log-likelihood**, and much of training a model is trying to
make it as large as possible.

### 2. The loss function: log-loss

Classification models are judged by the probability they give the correct
class. The penalty for a prediction that gives the correct class
probability $p$ is:

$$
\text{loss} = -\ln p
$$

| Probability given to the correct class $p$ | $-\ln p$ |
|---|---|
| 0.9 | 0.105 |
| 0.5 | 0.693 |
| 0.1 | 2.303 |
| 0.01 | 4.605 |

The minus sign makes the penalty positive, because the logarithm of a
probability (between 0 and 1) is negative. What matters is the shape of the
table: if the model is confident and right, the penalty is almost zero; **if
it is confident and wrong, the penalty explodes.** As $p$ goes to zero,
$-\ln p$ goes to infinity; the "wall on the left of the graph" is what
discourages the model from being overconfident here.

### 3. Taming skewed data

In quantities such as income, house price or city population, most values are
small and a few are huge. The yearly income of eight people:

| 18,000 | 22,000 | 25,000 | 31,000 | 40,000 | 55,000 | 90,000 | 2,500,000 |
|---|---|---|---|---|---|---|---|

The mean is 347,625, the median 35,500. A single value has pulled the mean
up tenfold; the largest value is $\frac{2{,}500{,}000}{18{,}000} \approx 139$
times the smallest.

Let us take $\log_{10}$ of each value:

| 4.255 | 4.342 | 4.398 | 4.491 | 4.602 | 4.740 | 4.954 | 6.398 |
|---|---|---|---|---|---|---|---|

The gap shrank to $6.398 - 4.255 = 2.14$ units. Rule 2 tells you why: in a
logarithm **a ratio becomes a difference**, and $\log_{10} 139 \approx 2.14$.
Going from 20 thousand to 40 thousand becomes the same distance as going from
1 million to 2 million.

If the values contain **zero**, $\log 0$ is undefined. Then $\ln(1 + x)$ is
used instead: for $x = 0$ the result is $\ln 1 = 0$.

### 4. The speed of algorithms

A method that halves the problem at each step finishes in $\log_2 n$ steps on
$n$ items. For a billion items that is $\log_2 10^9 \approx 30$ steps.
Searching a sorted list, decision trees and database indexes get their speed
from this logarithm.

### 5. Information and entropy

How "surprising" an event with probability $p$ is gets measured as
$-\log_2 p$ bits: a coin toss ($p = \frac{1}{2}$) is exactly
$-\log_2 \frac{1}{2} = 1$ bit, an event with probability $\frac{1}{8}$ is $3$
bits. The less expected an event, the more information it carries. The
entropy that decision trees use to choose which question to ask first comes
from this idea.

## In code

The subject of this chapter is mathematics, but one difference will be useful
when you write code later. **In programming languages a plain `log` is the
natural logarithm** ($\ln$), not base 10 as at school. Bases 10 and 2 have
their own functions (`log10`, `log2`). You will use logarithms in code in the
Data Science and Machine Learning tracks.

## Summary

- $\log_b x = y$ answers "which power of $b$ gives $x$?"; that is,
  $b^y = x$. When stuck, rewrite it in that form.
- The result is an exponent, so it can be negative or fractional; but **the
  argument must be positive.** Zero and negative numbers have no logarithm.
- Numbers below 1 have negative logarithms; the logarithm of a probability
  is always negative.
- Three bases: $\log_{10}$ (digits), $\ln$ (base $e$, the default in ML),
  $\log_2$ (halving, bits).
- The rules are the exponent rules backwards: product → sum, quotient →
  difference, power → factor. The logarithm of a sum does not expand.
- **Exponential equation:** isolate the power term, take the logarithm of
  both sides, bring the exponent down.
- **Logarithmic equation:** combine the logarithms, rewrite with the
  definition, solve and **check every answer.**
- In ML: turning products into sums, log-loss, compressing skewed values,
  $\log_2 n$ speed and entropy.
