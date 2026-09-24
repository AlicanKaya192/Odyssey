# Fractions

Three quarters of a pizza, two fifths of a class, eighty per cent of a
data set… We use fractions to describe a **part** of a whole.
Probabilities, ratios, averages and many of the numbers in machine
learning are really fractions. In this section we will see what a
fraction is, equivalent fractions, simplifying, and the four operations
together with **why** they are done the way they are.

Prerequisite: the Divisibility, Primes, GCD and LCM section.

## What is a fraction?

The fraction $\dfrac{a}{b}$ means cutting a whole into $b$ equal parts
and taking $a$ of them. The top number is the **numerator**, the bottom
one the **denominator**:

$$
\frac{3}{4} \quad \leftarrow \quad \begin{aligned} &\text{numerator: how many parts are taken} \\ &\text{denominator: how many parts the whole is cut into} \end{aligned}
$$

A fraction is also a **division**: $\dfrac{3}{4} = 3 \div 4$. That is why
the denominator **cannot be zero**; division by zero is undefined.

**Kinds of fraction:**

| Kind | Meaning | Example |
|---|---|---|
| Proper fraction | numerator smaller than denominator, value less than $1$ | $\dfrac{3}{4}$ |
| Improper fraction | numerator equal to or larger than denominator | $\dfrac{7}{3}$ |
| Mixed number | a whole number plus a proper fraction | $2\tfrac{1}{3}$ |

An improper fraction and a mixed number are two ways of writing the same
number. $7 \div 3 = 2$ remainder $1$: so $\dfrac{7}{3} = 2\tfrac{1}{3}$.
To convert back, $2\tfrac{1}{3} = \dfrac{2 \cdot 3 + 1}{3} = \dfrac{7}{3}$.

Every whole number is a fraction with denominator $1$: $5 = \dfrac{5}{1}$.

## Equivalent fractions and simplifying

<figure class="fig">
<svg viewBox="0 0 520 158" width="520"><rect class="dot" opacity="0.55" x="70.0" y="16" width="75.0" height="34"/><rect class="curve3" x="70.0" y="16" width="75.0" height="34"/><rect class="dot" opacity="0.55" x="145.0" y="16" width="75.0" height="34"/><rect class="curve3" x="145.0" y="16" width="75.0" height="34"/><rect class="dot" opacity="0.55" x="220.0" y="16" width="75.0" height="34"/><rect class="curve3" x="220.0" y="16" width="75.0" height="34"/><rect class="curve3" x="295.0" y="16" width="75.0" height="34"/><text class="ink" x="56" y="39.0" font-size="15" text-anchor="end">3/4</text><text class="dim" x="380" y="38.0" font-size="11" text-anchor="start">3 of 4 equal parts</text><rect class="dot" opacity="0.55" x="70.0" y="76" width="37.5" height="34"/><rect class="curve3" x="70.0" y="76" width="37.5" height="34"/><rect class="dot" opacity="0.55" x="107.5" y="76" width="37.5" height="34"/><rect class="curve3" x="107.5" y="76" width="37.5" height="34"/><rect class="dot" opacity="0.55" x="145.0" y="76" width="37.5" height="34"/><rect class="curve3" x="145.0" y="76" width="37.5" height="34"/><rect class="dot" opacity="0.55" x="182.5" y="76" width="37.5" height="34"/><rect class="curve3" x="182.5" y="76" width="37.5" height="34"/><rect class="dot" opacity="0.55" x="220.0" y="76" width="37.5" height="34"/><rect class="curve3" x="220.0" y="76" width="37.5" height="34"/><rect class="dot" opacity="0.55" x="257.5" y="76" width="37.5" height="34"/><rect class="curve3" x="257.5" y="76" width="37.5" height="34"/><rect class="curve3" x="295.0" y="76" width="37.5" height="34"/><rect class="curve3" x="332.5" y="76" width="37.5" height="34"/><text class="ink" x="56" y="99.0" font-size="15" text-anchor="end">6/8</text><text class="dim" x="380" y="98.0" font-size="11" text-anchor="start">6 of 8 equal parts</text><line class="curve2" stroke-dasharray="4 3" x1="295.0" y1="8" x2="295.0" y2="118"/><text class="ink" x="220.0" y="146" font-size="13" text-anchor="middle">the same length: 3/4 = 6/8</text></svg>
  <figcaption>The top bar is cut into $4$ parts with $3$ shaded; the bottom one into $8$ parts with $6$ shaded. The shaded length is the same: $\tfrac{3}{4}$ and $\tfrac{6}{8}$ are the same number. Cutting each part in two multiplied both the numerator and the denominator by two.</figcaption>
