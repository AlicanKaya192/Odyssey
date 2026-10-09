# Overall Review

The Foundational Mathematics module ends here. You started by reading numbers; you calculated with
fractions, powers and roots, set up equations with algebra, drew
relationships with functions, measured shapes with geometry and
trigonometry, and put uncertainty into numbers with counting, probability
and statistics. This section teaches no new topic: it shows how the parts
connect, uses them all together in one problem, and gathers the most common
traps in a single list. The quiz and the problems are mixed from the whole
module.

## How do the parts connect?

The topics of the Foundational Mathematics module advance along four branches, and all of them flow into
the Advanced Mathematics module.

<figure class="fig">
  <div class="flow">
    <span class="node"><b>Numbers</b><br>order of operations, fractions, decimals</span>
    <span class="arrow">→</span>
    <span class="node"><b>Powers and roots</b><br>exponent rules</span>
    <span class="arrow">→</span>
    <span class="node"><b>Algebra</b><br>expressions, factors, equations</span>
    <span class="arrow">→</span>
    <span class="node"><b>Functions</b><br>line, polynomial, exponential, logarithm</span>
  </div>
  <figcaption>The calculation branch: each step uses the language of the one before. Functions are the language every later topic speaks.</figcaption>
</figure>

<figure class="fig">
  <div class="flow">
    <span class="node"><b>Coordinates</b><br>point, distance, slope</span>
    <span class="arrow">→</span>
    <span class="node"><b>Geometry</b><br>angles, Pythagoras, area</span>
    <span class="arrow">→</span>
    <span class="node"><b>Trigonometry</b><br>sin, cos, unit circle</span>
  </div>
  <figcaption>The shape branch: Pythagoras gives the distance formula, the right triangle gives trigonometry. Vectors in the Advanced Mathematics module continue this branch.</figcaption>
</figure>

<figure class="fig">
  <div class="flow">
    <span class="node"><b>Sets</b><br>union, intersection</span>
    <span class="arrow">→</span>
    <span class="node"><b>Counting</b><br>permutations, combinations</span>
    <span class="arrow">→</span>
    <span class="node"><b>Probability</b><br>events, independence</span>
    <span class="arrow">→</span>
    <span class="node"><b>Statistics</b><br>mean, spread</span>
  </div>
  <figcaption>The uncertainty branch: events are sets, probability is counting, and statistics summarises data in the language of probability.</figcaption>
</figure>

The fourth branch is sequences and Σ notation: every sum from the mean to
the loss function is written with it, and it is used in all three branches.

## One problem from start to finish

Imagine an analyst looking at the data of a learning app. The questions
come, one after another, from different corners of the Foundational Mathematics module.

### 1. Growth: an exponential function

The app has $2000$ users and the number of users grows $10$ percent every
month. After $t$ months:

$$
N(t) = 2000 \cdot 1.1^t
$$

After $6$ months, $2000 \cdot 1.1^6 \approx 2000 \cdot 1.7716 \approx 3543$.
Percentages do not add up: six months bring not $60$ percent but about $77$
percent growth.

### 2. When? Logarithms

In how many months does the number of users double? $1.1^t = 2$; take the
logarithm of both sides:

$$
t = \frac{\ln 2}{\ln 1.1} \approx \frac{0.6931}{0.0953} \approx 7.27
$$

When does it reach $10{,}000$? $1.1^t = 5$, $t = \frac{\ln 5}{\ln 1.1}
\approx 16.9$; so it passes it at the end of month $17$.

