# Reading Mathematics: Symbols and Terms

Mathematics is a language. It has its own letters (numbers, variables),
its own words (operation symbols) and its own grammar (order of
operations, brackets). Most people who fear mathematics are not really
afraid of the calculations but of not being able to read this language:
they look at a formula, cannot tell what it says, and decide "this is not
for me".

This section works like a dictionary. It introduces, one by one, the
symbols and terms you will meet in every later section, and tells you how
each is **read** and what it **means**. You do not need to memorise
anything here; think of it as a place to come back to when you get stuck.

Prerequisite: none. This is the first section of the path.

## Numbers and number sets

In mathematics, numbers are grouped into **sets** by their properties.
Each set contains the one before it and allows something new.

| Symbol | Name | Contents | What does it add? |
|---|---|---|---|
| $\mathbb{N}$ | Natural numbers | $0, 1, 2, 3, \dots$ | Counting |
| $\mathbb{Z}$ | Integers | $\dots, -2, -1, 0, 1, 2, \dots$ | Negative numbers (debt, below zero) |
| $\mathbb{Q}$ | Rational numbers | $\tfrac{1}{2}$, $-\tfrac{3}{4}$, $0.75$ … | Fractions: the ratio of two integers |
| $\mathbb{R}$ | Real numbers | $\sqrt{2}$, $\pi$ … and all of the above | Every point of the number line |

<figure class="fig">
<svg viewBox="0 0 420 230" width="420"><rect class="curve3" x="8" y="8" width="404" height="214" rx="16"/><text class="ink" x="20" y="28" font-size="12" text-anchor="start">ℝ  Real</text><rect class="curve4" x="26" y="34" width="290" height="170" rx="16"/><text class="ink" x="38" y="54" font-size="12" text-anchor="start">ℚ  Rational</text><rect class="curve2" x="44" y="60" width="182" height="126" rx="16"/><text class="ink" x="56" y="80" font-size="12" text-anchor="start">ℤ  Integer</text><rect class="curve" x="62" y="86" width="84" height="82" rx="16"/><text class="ink" x="74" y="106" font-size="12" text-anchor="start">ℕ  Natural</text><text class="ink" x="84" y="136" font-size="14" text-anchor="middle">0</text><text class="ink" x="104" y="150" font-size="14" text-anchor="middle">1</text><text class="ink" x="124" y="136" font-size="14" text-anchor="middle">7</text><text class="ink" x="170" y="120" font-size="14" text-anchor="middle">−3</text><text class="ink" x="170" y="156" font-size="14" text-anchor="middle">−1</text><text class="ink" x="258" y="104" font-size="14" text-anchor="middle">1/2</text><text class="ink" x="262" y="150" font-size="14" text-anchor="middle">−0.75</text><text class="ink" x="258" y="184" font-size="14" text-anchor="middle">2/3</text><text class="ink" x="358" y="90" font-size="14" text-anchor="middle">√2</text><text class="ink" x="360" y="136" font-size="14" text-anchor="middle">π</text><text class="ink" x="356" y="182" font-size="14" text-anchor="middle">−√5</text></svg>
  <figcaption>The number sets sit inside each other: every natural number is an integer, every integer is a rational number, every rational number is a real number. Numbers like $\sqrt{2}$ and $\pi$ are real but not rational: no fraction writes them exactly.</figcaption>
</figure>

Numbers such as $\sqrt{2}$ or $\pi$, which are real but cannot be written
as a fraction, are called **irrational**. Their decimal expansions never
end and never repeat: $\pi = 3.14159265\dots$

**Note:** Some books start the natural numbers at $1$ and leave $0$ out.
In the Turkish curriculum $0$ is a natural number, and $1, 2, 3, \dots$ are
called the **counting numbers**.

### Set symbols