</figure>

Multiplying or dividing the numerator and denominator by **the same
number** (not zero) does not change the value of a fraction:

$$
\frac{a}{b} = \frac{a \cdot k}{b \cdot k}
$$

Expanding (multiplying) is used to bring fractions to a common
denominator, **simplifying** (dividing) to make the numbers smaller. For
the simplest form, divide the numerator and denominator by their
**GCD**:

$$
\frac{84}{126} = \frac{84 \div 42}{126 \div 42} = \frac{2}{3}
$$

If you cannot see the GCD straight away, you can simplify in steps: by
$2$, then $3$, then $7$. The result is the same.

## Comparing fractions

- **Same denominators:** the one with the larger numerator is larger:
  $\dfrac{5}{8} > \dfrac{3}{8}$.
- **Same numerators:** the one with the smaller denominator is larger:
  $\dfrac{3}{4} > \dfrac{3}{5}$ (cutting the whole into fewer parts makes
  each part bigger).
- **In general:** bring them to a common denominator, or
  **cross-multiply**.

$$
\frac{5}{7} \;\; ? \;\; \frac{2}{3} \qquad 5 \cdot 3 = 15, \quad 2 \cdot 7 = 14 \qquad 15 > 14 \;\Rightarrow\; \frac{5}{7} > \frac{2}{3}
$$

Cross-multiplying really brings them to the common denominator $21$: we
are comparing $\dfrac{15}{21}$ and $\dfrac{14}{21}$.

## Addition and subtraction

With the same denominator, add the numerators and keep the denominator:
$\dfrac{2}{7} + \dfrac{3}{7} = \dfrac{5}{7}$. We are counting parts of the
same size.

With different denominators the parts have different sizes; first we
must bring them to a **common denominator**.