<figure class="fig">
<svg viewBox="0 0 440 254" width="440"><line class="grid" x1="55.0" y1="240.0" x2="55.0" y2="20.0"/><line class="grid" x1="91.8" y1="240.0" x2="91.8" y2="20.0"/><line class="grid" x1="128.7" y1="240.0" x2="128.7" y2="20.0"/><line class="grid" x1="165.5" y1="240.0" x2="165.5" y2="20.0"/><line class="grid" x1="202.4" y1="240.0" x2="202.4" y2="20.0"/><line class="grid" x1="239.2" y1="240.0" x2="239.2" y2="20.0"/><line class="grid" x1="276.1" y1="240.0" x2="276.1" y2="20.0"/><line class="grid" x1="312.9" y1="240.0" x2="312.9" y2="20.0"/><line class="grid" x1="349.7" y1="240.0" x2="349.7" y2="20.0"/><line class="grid" x1="386.6" y1="240.0" x2="386.6" y2="20.0"/><line class="grid" x1="55.0" y1="240.0" x2="405.0" y2="240.0"/><line class="grid" x1="55.0" y1="203.3" x2="405.0" y2="203.3"/><line class="grid" x1="55.0" y1="166.7" x2="405.0" y2="166.7"/><line class="grid" x1="55.0" y1="130.0" x2="405.0" y2="130.0"/><line class="grid" x1="55.0" y1="93.3" x2="405.0" y2="93.3"/><line class="grid" x1="55.0" y1="56.7" x2="405.0" y2="56.7"/><line class="grid" x1="55.0" y1="20.0" x2="405.0" y2="20.0"/><line class="line" x1="55.0" y1="240.0" x2="405.0" y2="240.0"/><line class="line" x1="55.0" y1="240.0" x2="55.0" y2="20.0"/><text class="dim" x="91.8" y="253.0" font-size="9" text-anchor="middle">2</text><text class="dim" x="128.7" y="253.0" font-size="9" text-anchor="middle">4</text><text class="dim" x="165.5" y="253.0" font-size="9" text-anchor="middle">6</text><text class="dim" x="202.4" y="253.0" font-size="9" text-anchor="middle">8</text><text class="dim" x="239.2" y="253.0" font-size="9" text-anchor="middle">10</text><text class="dim" x="276.1" y="253.0" font-size="9" text-anchor="middle">12</text><text class="dim" x="312.9" y="253.0" font-size="9" text-anchor="middle">14</text><text class="dim" x="349.7" y="253.0" font-size="9" text-anchor="middle">16</text><text class="dim" x="386.6" y="253.0" font-size="9" text-anchor="middle">18</text><text class="dim" x="50.0" y="206.3" font-size="9" text-anchor="end">2000</text><text class="dim" x="50.0" y="169.7" font-size="9" text-anchor="end">4000</text><text class="dim" x="50.0" y="133.0" font-size="9" text-anchor="end">6000</text><text class="dim" x="50.0" y="96.3" font-size="9" text-anchor="end">8000</text><text class="dim" x="50.0" y="59.7" font-size="9" text-anchor="end">10000</text><text class="dim" x="50.0" y="23.0" font-size="9" text-anchor="end">12000</text><line class="curve3" stroke-dasharray="5 4" x1="55.0" y1="56.7" x2="405.0" y2="56.7"/><line class="curve3" stroke-dasharray="5 4" x1="55.0" y1="166.7" x2="189.0" y2="166.7"/><polyline class="curve" fill="none" points="55.0,203.3 56.5,203.1 57.9,202.8 59.4,202.5 60.8,202.2 62.3,201.9 63.8,201.6 65.2,201.3 66.7,201.1 68.1,200.8 69.6,200.5 71.0,200.2 72.5,199.9 74.0,199.6 75.4,199.2 76.9,198.9 78.3,198.6 79.8,198.3 81.2,198.0 82.7,197.7 84.2,197.4 85.6,197.0 87.1,196.7 88.5,196.4 90.0,196.1 91.5,195.7 92.9,195.4 94.4,195.0 95.8,194.7 97.3,194.4 98.8,194.0 100.2,193.7 101.7,193.3 103.1,193.0 104.6,192.6 106.0,192.3 107.5,191.9 109.0,191.5 110.4,191.2 111.9,190.8 113.3,190.4 114.8,190.0 116.2,189.7 117.7,189.3 119.2,188.9 120.6,188.5 122.1,188.1 123.5,187.7 125.0,187.3 126.5,186.9 127.9,186.5 129.4,186.1 130.8,185.7 132.3,185.3 133.8,184.9 135.2,184.5 136.7,184.1 138.1,183.6 139.6,183.2 141.0,182.8 142.5,182.3 144.0,181.9 145.4,181.5 146.9,181.0 148.3,180.6 149.8,180.1 151.2,179.7 152.7,179.2 154.2,178.8 155.6,178.3 157.1,177.8 158.5,177.3 160.0,176.9 161.5,176.4 162.9,175.9 164.4,175.4 165.8,174.9 167.3,174.4 168.8,174.0 170.2,173.4 171.7,172.9 173.1,172.4 174.6,171.9 176.0,171.4 177.5,170.9 179.0,170.4 180.4,169.8 181.9,169.3 183.3,168.8 184.8,168.2 186.2,167.7 187.7,167.1 189.2,166.6 190.6,166.0 192.1,165.5 193.5,164.9 195.0,164.3 196.5,163.8 197.9,163.2 199.4,162.6 200.8,162.0 202.3,161.4 203.8,160.8 205.2,160.2 206.7,159.6 208.1,159.0 209.6,158.4 211.0,157.8 212.5,157.2 214.0,156.5 215.4,155.9 216.9,155.3 218.3,154.6 219.8,154.0 221.2,153.3 222.7,152.7 224.2,152.0 225.6,151.4 227.1,150.7 228.5,150.0 230.0,149.3 231.5,148.6 232.9,147.9 234.4,147.2 235.8,146.5 237.3,145.8 238.8,145.1 240.2,144.4 241.7,143.7 243.1,143.0 244.6,142.2 246.0,141.5 247.5,140.7 249.0,140.0 250.4,139.2 251.9,138.5 253.3,137.7 254.8,136.9 256.2,136.1 257.7,135.3 259.2,134.6 260.6,133.8 262.1,132.9 263.5,132.1 265.0,131.3 266.5,130.5 267.9,129.7 269.4,128.8 270.8,128.0 272.3,127.1 273.8,126.3 275.2,125.4 276.7,124.6 278.1,123.7 279.6,122.8 281.0,121.9 282.5,121.0 284.0,120.1 285.4,119.2 286.9,118.3 288.3,117.4 289.8,116.4 291.2,115.5 292.7,114.6 294.2,113.6 295.6,112.7 297.1,111.7 298.5,110.7 300.0,109.7 301.5,108.8 302.9,107.8 304.4,106.8 305.8,105.8 307.3,104.7 308.8,103.7 310.2,102.7 311.7,101.6 313.1,100.6 314.6,99.5 316.0,98.5 317.5,97.4 319.0,96.3 320.4,95.2 321.9,94.1 323.3,93.0 324.8,91.9 326.2,90.8 327.7,89.7 329.2,88.5 330.6,87.4 332.1,86.2 333.5,85.1 335.0,83.9 336.5,82.7 337.9,81.5 339.4,80.3 340.8,79.1 342.3,77.9 343.8,76.7 345.2,75.4 346.7,74.2 348.1,72.9 349.6,71.7 351.0,70.4 352.5,69.1 354.0,67.8 355.4,66.5 356.9,65.2 358.3,63.9 359.8,62.5 361.2,61.2 362.7,59.8 364.2,58.5 365.6,57.1 367.1,55.7 368.5,54.3 370.0,52.9 371.5,51.5 372.9,50.0 374.4,48.6 375.8,47.2 377.3,45.7 378.8,44.2 380.2,42.7 381.7,41.3 383.1,39.7 384.6,38.2 386.0,36.7 387.5,35.2 389.0,33.6 390.4,32.0 391.9,30.5 393.3,28.9 394.8,27.3 396.2,25.7 397.7,24.1 399.2,22.4 400.6,20.8 402.1,19.1 403.5,17.4 405.0,15.8"/><circle class="dot2" cx="165.5" cy="175.0" r="4.5"/><circle class="dot3" cx="189.0" cy="166.7" r="4.5"/><circle class="dot2" cx="368.2" cy="54.7" r="4.5"/><text class="ink" x="173.5" y="187.0" font-size="11" text-anchor="start">month 6 ≈ 3543</text><text class="ink" x="181.0" y="158.7" font-size="11" text-anchor="end">double: ≈ 7.3 months</text><text class="ink" x="358.2" y="50.7" font-size="11" text-anchor="end">passes 10,000 in month 17</text><text class="dim" x="405.0" y="234.0" font-size="10" text-anchor="end">month</text><text class="dim" x="61.0" y="30.0" font-size="10" text-anchor="start">users</text></svg>
  <figcaption>10 percent growth a month. The number doubles in 7.3 months and passes 10,000 in month 17; the curve rises faster every month than the month before.</figcaption>
