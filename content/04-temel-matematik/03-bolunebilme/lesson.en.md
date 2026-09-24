# Divisibility, Primes, GCD and LCM

Whether one number divides **exactly** into another looks like a small
question at first. But simplifying fractions, splitting a job into equal
parts and finding when two events will line up again all rest on it. In
this section we will see the divisibility rules, the building blocks of
numbers, the **primes**, and two powerful tools: the greatest common
divisor (**GCD**) and the least common multiple (**LCM**).

Prerequisite: the Natural Numbers and Order of Operations section
(especially division with remainder).

## Divisors and multiples

Let $a$ and $b$ be natural numbers. If dividing $b$ by $a$ leaves
remainder $0$, that is, if for some natural number $k$ we can write

$$
b = a \cdot k
$$

then $a$ is a **divisor** of $b$ and $b$ is a **multiple** of $a$. For
example, $12 = 3 \cdot 4$: $3$ is a divisor of $12$; $12$ is a multiple of $3$.

- The divisors of $12$: $1, 2, 3, 4, 6, 12$. Finitely many.
- The multiples of $12$: $12, 24, 36, 48, \dots$ Infinitely many.

The orderly way to find divisors is to look for them **in pairs**:
$1 \cdot 12$, $2 \cdot 6$, $3 \cdot 4$. Once the factors meet in the
middle you can stop; $4 \cdot 3$ has already been found.

## Divisibility rules

We can tell whether a large number is divisible by a small one from its
digits, without dividing:

| Divisor | Rule | Example |
|---|---|---|
| $2$ | the last digit is even ($0, 2, 4, 6, 8$) | $3\,584$: last digit $4$ ✓ |
| $3$ | the digit sum is divisible by $3$ | $2\,415$: $2+4+1+5 = 12$ ✓ |
| $4$ | the number formed by the last two digits is divisible by $4$ | $7\,316$: $16$ ✓ |
| $5$ | the last digit is $0$ or $5$ | $1\,235$ ✓ |
| $6$ | divisible by both $2$ and $3$ | $474$: even, $4+7+4 = 15$ ✓ |
| $8$ | the number formed by the last three digits is divisible by $8$ | $5\,120$: $120 = 8 \cdot 15$ ✓ |
| $9$ | the digit sum is divisible by $9$ | $8\,127$: $8+1+2+7 = 18$ ✓ |
| $10$ | the last digit is $0$ | $4\,930$ ✓ |
| $11$ | starting from the right, add the digits with signs $+, -, +, -$; the result is divisible by $11$ | $9\,273$: $3 - 7 + 2 - 9 = -11$ ✓ |

### Why does the digit-sum rule work?

The key: $10 = 9 + 1$, $100 = 99 + 1$, $1\,000 = 999 + 1$. So every place
value is **a multiple of $9$ plus $1$**. Let us expand a three-digit
number $abc$:

$$
\begin{aligned}
100a + 10b + c &= (99a + a) + (9b + b) + c \\
&= \underbrace{99a + 9b}_{\text{a multiple of } 9} + (a + b + c)
\end{aligned}
$$

The first part is always divisible by $9$ (and so by $3$). What is left,
$a + b + c$, is the digit sum. The number is divisible by $9$ exactly
when its digit sum is. What is more, the remainder of the number on
division by $9$ equals the remainder of its digit sum.

## Prime numbers

A number greater than $1$ whose only divisors are $1$ and itself is
called a **prime**: $2, 3, 5, 7, 11, 13, \dots$ A number greater than $1$
that is not prime is called **composite**: $4 = 2 \cdot 2$,
$6 = 2 \cdot 3$.

- **$1$ is not prime**: it has only one divisor. We will see why it is
  defined this way in a moment, with prime factorisation.
- **$2$ is the only even prime**: every even number larger than it is
  divisible by $2$ and so composite.

An old and lovely way to find primes is the **sieve of Eratosthenes**:
start from $2$ and cross out the multiples of each prime; whatever
survives is prime.