<figure class="fig">
<svg viewBox="0 0 480 282" width="480"><rect class="dot" opacity="0.55" x="70.0" y="14" width="150.0" height="34"/><rect class="curve3" x="70.0" y="14" width="150.0" height="34"/><rect class="curve3" x="220.0" y="14" width="150.0" height="34"/><text class="ink" x="56" y="37.0" font-size="15" text-anchor="end">1/2</text><rect class="dot2" opacity="0.55" x="70.0" y="60" width="100.0" height="34"/><rect class="curve3" x="70.0" y="60" width="100.0" height="34"/><rect class="curve3" x="170.0" y="60" width="100.0" height="34"/><rect class="curve3" x="270.0" y="60" width="100.0" height="34"/><text class="ink" x="56" y="83.0" font-size="15" text-anchor="end">1/3</text><text class="dim" x="220.0" y="118" font-size="12" text-anchor="middle">↓ cut into sixths</text><rect class="dot" opacity="0.55" x="70.0" y="132" width="50.0" height="34"/><rect class="curve3" x="70.0" y="132" width="50.0" height="34"/><rect class="dot" opacity="0.55" x="120.0" y="132" width="50.0" height="34"/><rect class="curve3" x="120.0" y="132" width="50.0" height="34"/><rect class="dot" opacity="0.55" x="170.0" y="132" width="50.0" height="34"/><rect class="curve3" x="170.0" y="132" width="50.0" height="34"/><rect class="curve3" x="220.0" y="132" width="50.0" height="34"/><rect class="curve3" x="270.0" y="132" width="50.0" height="34"/><rect class="curve3" x="320.0" y="132" width="50.0" height="34"/><text class="ink" x="56" y="155.0" font-size="15" text-anchor="end">3/6</text><rect class="dot2" opacity="0.55" x="70.0" y="178" width="50.0" height="34"/><rect class="curve3" x="70.0" y="178" width="50.0" height="34"/><rect class="dot2" opacity="0.55" x="120.0" y="178" width="50.0" height="34"/><rect class="curve3" x="120.0" y="178" width="50.0" height="34"/><rect class="curve3" x="170.0" y="178" width="50.0" height="34"/><rect class="curve3" x="220.0" y="178" width="50.0" height="34"/><rect class="curve3" x="270.0" y="178" width="50.0" height="34"/><rect class="curve3" x="320.0" y="178" width="50.0" height="34"/><text class="ink" x="56" y="201.0" font-size="15" text-anchor="end">2/6</text><rect class="dot" opacity="0.55" x="70.0" y="236" width="50.0" height="34"/><rect class="curve3" x="70.0" y="236" width="50.0" height="34"/><rect class="dot" opacity="0.55" x="120.0" y="236" width="50.0" height="34"/><rect class="curve3" x="120.0" y="236" width="50.0" height="34"/><rect class="dot" opacity="0.55" x="170.0" y="236" width="50.0" height="34"/><rect class="curve3" x="170.0" y="236" width="50.0" height="34"/><rect class="curve3" x="220.0" y="236" width="50.0" height="34"/><rect class="curve3" x="270.0" y="236" width="50.0" height="34"/><rect class="curve3" x="320.0" y="236" width="50.0" height="34"/><rect class="curve3" x="70.0" y="236" width="50.0" height="34"/><rect class="curve3" x="120.0" y="236" width="50.0" height="34"/><rect class="curve3" x="170.0" y="236" width="50.0" height="34"/><rect class="dot2" opacity="0.55" x="220.0" y="236" width="50.0" height="34"/><rect class="curve3" x="220.0" y="236" width="50.0" height="34"/><rect class="dot2" opacity="0.55" x="270.0" y="236" width="50.0" height="34"/><rect class="curve3" x="270.0" y="236" width="50.0" height="34"/><rect class="curve3" x="320.0" y="236" width="50.0" height="34"/><text class="ink" x="56" y="259.0" font-size="15" text-anchor="end">5/6</text><text class="dim" x="382" y="258.0" font-size="12" text-anchor="start">= 3/6 + 2/6</text></svg>
  <figcaption>A half and a third cannot be added directly, their parts have different sizes. Cutting both into sixths, the half becomes $3$ parts and the third $2$; the total is $5$ sixths.</figcaption>
</figure>

$$
\frac{1}{2} + \frac{1}{3} = \frac{3}{6} + \frac{2}{6} = \frac{5}{6}
$$

The best common denominator is the **LCM** of the denominators. For
$\dfrac{5}{12} + \dfrac{7}{18}$, $\text{LCM}(12, 18) = 36$:

$$
\frac{5}{12} + \frac{7}{18} = \frac{15}{36} + \frac{14}{36} = \frac{29}{36}
$$

Multiplying the denominators ($12 \cdot 18 = 216$) also gives the right
answer, but the numbers grow and you have to simplify at the end.

**With mixed numbers**, either convert to improper fractions or add the
whole parts and the fraction parts separately: $2\tfrac{1}{3} +
1\tfrac{1}{2} = 3 + \tfrac{5}{6} = 3\tfrac{5}{6}$.

## Multiplication

Multiply the numerators, multiply the denominators:

$$
\frac{a}{b} \cdot \frac{c}{d} = \frac{a \cdot c}{b \cdot d}
$$

$\dfrac{2}{3} \cdot \dfrac{3}{4}$: "two thirds of three quarters". Cutting
a square into $4$ across and $3$ down gives $12$ small pieces; $2$ rows of
$3$ columns are $6$ pieces: $\dfrac{6}{12} = \dfrac{1}{2}$.

**Simplify first, then multiply.** Cancelling common factors between a
numerator and a denominator before multiplying keeps the numbers small:

$$
\frac{2}{3} \cdot \frac{3}{4} = \frac{2 \cdot \cancel{3}}{\cancel{3} \cdot 4} = \frac{2}{4} = \frac{1}{2}
$$

**"Of" means "times".** "$\dfrac{2}{3}$ of $12$" means $\dfrac{2}{3}
\cdot 12 = 8$: divide $12$ by $3$ ($4$) and take $2$ of them ($8$).

## Division

Dividing by a fraction means multiplying by its **reciprocal**:

$$
\frac{a}{b} \div \frac{c}{d} = \frac{a}{b} \cdot \frac{d}{c}
$$