</figure>

### 3. Advertising and new users: a line

Data from two months: $1000$ in advertising brought $150$ new users, $3000$
brought $350$. Assume a linear relationship. The slope:

$$
m = \frac{350 - 150}{3000 - 1000} = \frac{200}{2000} = 0.1
$$

Every $10$ brings one user. $150 = 0.1 \cdot 1000 + b$, so $b = 50$:
$y = 0.1x + 50$. The prediction for $5000$ is $550$. If $520$ actually
come, the error is $520 - 550 = -30$ and its square $900$.

### 4. Time in the app: statistics

The daily usage (minutes) of five users: $12, 15, 18, 20, 35$. The mean is
$20$, the median $18$. The deviations are $-8, -5, -2, 0, 15$; their squares
add up to $318$; the variance is $63.6$ and the standard deviation
$\approx 7.97$. The z-score of $35$ minutes is $\frac{15}{7.97} \approx
1.88$: almost two standard deviations above the mean, a user who stands
out but is not unbelievable.

### 5. Premium members: probability

$30$ percent of users are premium. The probability that at least one of $3$
random, independent users is premium, with the complement:
$1 - 0.7^3 = 1 - 0.343 = 0.657$.

In five steps an exponential function, a logarithm, the equation of a
line, statistics written with Σ and the rules of probability worked
together. The first day of a machine learning project looks exactly like
this.