<figure class="fig">
<svg viewBox="0 0 440 248" width="440"><text class="dim" x="40.0" y="39.0" font-size="14" text-anchor="middle">1</text><rect class="dot" opacity="0.28" x="62" y="16" width="36" height="36" rx="5"/><rect class="curve" x="62" y="16" width="36" height="36" rx="5" style="stroke-width:1.6"/><text class="ink" x="80.0" y="39.0" font-size="14" text-anchor="middle">2</text><rect class="dot" opacity="0.28" x="102" y="16" width="36" height="36" rx="5"/><rect class="curve" x="102" y="16" width="36" height="36" rx="5" style="stroke-width:1.6"/><text class="ink" x="120.0" y="39.0" font-size="14" text-anchor="middle">3</text><rect class="box" x="142" y="16" width="36" height="36" rx="5"/><text class="dim" x="160.0" y="39.0" font-size="13" text-anchor="middle">4</text><rect class="dot" opacity="0.28" x="182" y="16" width="36" height="36" rx="5"/><rect class="curve" x="182" y="16" width="36" height="36" rx="5" style="stroke-width:1.6"/><text class="ink" x="200.0" y="39.0" font-size="14" text-anchor="middle">5</text><rect class="box" x="222" y="16" width="36" height="36" rx="5"/><text class="dim" x="240.0" y="39.0" font-size="13" text-anchor="middle">6</text><rect class="dot" opacity="0.28" x="262" y="16" width="36" height="36" rx="5"/><rect class="curve" x="262" y="16" width="36" height="36" rx="5" style="stroke-width:1.6"/><text class="ink" x="280.0" y="39.0" font-size="14" text-anchor="middle">7</text><rect class="box" x="302" y="16" width="36" height="36" rx="5"/><text class="dim" x="320.0" y="39.0" font-size="13" text-anchor="middle">8</text><rect class="box" x="342" y="16" width="36" height="36" rx="5"/><text class="dim" x="360.0" y="39.0" font-size="13" text-anchor="middle">9</text><rect class="box" x="382" y="16" width="36" height="36" rx="5"/><text class="dim" x="400.0" y="39.0" font-size="13" text-anchor="middle">10</text><rect class="dot" opacity="0.28" x="22" y="56" width="36" height="36" rx="5"/><rect class="curve" x="22" y="56" width="36" height="36" rx="5" style="stroke-width:1.6"/><text class="ink" x="40.0" y="79.0" font-size="14" text-anchor="middle">11</text><rect class="box" x="62" y="56" width="36" height="36" rx="5"/><text class="dim" x="80.0" y="79.0" font-size="13" text-anchor="middle">12</text><rect class="dot" opacity="0.28" x="102" y="56" width="36" height="36" rx="5"/><rect class="curve" x="102" y="56" width="36" height="36" rx="5" style="stroke-width:1.6"/><text class="ink" x="120.0" y="79.0" font-size="14" text-anchor="middle">13</text><rect class="box" x="142" y="56" width="36" height="36" rx="5"/><text class="dim" x="160.0" y="79.0" font-size="13" text-anchor="middle">14</text><rect class="box" x="182" y="56" width="36" height="36" rx="5"/><text class="dim" x="200.0" y="79.0" font-size="13" text-anchor="middle">15</text><rect class="box" x="222" y="56" width="36" height="36" rx="5"/><text class="dim" x="240.0" y="79.0" font-size="13" text-anchor="middle">16</text><rect class="dot" opacity="0.28" x="262" y="56" width="36" height="36" rx="5"/><rect class="curve" x="262" y="56" width="36" height="36" rx="5" style="stroke-width:1.6"/><text class="ink" x="280.0" y="79.0" font-size="14" text-anchor="middle">17</text><rect class="box" x="302" y="56" width="36" height="36" rx="5"/><text class="dim" x="320.0" y="79.0" font-size="13" text-anchor="middle">18</text><rect class="dot" opacity="0.28" x="342" y="56" width="36" height="36" rx="5"/><rect class="curve" x="342" y="56" width="36" height="36" rx="5" style="stroke-width:1.6"/><text class="ink" x="360.0" y="79.0" font-size="14" text-anchor="middle">19</text><rect class="box" x="382" y="56" width="36" height="36" rx="5"/><text class="dim" x="400.0" y="79.0" font-size="13" text-anchor="middle">20</text><rect class="box" x="22" y="96" width="36" height="36" rx="5"/><text class="dim" x="40.0" y="119.0" font-size="13" text-anchor="middle">21</text><rect class="box" x="62" y="96" width="36" height="36" rx="5"/><text class="dim" x="80.0" y="119.0" font-size="13" text-anchor="middle">22</text><rect class="dot" opacity="0.28" x="102" y="96" width="36" height="36" rx="5"/><rect class="curve" x="102" y="96" width="36" height="36" rx="5" style="stroke-width:1.6"/><text class="ink" x="120.0" y="119.0" font-size="14" text-anchor="middle">23</text><rect class="box" x="142" y="96" width="36" height="36" rx="5"/><text class="dim" x="160.0" y="119.0" font-size="13" text-anchor="middle">24</text><rect class="box" x="182" y="96" width="36" height="36" rx="5"/><text class="dim" x="200.0" y="119.0" font-size="13" text-anchor="middle">25</text><rect class="box" x="222" y="96" width="36" height="36" rx="5"/><text class="dim" x="240.0" y="119.0" font-size="13" text-anchor="middle">26</text><rect class="box" x="262" y="96" width="36" height="36" rx="5"/><text class="dim" x="280.0" y="119.0" font-size="13" text-anchor="middle">27</text><rect class="box" x="302" y="96" width="36" height="36" rx="5"/><text class="dim" x="320.0" y="119.0" font-size="13" text-anchor="middle">28</text><rect class="dot" opacity="0.28" x="342" y="96" width="36" height="36" rx="5"/><rect class="curve" x="342" y="96" width="36" height="36" rx="5" style="stroke-width:1.6"/><text class="ink" x="360.0" y="119.0" font-size="14" text-anchor="middle">29</text><rect class="box" x="382" y="96" width="36" height="36" rx="5"/><text class="dim" x="400.0" y="119.0" font-size="13" text-anchor="middle">30</text><rect class="dot" opacity="0.28" x="22" y="136" width="36" height="36" rx="5"/><rect class="curve" x="22" y="136" width="36" height="36" rx="5" style="stroke-width:1.6"/><text class="ink" x="40.0" y="159.0" font-size="14" text-anchor="middle">31</text><rect class="box" x="62" y="136" width="36" height="36" rx="5"/><text class="dim" x="80.0" y="159.0" font-size="13" text-anchor="middle">32</text><rect class="box" x="102" y="136" width="36" height="36" rx="5"/><text class="dim" x="120.0" y="159.0" font-size="13" text-anchor="middle">33</text><rect class="box" x="142" y="136" width="36" height="36" rx="5"/><text class="dim" x="160.0" y="159.0" font-size="13" text-anchor="middle">34</text><rect class="box" x="182" y="136" width="36" height="36" rx="5"/><text class="dim" x="200.0" y="159.0" font-size="13" text-anchor="middle">35</text><rect class="box" x="222" y="136" width="36" height="36" rx="5"/><text class="dim" x="240.0" y="159.0" font-size="13" text-anchor="middle">36</text><rect class="dot" opacity="0.28" x="262" y="136" width="36" height="36" rx="5"/><rect class="curve" x="262" y="136" width="36" height="36" rx="5" style="stroke-width:1.6"/><text class="ink" x="280.0" y="159.0" font-size="14" text-anchor="middle">37</text><rect class="box" x="302" y="136" width="36" height="36" rx="5"/><text class="dim" x="320.0" y="159.0" font-size="13" text-anchor="middle">38</text><rect class="box" x="342" y="136" width="36" height="36" rx="5"/><text class="dim" x="360.0" y="159.0" font-size="13" text-anchor="middle">39</text><rect class="box" x="382" y="136" width="36" height="36" rx="5"/><text class="dim" x="400.0" y="159.0" font-size="13" text-anchor="middle">40</text><rect class="dot" opacity="0.28" x="22" y="176" width="36" height="36" rx="5"/><rect class="curve" x="22" y="176" width="36" height="36" rx="5" style="stroke-width:1.6"/><text class="ink" x="40.0" y="199.0" font-size="14" text-anchor="middle">41</text><rect class="box" x="62" y="176" width="36" height="36" rx="5"/><text class="dim" x="80.0" y="199.0" font-size="13" text-anchor="middle">42</text><rect class="dot" opacity="0.28" x="102" y="176" width="36" height="36" rx="5"/><rect class="curve" x="102" y="176" width="36" height="36" rx="5" style="stroke-width:1.6"/><text class="ink" x="120.0" y="199.0" font-size="14" text-anchor="middle">43</text><rect class="box" x="142" y="176" width="36" height="36" rx="5"/><text class="dim" x="160.0" y="199.0" font-size="13" text-anchor="middle">44</text><rect class="box" x="182" y="176" width="36" height="36" rx="5"/><text class="dim" x="200.0" y="199.0" font-size="13" text-anchor="middle">45</text><rect class="box" x="222" y="176" width="36" height="36" rx="5"/><text class="dim" x="240.0" y="199.0" font-size="13" text-anchor="middle">46</text><rect class="dot" opacity="0.28" x="262" y="176" width="36" height="36" rx="5"/><rect class="curve" x="262" y="176" width="36" height="36" rx="5" style="stroke-width:1.6"/><text class="ink" x="280.0" y="199.0" font-size="14" text-anchor="middle">47</text><rect class="box" x="302" y="176" width="36" height="36" rx="5"/><text class="dim" x="320.0" y="199.0" font-size="13" text-anchor="middle">48</text><rect class="box" x="342" y="176" width="36" height="36" rx="5"/><text class="dim" x="360.0" y="199.0" font-size="13" text-anchor="middle">49</text><rect class="box" x="382" y="176" width="36" height="36" rx="5"/><text class="dim" x="400.0" y="199.0" font-size="13" text-anchor="middle">50</text><rect class="dot" opacity="0.28" x="30" y="225" width="14" height="14" rx="3"/><rect class="curve" x="30" y="225" width="14" height="14" rx="3" style="stroke-width:1.4"/><text class="ink" x="50" y="236" font-size="12" text-anchor="start">prime</text><rect class="box" x="140" y="225" width="14" height="14" rx="3"/><text class="ink" x="160" y="236" font-size="12" text-anchor="start">composite</text><text class="dim" x="270" y="236" font-size="12" text-anchor="start">1: neither</text></svg>
  <figcaption>The numbers from $1$ to $50$. After crossing out the multiples of $2$, then of $3$, $5$ and $7$, $15$ primes are left. Since $7 \cdot 7 = 49$, there is no need to sieve beyond $7$ up to $50$.</figcaption>