Why? $3 \div \dfrac{1}{4}$ asks "how many quarters are there in $3$?"
Each whole has $4$ quarters, so $3$ wholes have $12$: $3 \div \dfrac{1}{4}
= 3 \cdot 4 = 12$. Dividing by a small number makes the result **larger**.

$$
\frac{3}{4} \div \frac{9}{8} = \frac{3}{4} \cdot \frac{8}{9} = \frac{24}{36} = \frac{2}{3}
$$

**Check:** $\dfrac{2}{3} \cdot \dfrac{9}{8} = \dfrac{18}{24} =
\dfrac{3}{4}$ ✓. Division reverses multiplication.

## Order of operations with fractions

The rules do not change: brackets, exponents, multiplication and
division, addition and subtraction. A fraction bar acts like a bracket:
its top and bottom are worked out separately.

$$
\begin{aligned}
\frac{1}{2} + \frac{2}{3} \cdot \frac{9}{4} &= \frac{1}{2} + \frac{3}{2} \\
&= \frac{4}{2} = 2
\end{aligned}
$$

Multiplication first ($\tfrac{2}{3} \cdot \tfrac{9}{4} = \tfrac{18}{12} = \tfrac{3}{2}$), then addition.

## Fractions in machine learning

**Accuracy.** A model that gets $45$ of $60$ examples right has accuracy
$\dfrac{45}{60} = \dfrac{3}{4}$.

**Probabilities.** A classifier might give probabilities $\dfrac{1}{2}$,
$\dfrac{1}{3}$ and $\dfrac{1}{6}$ to three classes. The probabilities must
add up to $1$: $\dfrac{3}{6} + \dfrac{2}{6} + \dfrac{1}{6} = 1$ ✓.

**Splitting data.** $\dfrac{4}{5}$ of the data goes to training and
$\dfrac{1}{5}$ to testing. With $1\,000$ examples: $800$ for training,
$200$ for testing.

## Common mistakes

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Wrong</h4>
      <p>$\dfrac{1}{2} + \dfrac{1}{3} = \dfrac{2}{5}$</p>
      <p>$\dfrac{2 + 3}{2 + 5} = \dfrac{3}{5}$</p>
      <p>$\dfrac{3}{4} \div \dfrac{1}{2} = \dfrac{3}{8}$</p>
      <p>$2\tfrac{1}{3} = \dfrac{2}{3}$</p>
    </div>
    <div class="ok">
      <h4>Right</h4>
      <p>$\dfrac{1}{2} + \dfrac{1}{3} = \dfrac{5}{6}$</p>
      <p>$\dfrac{2 + 3}{2 + 5} = \dfrac{5}{7}$</p>
      <p>$\dfrac{3}{4} \div \dfrac{1}{2} = \dfrac{3}{4} \cdot 2 = \dfrac{3}{2}$</p>
      <p>$2\tfrac{1}{3} = \dfrac{7}{3}$</p>
    </div>
  </div>
  <figcaption>In addition, numerators and denominators are not added separately; cancelling only works between factors.</figcaption>
</figure>

- **Adding numerators and denominators.** $\dfrac{1}{2} + \dfrac{1}{3}$
  cannot be $\dfrac{2}{5}$: $\dfrac{2}{5}$ is smaller than $\dfrac{1}{2}$
  alone!
- **Cancelling terms of a sum.** In $\dfrac{2 + 3}{2 + 5}$ the $2$s do not
  cancel; $2$ is a term, not a factor. Work out the top and the bottom
  first.
- **Flipping the wrong fraction in division.** It is the **divisor** (the
  second fraction) that gets flipped, not the dividend.

## Summary

- $\dfrac{a}{b}$: cut the whole into $b$ parts and take $a$; it equals $a \div b$; $b \ne 0$.
- Multiplying or dividing top and bottom by the same number keeps the value; for the simplest form divide by the GCD.
- Comparing: common denominator or cross-multiplying.
- Addition and subtraction: bring to a common denominator (LCM), add the numerators.
- Multiplication: multiply tops and bottoms; cancel first.
- Division: multiply by the reciprocal of the divisor.
- Mixed number: $2\tfrac{1}{3} = \dfrac{7}{3}$.
- Cancelling only between factors; terms inside a sum do not cancel.