## What did you learn, section by section?

| Topic | Key idea | In machine learning |
|---|---|---|
| Numbers, order of operations | Brackets first, then powers, then multiplication and division | every formula |
| Fractions, decimals, percentages | A ratio is a division; percentages build up by multiplying | accuracy, probability |
| Powers and roots | $a^m a^n = a^{m+n}$, $a^{-n} = \frac{1}{a^n}$ | learning rates, scales |
| Algebra and factoring | Identities, the same operation on both sides | model equations |
| Equations and inequalities | Isolate the unknown; multiplying by a negative flips the sign | constraints |
| Systems of equations | Two unknowns, two equations | solving for weights |
| Quadratics | $\Delta$, roots, the parabola | loss curves |
| Sets and logic | Union, intersection, "and", "or" | filters, events |
| Functions | Input → output, composition, inverse | a model is a function |
| Coordinates and lines | Slope, $y = mx + b$, distance | linear regression |
| Polynomials | Degree, roots, division | polynomial regression |
| Exponentials and logarithms | Constant ratio; the logarithm finds the exponent | sigmoid, log loss |
| Sequences and Σ | Arithmetic, geometric, sum formulas | every mean and loss |
| Geometry | Pythagoras, area, similarity | distance, IoU |
| Trigonometry | sin, cos, radians, the unit circle | cosine similarity |
| Counting | Multiplication principle, $P$, $\binom{n}{k}$ | search spaces |
| Probability | Complement, union, independence, conditional | class probabilities |
| Statistics | Mean, median, standard deviation, z | scaling, outliers |

## The most common traps

The mistakes that came up again and again in the Foundational Mathematics module, in one list:

| Trap | Correct |
|---|---|
| $-3^2 = 9$ | $-3^2 = -9$; $(-3)^2 = 9$ |
| $\frac{1}{2} + \frac{1}{3} = \frac{2}{5}$ | common denominator: $\frac{5}{6}$ |
| $(a + b)^2 = a^2 + b^2$ | $a^2 + 2ab + b^2$ |
| $\sqrt{a + b} = \sqrt{a} + \sqrt{b}$ | a root does not distribute over a sum |
| $\log(a + b) = \log a + \log b$ | $\log(ab) = \log a + \log b$ |
| multiplying an inequality by a negative and keeping the sign | the sign flips |
| three times $10$ percent = $30$ percent | $1.1^3 = 1.331$ |
| $a_n = a_1 + nd$ | $a_1 + (n - 1)d$ |
| $\sin 30$ with the calculator in radians | check the unit of the angle |
| permutations when order does not matter | $\binom{n}{k}$ |
| $P(A \cup B) = P(A) + P(B)$ | subtract the overlap |
| taking the mean as "typical" in skewed data | look at the median |

## The next step

The Mathematics of AI continues along three branches:

- **Linear algebra:** vectors and matrices. The coordinate plane and
  trigonometry carry over here; a row of data is a vector, a dataset a
  matrix.
- **Calculus:** limits, derivatives, integrals and gradients. Functions,
  polynomials, exponentials and logarithms are revisited with the question
  "how fast does it change"; how models learn (gradient descent) comes from
  here.
- **Probability and statistics:** conditional probability, Bayes,
  distributions, the mathematics of regression and entropy. Built on the
  probability and statistics foundation of this module.

## Summary

- The four branches of the Foundational Mathematics module: calculation (from numbers to functions),
  shape (from coordinates to trigonometry), uncertainty (from sets to
  statistics) and Σ notation, which ties them together.
- In a real problem these branches work together: growth is exponential,
  "when" is a logarithm, a relationship is a line, a summary is statistics,
  a risk is probability.
- The most common mistakes come from operations that do not distribute
  (squares, roots, logarithms), from signs and directions, from adding
  percentages and from units.
- Next up is the Advanced Mathematics module: linear algebra, calculus and probability–statistics.