</figure>

**Is a number prime?** Divide $n$ by the primes **whose square does not
exceed $n$**. If none divides it, $n$ is prime. Why is that enough? If
$n = a \cdot b$, at least one of the factors stays on the small side: if
both were large, their product would exceed $n$. For $97$, checking $2,
3, 5, 7$ is enough ($11 \cdot 11 = 121 > 97$); none divides it, so $97$
is prime.

## Prime factorisation

Every composite number can be written as a product of primes. Build a
**factor tree**: split the number into any two factors, and keep
splitting the branches that are not prime.

<figure class="fig">
<svg viewBox="0 0 400 280" width="400"><line class="curve3" x1="200" y1="38" x2="120" y2="72"/><line class="curve3" x1="200" y1="38" x2="290" y2="72"/><line class="curve3" x1="120" y1="98" x2="70" y2="132"/><line class="curve3" x1="120" y1="98" x2="170" y2="132"/><line class="curve3" x1="290" y1="98" x2="255" y2="132"/><line class="curve3" x1="290" y1="98" x2="325" y2="132"/><line class="curve3" x1="70" y1="158" x2="40" y2="192"/><line class="curve3" x1="70" y1="158" x2="100" y2="192"/><line class="curve3" x1="170" y1="158" x2="145" y2="192"/><line class="curve3" x1="170" y1="158" x2="195" y2="192"/><rect class="box" x="177.5" y="12" width="45" height="28" rx="6"/><text class="ink" x="200" y="31" font-size="14" text-anchor="middle">360</text><rect class="box" x="102.0" y="72" width="36" height="28" rx="6"/><text class="ink" x="120" y="91" font-size="14" text-anchor="middle">36</text><rect class="box" x="272.0" y="72" width="36" height="28" rx="6"/><text class="ink" x="290" y="91" font-size="14" text-anchor="middle">10</text><rect class="box" x="56.5" y="132" width="27" height="28" rx="6"/><text class="ink" x="70" y="151" font-size="14" text-anchor="middle">4</text><rect class="box" x="156.5" y="132" width="27" height="28" rx="6"/><text class="ink" x="170" y="151" font-size="14" text-anchor="middle">9</text><circle class="dot" opacity="0.28" cx="255" cy="146" r="15"/><circle class="curve" cx="255" cy="146" r="15" style="stroke-width:1.6"/><text class="ink" x="255" y="151" font-size="14" text-anchor="middle">2</text><circle class="dot" opacity="0.28" cx="325" cy="146" r="15"/><circle class="curve" cx="325" cy="146" r="15" style="stroke-width:1.6"/><text class="ink" x="325" y="151" font-size="14" text-anchor="middle">5</text><circle class="dot" opacity="0.28" cx="40" cy="206" r="15"/><circle class="curve" cx="40" cy="206" r="15" style="stroke-width:1.6"/><text class="ink" x="40" y="211" font-size="14" text-anchor="middle">2</text><circle class="dot" opacity="0.28" cx="100" cy="206" r="15"/><circle class="curve" cx="100" cy="206" r="15" style="stroke-width:1.6"/><text class="ink" x="100" y="211" font-size="14" text-anchor="middle">2</text><circle class="dot" opacity="0.28" cx="145" cy="206" r="15"/><circle class="curve" cx="145" cy="206" r="15" style="stroke-width:1.6"/><text class="ink" x="145" y="211" font-size="14" text-anchor="middle">3</text><circle class="dot" opacity="0.28" cx="195" cy="206" r="15"/><circle class="curve" cx="195" cy="206" r="15" style="stroke-width:1.6"/><text class="ink" x="195" y="211" font-size="14" text-anchor="middle">3</text><text class="ink" x="200" y="250" font-size="13" text-anchor="middle">360 = 2 · 2 · 2 · 3 · 3 · 5 = 2³ · 3² · 5</text><text class="dim" x="200" y="268" font-size="11" text-anchor="middle">every leaf is prime</text></svg>
  <figcaption>We split $360$ as $36 \cdot 10$ and divided each branch until reaching primes. Starting elsewhere ($360 = 8 \cdot 45$, say) the tree would look different, but the leaves would still be three $2$s, two $3$s and one $5$.</figcaption>