| Symbol | Read as | Example |
|---|---|---|
| $\in$ | "is an element of" | $3 \in \mathbb{N}$: 3 is a natural number |
| $\notin$ | "is not an element of" | $-3 \notin \mathbb{N}$ |
| $\subset$ | "is a subset of" | $\mathbb{N} \subset \mathbb{Z}$ |
| $\{\ \}$ | set braces | $\{1, 2, 3\}$: the set of 1, 2 and 3 |

We will study sets in detail in the Sets and Logic section; for now being
able to read them is enough.

## Variables and constants

When we do not know the value of a number, or want to say something that
holds for **every** number, we write a letter in its place. This letter is
called a **variable**.

- Instead of "three more than a number", $x + 3$.
- Instead of "for every number, adding 0 does not change it", $a + 0 = a$.

Letters whose value stays fixed are called **constants**: $\pi \approx
3.14159$ never changes. When a problem says "$a$ is a constant", it means
$a$ is a definite number that has not been told to us.

The choice of letters is arbitrary, but there are conventions:

| Letters | Usually used for |
|---|---|
| $x, y, z$ | Unknowns, variables |
| $a, b, c$ | Constants, coefficients |
| $n, m, k$ | Whole numbers, counts ("$n$ of them") |
| $i, j$ | Position numbers (1st, 2nd, 3rd element) |
| $f, g, h$ | Functions |
| $t$ | Time |

### Greek letters

When Latin letters are not enough, the Greek alphabet is used. The ones
you will meet most in machine learning:

| Letter | Read as | Typical use |
|---|---|---|
| $\alpha$ | alpha | Learning rate, angle |
| $\beta$ | beta | Coefficients, weights |
| $\gamma$ | gamma | Discount factor |
| $\delta$, $\Delta$ | delta | Small change, difference ($\Delta x$: "the change in $x$") |
| $\varepsilon$ | epsilon | A very small number, error |
| $\theta$ | theta | Angle, the parameters of a model |
| $\lambda$ | lambda | Regularisation coefficient, eigenvalue |
| $\mu$ | mu | Mean |
| $\pi$ | pi | $3.14159\dots$ (a circle's circumference / diameter) |
| $\sigma$, $\Sigma$ | sigma | Standard deviation; the capital is the sum symbol |
| $\varphi$ | phi | Angle, special functions |

The lower-case and capital forms of a letter often mean different things:
$\sigma$ is the standard deviation, $\Sigma$ the sum symbol.

## Operation symbols

| Symbol | Read as | Example |
|---|---|---|
| $+$ | plus | $5 + 3 = 8$ |
| $-$ | minus | $5 - 3 = 2$ |
| $\times$, $\cdot$ | times | $5 \times 3 = 5 \cdot 3 = 15$ |
| $\div$, $/$, fraction bar | divided by | $15 \div 3 = 15/3 = \tfrac{15}{3} = 5$ |
| $a^n$ | "$a$ to the power $n$", "$a$ to the $n$th" | $2^3 = 2 \cdot 2 \cdot 2 = 8$ |
| $\sqrt{a}$ | "square root of $a$" | $\sqrt{9} = 3$ |
| $\lvert a \rvert$ | "the absolute value of $a$" | $\lvert -4 \rvert = 4$ |

### Writing side by side means multiplying

When working with letters, the multiplication sign is usually left out:

$$
2x = 2 \cdot x
\qquad
ab = a \cdot b
\qquad
3(x + 1) = 3 \cdot (x + 1)
$$

**Careful:** This rule only applies with letters. $23$ is not "2 times 3",
it is the number twenty-three. $2x$ is "2 times $x$"; if $x = 5$, then $2x
= 10$, not $25$.

In algebra a dot ($\cdot$) is preferred so that $\times$ is not confused
with the letter $x$.

### The fraction bar is a bracket

$$
\frac{6 + 4}{2} = \frac{10}{2} = 5
$$

Everything above and below the fraction bar is calculated first on its
own. When the same expression is written on one line, brackets are
essential: $(6 + 4) / 2 = 5$, but $6 + 4 / 2 = 6 + 2 = 8$.

### Brackets

$(\ )$, $[\ ]$ and $\{\ \}$ are used for grouping; in nested brackets
different kinds are chosen to make reading easier:

$$
2 \cdot [3 + (4 - 1)] = 2 \cdot [3 + 3] = 2 \cdot 6 = 12
$$

You work from the innermost bracket outwards. We will see which operation
comes first in detail in the next section (Order of Operations).

## Relation symbols

These symbols say **how two things compare**; the result is not a number
but a sentence that is true or false.

| Symbol | Read as | Example |
|---|---|---|
| $=$ | equals | $2 + 3 = 5$ |
| $\ne$ | is not equal to | $2 + 3 \ne 6$ |
| $<$ | is less than | $3 < 5$ |
| $>$ | is greater than | $5 > 3$ |
| $\le$ | is less than or equal to | $x \le 10$: $x$ is at most 10 |
| $\ge$ | is greater than or equal to | $x \ge 0$: $x$ is not negative |
| $\approx$ | is approximately equal to | $\pi \approx 3.14$ |
| $\Rightarrow$ | implies, then | $x = 2 \Rightarrow x^2 = 4$ |
| $\iff$ | if and only if | $x + 1 = 3 \iff x = 2$ |

**To keep $<$ and $>$ apart:** the open mouth of the symbol always faces
the **larger** number. In $3 < 5$ the mouth opens towards 5.

**A chain inequality:** $-2 < x \le 3$ means "$x$ is greater than $-2$ and
less than or equal to $3$". The integers satisfying it are $-1, 0, 1, 2,
3$.

**$\Rightarrow$ goes one way.** $x = 2 \Rightarrow x^2 = 4$ is true, but not
the reverse: if $x^2 = 4$, $x$ could also be $-2$.

## Expression, term, coefficient: the parts of a formula

<figure class="fig">
<svg viewBox="0 0 400 176" width="400"><text class="ink" x="85" y="118" font-size="34" text-anchor="middle">3</text><text class="ink" x="110" y="118" font-size="34" text-anchor="middle">x</text><text class="ink" x="165" y="118" font-size="34" text-anchor="middle">−</text><text class="ink" x="205" y="118" font-size="34" text-anchor="middle">5</text><text class="ink" x="230" y="118" font-size="34" text-anchor="middle">x</text><text class="ink" x="275" y="118" font-size="34" text-anchor="middle">+</text><text class="ink" x="320" y="118" font-size="34" text-anchor="middle">7</text><text class="ink" x="130" y="100" font-size="18" text-anchor="middle">2</text><line class="curve" x1="85" y1="58" x2="85" y2="84"/><text class="ink" x="85" y="50" font-size="12" text-anchor="middle">coefficient</text><line class="curve2" x1="130" y1="38" x2="130" y2="80"/><text class="ink" x="130" y="30" font-size="12" text-anchor="middle">exponent</text><line class="curve4" x1="230" y1="58" x2="230" y2="90"/><text class="ink" x="230" y="50" font-size="12" text-anchor="middle">variable</text><path class="curve3" d="M68,132 v8 H142 v-8" fill="none"/><text class="ink" x="105.0" y="162" font-size="12" text-anchor="middle">term 1</text><path class="curve3" d="M152,132 v8 H248 v-8" fill="none"/><text class="ink" x="200.0" y="162" font-size="12" text-anchor="middle">term 2</text><path class="curve3" d="M262,132 v8 H338 v-8" fill="none"/><text class="ink" x="300.0" y="162" font-size="12" text-anchor="middle">constant term</text></svg>
  <figcaption>The expression $3x^2 - 5x + 7$ has three terms. In a term, the number in front of the letter is the coefficient (purple) and the small number at the letter's top right is the exponent (orange). A term with no letter is called the constant term.</figcaption>
</figure>

| Term | Meaning | Example |
|---|---|---|
| **Expression** | A piece of writing made of numbers, letters and operations; no equals sign | $3x^2 - 5x + 7$ |
| **Term** | The parts of an expression separated by $+$ and $-$ | $3x^2$, $-5x$, $7$ |
| **Coefficient** | The number multiplying the letter in a term | $3$ in $3x^2$; $-5$ in $-5x$ |
| **Constant term** | The term with no letter | $7$ |
| **Equation** | A sentence saying two expressions are equal | $2x + 1 = 7$ |
| **Inequality** | A sentence saying one is larger or smaller than the other | $2x + 1 < 7$ |
| **Formula** | An equality computing one quantity from others | Area of a rectangle $A = a \cdot b$ |
| **Identity** | An equality true for every value | $a + b = b + a$ |

**The coefficient's sign belongs to the term:** in $3x^2 - 5x + 7$ the
coefficient of $x$ is $-5$, not $5$. Think of the expression as $3x^2 +
(-5x) + 7$.

**The coefficient of $x$ is 1:** when $x$ is written alone, there is an
invisible $1$ in front of it; the coefficient of $-x$ is $-1$.

### Substituting a value

To find the value of an expression, we write the number in place of the
letter. For $x = 2$:

$$
\begin{aligned}
3x^2 - 5x + 7 &= 3 \cdot 2^2 - 5 \cdot 2 + 7 \\
&= 3 \cdot 4 - 10 + 7 \\
&= 12 - 10 + 7 = 9
\end{aligned}
$$

When substituting a negative number, **use brackets**: for $x = -2$,
$3 \cdot (-2)^2 - 5 \cdot (-2) + 7 = 12 + 10 + 7 = 29$.

### Expression versus equation

An expression is like a **noun**: it describes something but makes no
claim. An equation is a **sentence**: it says "these two are equal", which
may be true or false. $2x + 1$ is an expression; $2x + 1 = 7$ is an
equation, true only when $x = 3$. We **simplify** or **evaluate**
expressions; we **solve** equations.

## Superscripts and subscripts

The small number at a letter's **top right** is an exponent; the small
number at its **bottom right** is a **subscript** (index):

| Written | Read as | Meaning |
|---|---|---|
| $x^2$ | "$x$ squared" | $x \cdot x$ |
| $x_2$ | "$x$ two", "$x$ sub two" | the **second** of the variables called $x$ |
| $x_i$ | "$x$ sub $i$" | the $i$-th element |
| $a_{ij}$ | "$a$ sub $i$ $j$" | the entry in row $i$, column $j$ of a table |

A subscript does no calculation; it is only a **name**. We might call the
prices of five houses $x_1, x_2, x_3, x_4, x_5$; $x_3$ is the price of the
third house. With many elements, "and so on" is said with three dots:
$x_1, x_2, \dots, x_n$ means "from $x_1$ to $x_n$, $n$ of them".

## The sum symbol Σ

A capital sigma is used to add up many terms:

$$
\sum_{i=1}^{4} x_i = x_1 + x_2 + x_3 + x_4
$$

Read it as: "the sum of $x_i$ for $i$ from 1 to 4". The $i = 1$ below says
where it starts, the $4$ above where it ends. An example:

$$
\sum_{i=1}^{4} i = 1 + 2 + 3 + 4 = 10
$$

This symbol is everywhere in machine learning; we will see it in detail
in the Sequences and Series section.

## Function notation

$f(x) = 2x + 1$ says: "there is a rule called $f$; give it an $x$ and it
gives you $2x + 1$". $f(3)$ means giving the rule $3$:

$$
f(3) = 2 \cdot 3 + 1 = 7
$$

**Careful:** $f(x)$ is **not** "$f$ times $x$". Here the brackets show the
input given to the rule. We will study functions in their own section.

## Reading formulas aloud

The best way to understand a formula is to read it aloud.

| Formula | Read as |
|---|---|
| $x^2 + y^2 = r^2$ | "$x$ squared plus $y$ squared equals $r$ squared" |
| $\frac{a + b}{2}$ | "$a$ plus $b$, over two" (half of $a + b$) |
| $\lvert x - 3 \rvert \le 1$ | "the absolute value of $x$ minus 3 is at most 1" |
| $x_1 + x_2 + \cdots + x_n$ | "$x$ one plus $x$ two plus … plus $x$ $n$" |
| $f(x) = 3x - 1$ | "$f$ of $x$ equals 3 $x$ minus 1" |

## Reading a formula in machine learning

The prediction of a linear model:

$$
\hat{y} = w_1 x_1 + w_2 x_2 + b
$$

Piece by piece:

- $\hat{y}$ ("$y$ hat"): the model's **prediction**. The hat means
  "estimated"; the true value is $y$ without a hat.
- $x_1, x_2$: features of a house, for example square metres and number
  of rooms.
- $w_1, w_2$: the **weight** of each feature: how much that feature
  contributes to the prediction.
- $b$: the constant term (bias).

If $w_1 = 2$, $w_2 = 10$, $b = 5$ and a house has $x_1 = 100$, $x_2 = 3$:

$$
\hat{y} = 2 \cdot 100 + 10 \cdot 3 + 5 = 200 + 30 + 5 = 235
$$

And an error measure, the **mean squared error**:

$$
\frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2
$$

"One over $n$ times the sum, for $i$ from 1 to $n$, of the squares of $y_i$
minus $\hat{y}_i$". That is: for each example take the difference between
the true value and the prediction, square it, add them all up, divide by
the number of examples. If you can read that sentence, you can read the
formula.

## Common mistakes

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Wrong</h4>
      <p>$x^2$ and $x_2$ are the same</p>
      <p>With $x = 5$, $2x = 25$</p>
      <p>$f(x)$ = $f$ times $x$</p>
      <p>In $3x^2 - 5x$ the coefficient of $x$ is $5$</p>
    </div>
    <div class="ok">
      <h4>Right</h4>
      <p>$x^2 = x \cdot x$; $x_2$ is the second $x$</p>
      <p>$2x = 2 \cdot 5 = 10$</p>
      <p>$f(x)$: the value the rule $f$ gives for $x$</p>
      <p>The coefficient with its sign: $-5$</p>
    </div>
  </div>
  <figcaption>The symbols are small but the differences are big: a superscript is an operation, a subscript is a name.</figcaption>
</figure>

- **Substituting a negative number without brackets.** For $x = -3$, $x^2$
  is $(-3)^2 = 9$; writing $-3^2$ reads as $-9$.
- **Using $=$ to mean "then".** $2 + 3 = 5 \cdot 2 = 10$ is wrong writing,
  because $2 + 3 \ne 10$. Both sides of every $=$ must really be equal;
  write intermediate results on separate lines.
- **Reading $<$ and $>$ backwards.** The open mouth faces the larger
  number.

## Summary

- The number sets sit inside each other: $\mathbb{N} \subset \mathbb{Z} \subset \mathbb{Q} \subset \mathbb{R}$; $\sqrt{2}$, $\pi$ are irrational.
- Variable: a letter whose value is unknown or can be anything; constant: one that does not change.
- Writing side by side means multiplying: $2x = 2 \cdot x$, $3(x + 1) = 3 \cdot (x + 1)$.
- The fraction bar behaves like a bracket.
- Relation symbols ($=, \ne, <, >, \le, \ge, \approx$) make a sentence that is true or false.
- Expression: made of terms; a term has a coefficient (with its sign), a variable and an exponent. Equation: two expressions set equal.
- A superscript is an operation ($x^2$), a subscript is a name ($x_2$).
- $\sum_{i=1}^{n} x_i$: add from $x_1$ to $x_n$. $f(x)$: give $x$ to the rule $f$.
- Read ML formulas piece by piece and aloud: $\hat{y} = w_1x_1 + w_2x_2 + b$.