</figure>

$$
360 = 2^3 \cdot 3^2 \cdot 5
$$

**The fundamental theorem of arithmetic:** this way of writing it is
**unique** (apart from the order of the factors). Whichever route you
take, you reach the same primes. That is why $1$ is not counted as a
prime: if it were, there would be endless ways of writing $360 = 1 \cdot
2^3 \cdot 3^2 \cdot 5 = 1 \cdot 1 \cdot 2^3 \cdot \dots$

The prime factors are a number's "identity". Its divisors can be read
off from them: every divisor of $360$ has the form $2^a \cdot 3^b \cdot
5^c$ with $a \in \{0,1,2,3\}$, $b \in \{0,1,2\}$, $c \in \{0,1\}$. The
number of choices:

$$
(3 + 1)(2 + 1)(1 + 1) = 4 \cdot 3 \cdot 2 = 24
$$

$360$ has $24$ divisors. The rule: **multiply each exponent plus one**.

## GCD: greatest common divisor

The largest number that divides both numbers. Take $84$ and $126$.

**With prime factors:** take the common primes with their **smaller**
exponents.

$$
84 = 2^2 \cdot 3 \cdot 7, \qquad 126 = 2 \cdot 3^2 \cdot 7
$$

The common primes are $2$, $3$, $7$; the smaller exponents give $2^1$,
$3^1$, $7^1$:

$$
\text{GCD}(84, 126) = 2 \cdot 3 \cdot 7 = 42
$$

**Euclid's algorithm:** divide the larger number by the smaller, then
carry on with the remainder. When the remainder is $0$, the last divisor
is the GCD.

$$
\begin{aligned}
126 &= 84 \cdot 1 + 42 \\
84 &= 42 \cdot 2 + 0
\end{aligned}
$$

The GCD is $42$. Why does it work? Every number that divides both $126$
and $84$ also divides their difference $42$; so the common divisors of
the pair $(126, 84)$ are the same as those of $(84, 42)$. The numbers
shrink while the GCD stays the same. For large numbers this is much
faster than factorising; it is what computers use.

Numbers whose GCD is $1$ are called **coprime**: $8$ and $15$, for
example. Neither is prime, but they share no prime factor.

## LCM: least common multiple

The smallest (non-zero) number that is a multiple of both.

**With prime factors:** take all the primes with their **larger**
exponents.

$$
\text{LCM}(84, 126) = 2^2 \cdot 3^2 \cdot 7 = 252
$$

**Check:** $252 = 84 \cdot 3 = 126 \cdot 2$ ✓.

For two numbers there is a nice link:

$$
\text{GCD}(a, b) \cdot \text{LCM}(a, b) = a \cdot b
$$

$42 \cdot 252 = 10\,584 = 84 \cdot 126$. That is because for each prime,
the smaller exponent plus the larger exponent equals the sum of the
exponents in the two numbers. If you know the GCD, the LCM takes one
division: $84 \cdot 126 \div 42 = 252$.

## Which one to use?

<figure class="fig">
  <div class="versus">
    <div class="ok">
      <h4>GCD</h4>
      <p>Splitting something into <b>equal, largest pieces</b></p>
      <p>Tiling a floor with the largest square tiles</p>
      <p>Simplifying a fraction</p>
      <p>The answer is <b>at most</b> the numbers</p>
    </div>
    <div class="ok">
      <h4>LCM</h4>
      <p>Two events happening <b>at the same time again</b></p>
      <p>Cycles of different lengths lining up</p>
      <p>Bringing fractions to a common denominator</p>
      <p>The answer is <b>at least</b> the numbers</p>
    </div>
  </div>
  <figcaption>If the question says "split, share, largest piece", it is GCD; if it says "repeat, line up, first common moment", it is LCM.</figcaption>
</figure>

**Example (LCM):** One bus leaves every $12$ minutes, another every $18$
minutes. They left together at $08{:}00$. They leave together at a
multiple of both times: $\text{LCM}(12, 18) = 36$. The next joint
departure is at $08{:}36$.

**Example (GCD):** $24$ apples and $36$ pears are to be shared among as
many plates as possible, with the same number of apples and the same
number of pears on each plate. The number of plates must divide both:
$\text{GCD}(24, 36) = 12$ plates, with $2$ apples and $3$ pears on each.

## Divisibility in machine learning

**Batch size.** To split a data set of $1\,000$ examples into equal
batches, the batch size must be a divisor of $1\,000$: $16$ does not
divide it ($1\,000 = 16 \cdot 62 + 8$, the last batch is short), $8$ and
$40$ do.

**Cutting an image into patches.** Some image models cut a $224 \times
224$ pixel picture into square $16 \times 16$ patches. Since $224 = 16
\cdot 14$, there are $14$ patches along each side, $14 \cdot 14 = 196$
in total. If the patch size did not divide the side, pixels would be
left over at the edge.

**Cycles lining up.** If a model is saved every $12$ epochs and the
learning rate is lowered every $18$ epochs, the two first happen together
at epoch $36$: the LCM.

## Common mistakes

- **Counting $1$ as prime.** A prime must have exactly two divisors; $1$
  has one.
- **Checking the rule for $6$ with the digit sum only.** To be divisible
  by $6$, a number must be divisible by both $3$ (digit sum) and $2$
  (even). $213$: the digit sum is $6$ but it is odd, so it is not
  divisible by $6$.
- **Mixing up GCD and LCM.** The GCD cannot be larger than the two
  numbers, and the LCM cannot be smaller. Check that your answer respects
  these limits.
- **Stopping the factor tree too early.** No composite number may remain
  among the leaves: $360 = 4 \cdot 9 \cdot 10$ is a factorisation but not
  a **prime** factorisation.

## Summary

- If $b = a \cdot k$, then $a$ is a divisor of $b$ and $b$ a multiple of $a$.
- Divisibility rules: $2, 5, 10$ last digit; $4$ last two; $8$ last three; $3, 9$ digit sum; $6$ = $2$ and $3$; $11$ alternating sum.
- A prime has exactly two divisors. $1$ is not prime, $2$ is the only even prime.
- Primality test: dividing by the primes whose square does not exceed the number is enough.
- Every number's prime factorisation is unique; the number of divisors is the product of the exponents plus one.
- GCD: common primes, smaller exponents; or Euclid's algorithm.
- LCM: all primes, larger exponents; $\text{GCD} \cdot \text{LCM} = a \cdot b$.
- Split, share → GCD; line up, same moment again → LCM.
