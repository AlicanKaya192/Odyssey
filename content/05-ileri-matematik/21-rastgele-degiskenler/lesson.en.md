# Random Variables, Expectation and Variance

So far probability has talked about events: "will it be heads?", "is the
person ill?". Most questions, however, are about a number: how many heads
came up, how much a customer spent, how large a model's error was. A
**random variable** turns the result of an experiment into a number. Two
summaries are usually enough to describe it: the **expected value** (what
the average is in the long run) and the **variance** (how spread out it
is). In machine learning, training means making an expected value (the
expected loss) small; a stochastic gradient is an estimate of an expected
value, and the scaling in dropout is there to preserve one. In this section
we will see discrete and continuous random variables, expectation, variance
and their rules of calculation.

Prerequisites: Conditional Probability and Bayes, Integrals and Area, and
Data and Basic Statistics in MATH 1.

## Random variables

A random variable is a function that assigns a number to each outcome. Toss
a coin three times and let $X$ be the number of heads. There are eight
equally likely outcomes:

| Outcome | TTT | TTH, THT, HTT | THH, HTH, HHT | HHH |
|---|---|---|---|---|
| $X$ | $0$ | $1$ | $2$ | $3$ |
| $P(X = x)$ | $\frac{1}{8}$ | $\frac{3}{8}$ | $\frac{3}{8}$ | $\frac{1}{8}$ |

Variables whose values can be counted (separate values) are called
**discrete**; those that can take every value in an interval are
**continuous**. The number of heads is discrete, a person's height
continuous.

## Probability distributions

For a discrete variable, the table giving each value its probability is the
**probability mass function** $p(x) = P(X = x)$. It has two rules: every
$p(x) \geq 0$ and $\sum_x p(x) = 1$.

<figure class="fig">
<svg viewBox="0 0 440 242" width="440"><line class="grid" x1="98.6" y1="210.0" x2="98.6" y2="20.0"/><line class="grid" x1="179.5" y1="210.0" x2="179.5" y2="20.0"/><line class="grid" x1="260.5" y1="210.0" x2="260.5" y2="20.0"/><line class="grid" x1="341.4" y1="210.0" x2="341.4" y2="20.0"/><line class="grid" x1="50.0" y1="210.0" x2="390.0" y2="210.0"/><line class="grid" x1="50.0" y1="157.2" x2="390.0" y2="157.2"/><line class="grid" x1="50.0" y1="104.4" x2="390.0" y2="104.4"/><line class="grid" x1="50.0" y1="51.7" x2="390.0" y2="51.7"/><line class="line" x1="50.0" y1="210.0" x2="390.0" y2="210.0"/><line class="line" x1="98.6" y1="210.0" x2="98.6" y2="20.0"/><text class="dim" x="98.6" y="223.0" font-size="9" text-anchor="middle">0</text><text class="dim" x="179.5" y="223.0" font-size="9" text-anchor="middle">1</text><text class="dim" x="260.5" y="223.0" font-size="9" text-anchor="middle">2</text><text class="dim" x="341.4" y="223.0" font-size="9" text-anchor="middle">3</text><text class="dim" x="93.6" y="107.4" font-size="9" text-anchor="end">0.25</text><text class="dim" x="93.6" y="54.7" font-size="9" text-anchor="end">0.375</text><rect class="dot" opacity="0.6" x="74.3" y="157.2" width="48.6" height="52.8"/><text class="ink" x="98.6" y="151.2" font-size="11" text-anchor="middle">1/8</text><rect class="dot" opacity="0.6" x="155.2" y="51.7" width="48.6" height="158.3"/><text class="ink" x="179.5" y="45.7" font-size="11" text-anchor="middle">3/8</text><rect class="dot" opacity="0.6" x="236.2" y="51.7" width="48.6" height="158.3"/><text class="ink" x="260.5" y="45.7" font-size="11" text-anchor="middle">3/8</text><rect class="dot" opacity="0.6" x="317.1" y="157.2" width="48.6" height="52.8"/><text class="ink" x="341.4" y="151.2" font-size="11" text-anchor="middle">1/8</text><line class="curve2" stroke-dasharray="5 4" x1="220.0" y1="210.0" x2="220.0" y2="28.4"/><text class="ink" x="220.0" y="24.4" font-size="11" text-anchor="middle">E[X] = 1.5</text><text class="dim" x="390.0" y="238.0" font-size="10" text-anchor="end">number of heads x</text><text class="dim" x="56.0" y="30.0" font-size="10" text-anchor="start">P(X = x)</text></svg>
  <figcaption>The distribution of the number of heads in three tosses: 0 and 3 in one way each (1/8), 1 and 2 in three ways each (3/8). The distribution is symmetric about 1.5; the expected value sits right in the middle.</figcaption>
</figure>

The **cumulative distribution** $F(x) = P(X \leq x)$ is the sum of the
probabilities up to $x$. Here $F(1) = \frac{1}{8} + \frac{3}{8} =
\frac{1}{2}$.

## Expected value

The expected value is the average of the values weighted by their
probabilities:

$$
E[X] = \mu = \sum_x x \, p(x)
$$

Number of heads: $0 \cdot \frac{1}{8} + 1 \cdot \frac{3}{8} + 2 \cdot
\frac{3}{8} + 3 \cdot \frac{1}{8} = \frac{12}{8} = 1.5$.

A die: $\frac{1 + 2 + 3 + 4 + 5 + 6}{6} = 3.5$. The expected value need not
be a possible outcome; a die never shows $3.5$. Its meaning: the average of
many rolls approaches $3.5$ (the law of large numbers).

**A game.** You pay $10$ and roll a die; a $6$ wins $50$, anything else
wins nothing. The net gain $X$ is $40$ ($\frac{1}{6}$) or $-10$
($\frac{5}{6}$).

$$
E[X] = 40 \cdot \tfrac{1}{6} - 10 \cdot \tfrac{5}{6} = \frac{40 - 50}{6} \approx -1.67
$$

On average $1.67$ is lost per game. Casinos set up games whose expected
value is in their favour.

**The expected value of a function.** $E[g(X)] = \sum_x g(x) \, p(x)$. For
a die $E[X^2] = \frac{1 + 4 + 9 + 16 + 25 + 36}{6} = \frac{91}{6}$. Note:
$E[X^2] \neq (E[X])^2 = 12.25$.

## Linearity

The most useful property of expectation:

$$
E[aX + b] = a \, E[X] + b \qquad E[X + Y] = E[X] + E[Y]
$$

The second equality holds even if $X$ and $Y$ are dependent. The expected
sum of $10$ dice is $10 \cdot 3.5 = 35$, without ever working out the
distribution of the sum.

## Variance

The variance is the expected value of the squared deviations from the
expected value:

$$
\operatorname{Var}(X) = E\big[(X - \mu)^2\big] = E[X^2] - \mu^2
$$

The standard deviation is $\sigma = \sqrt{\operatorname{Var}(X)}$. The
second form is easier to compute. A die: $\frac{91}{6} - 3.5^2 =
\frac{182 - 147}{12} = \frac{35}{12} \approx 2.92$; $\sigma \approx 1.71$.

<figure class="fig">
<svg viewBox="0 0 440 212" width="440"><line class="grid" x1="35.8" y1="170.0" x2="35.8" y2="30.0"/><line class="grid" x1="62.2" y1="170.0" x2="62.2" y2="30.0"/><line class="grid" x1="88.6" y1="170.0" x2="88.6" y2="30.0"/><line class="grid" x1="115.0" y1="170.0" x2="115.0" y2="30.0"/><line class="grid" x1="141.4" y1="170.0" x2="141.4" y2="30.0"/><line class="grid" x1="167.8" y1="170.0" x2="167.8" y2="30.0"/><line class="grid" x1="194.2" y1="170.0" x2="194.2" y2="30.0"/><line class="grid" x1="20.0" y1="170.0" x2="210.0" y2="170.0"/><line class="grid" x1="20.0" y1="106.4" x2="210.0" y2="106.4"/><line class="grid" x1="20.0" y1="42.7" x2="210.0" y2="42.7"/><line class="line" x1="20.0" y1="170.0" x2="210.0" y2="170.0"/><line class="line" x1="35.8" y1="170.0" x2="35.8" y2="30.0"/><text class="dim" x="35.8" y="183.0" font-size="9" text-anchor="middle">0</text><text class="dim" x="62.2" y="183.0" font-size="9" text-anchor="middle">1</text><text class="dim" x="88.6" y="183.0" font-size="9" text-anchor="middle">2</text><text class="dim" x="115.0" y="183.0" font-size="9" text-anchor="middle">3</text><text class="dim" x="141.4" y="183.0" font-size="9" text-anchor="middle">4</text><text class="dim" x="167.8" y="183.0" font-size="9" text-anchor="middle">5</text><text class="dim" x="194.2" y="183.0" font-size="9" text-anchor="middle">6</text><rect class="dot" opacity="0.6" x="80.7" y="106.4" width="15.8" height="63.6"/><rect class="dot" opacity="0.6" x="107.1" y="42.7" width="15.8" height="127.3"/><rect class="dot" opacity="0.6" x="133.5" y="106.4" width="15.8" height="63.6"/><line class="curve3" stroke-dasharray="5 4" x1="115.0" y1="170.0" x2="115.0" y2="30.0"/><text class="ink" x="115" y="20" font-size="12" text-anchor="middle">A: Var = 0.5</text><line class="grid" x1="250.8" y1="170.0" x2="250.8" y2="30.0"/><line class="grid" x1="277.2" y1="170.0" x2="277.2" y2="30.0"/><line class="grid" x1="303.6" y1="170.0" x2="303.6" y2="30.0"/><line class="grid" x1="330.0" y1="170.0" x2="330.0" y2="30.0"/><line class="grid" x1="356.4" y1="170.0" x2="356.4" y2="30.0"/><line class="grid" x1="382.8" y1="170.0" x2="382.8" y2="30.0"/><line class="grid" x1="409.2" y1="170.0" x2="409.2" y2="30.0"/><line class="grid" x1="235.0" y1="170.0" x2="425.0" y2="170.0"/><line class="grid" x1="235.0" y1="106.4" x2="425.0" y2="106.4"/><line class="grid" x1="235.0" y1="42.7" x2="425.0" y2="42.7"/><line class="line" x1="235.0" y1="170.0" x2="425.0" y2="170.0"/><line class="line" x1="250.8" y1="170.0" x2="250.8" y2="30.0"/><text class="dim" x="250.8" y="183.0" font-size="9" text-anchor="middle">0</text><text class="dim" x="277.2" y="183.0" font-size="9" text-anchor="middle">1</text><text class="dim" x="303.6" y="183.0" font-size="9" text-anchor="middle">2</text><text class="dim" x="330.0" y="183.0" font-size="9" text-anchor="middle">3</text><text class="dim" x="356.4" y="183.0" font-size="9" text-anchor="middle">4</text><text class="dim" x="382.8" y="183.0" font-size="9" text-anchor="middle">5</text><text class="dim" x="409.2" y="183.0" font-size="9" text-anchor="middle">6</text><rect class="dot2" opacity="0.6" x="242.9" y="119.1" width="15.9" height="50.9"/><rect class="dot2" opacity="0.6" x="269.3" y="144.5" width="15.8" height="25.5"/><rect class="dot2" opacity="0.6" x="322.1" y="68.2" width="15.8" height="101.8"/><rect class="dot2" opacity="0.6" x="374.9" y="144.5" width="15.8" height="25.5"/><rect class="dot2" opacity="0.6" x="401.2" y="119.1" width="15.9" height="50.9"/><line class="curve3" stroke-dasharray="5 4" x1="330.0" y1="170.0" x2="330.0" y2="30.0"/><text class="ink" x="330" y="20" font-size="12" text-anchor="middle">B: Var = 4.4</text><text class="ink" x="220" y="200" font-size="12" text-anchor="middle">both have E[X] = 3</text></svg>
  <figcaption>Both distributions have expected value 3. A's probability is gathered between 2 and 4, variance 0.5. B's probability is spread to the ends, variance 4.4. The expected value describes the centre, the variance the spread.</figcaption>
</figure>

**Rules.**

| Rule | Why |
|---|---|
| $\operatorname{Var}(X + b) = \operatorname{Var}(X)$ | shifting does not change the spread |
| $\operatorname{Var}(aX) = a^2 \operatorname{Var}(X)$ | deviations are $a$ times, their squares $a^2$ times |
| if independent, $\operatorname{Var}(X + Y) = \operatorname{Var}(X) + \operatorname{Var}(Y)$ | no shared fluctuation |

**The variance of the mean.** For the mean $\bar{X}$ of $n$ independent,
identically distributed variables, $E[\bar{X}] = \mu$ and
$\operatorname{Var}(\bar{X}) = \frac{\sigma^2}{n}$. Averaging keeps the
centre and shrinks the spread; the standard deviation falls like
$\frac{\sigma}{\sqrt{n}}$. The Sampling and the Central Limit Theorem
section is built on this.

## Continuous random variables

The probability that a continuous variable takes any single value is $0$;
probability is given to intervals. A **probability density function**
$f(x)$ describes this: the probability of an interval is the area under
the curve.

$$
P(a \leq X \leq b) = \int_a^b f(x) \, dx \qquad \int_{-\infty}^{\infty} f(x) \, dx = 1
$$

<figure class="fig">
<svg viewBox="0 0 440 234" width="440"><line class="grid" x1="76.2" y1="220.0" x2="76.2" y2="20.0"/><line class="grid" x1="141.5" y1="220.0" x2="141.5" y2="20.0"/><line class="grid" x1="206.9" y1="220.0" x2="206.9" y2="20.0"/><line class="grid" x1="272.3" y1="220.0" x2="272.3" y2="20.0"/><line class="grid" x1="337.7" y1="220.0" x2="337.7" y2="20.0"/><line class="grid" x1="50.0" y1="220.0" x2="390.0" y2="220.0"/><line class="grid" x1="50.0" y1="176.5" x2="390.0" y2="176.5"/><line class="grid" x1="50.0" y1="133.0" x2="390.0" y2="133.0"/><line class="grid" x1="50.0" y1="89.6" x2="390.0" y2="89.6"/><line class="grid" x1="50.0" y1="46.1" x2="390.0" y2="46.1"/><line class="line" x1="50.0" y1="220.0" x2="390.0" y2="220.0"/><line class="line" x1="76.2" y1="220.0" x2="76.2" y2="20.0"/><text class="dim" x="206.9" y="233.0" font-size="9" text-anchor="middle">0.5</text><text class="dim" x="337.7" y="233.0" font-size="9" text-anchor="middle">1</text><text class="dim" x="71.2" y="136.0" font-size="9" text-anchor="end">1</text><text class="dim" x="71.2" y="49.1" font-size="9" text-anchor="end">2</text><polygon class="dot" opacity="0.35" points="206.9,220.0 206.9,133.0 208.0,132.3 209.1,131.6 210.2,130.9 211.3,130.1 212.4,129.4 213.5,128.7 214.6,128.0 215.6,127.2 216.7,126.5 217.8,125.8 218.9,125.1 220.0,124.3 221.1,123.6 222.2,122.9 223.3,122.2 224.4,121.4 225.4,120.7 226.5,120.0 227.6,119.3 228.7,118.6 229.8,117.8 230.9,117.1 232.0,116.4 233.1,115.7 234.2,114.9 235.3,114.2 236.3,113.5 237.4,112.8 238.5,112.0 239.6,111.3 240.7,110.6 241.8,109.9 242.9,109.1 244.0,108.4 245.1,107.7 246.2,107.0 247.2,106.2 248.3,105.5 249.4,104.8 250.5,104.1 251.6,103.3 252.7,102.6 253.8,101.9 254.9,101.2 256.0,100.4 257.1,99.7 258.1,99.0 259.2,98.3 260.3,97.5 261.4,96.8 262.5,96.1 263.6,95.4 264.7,94.6 265.8,93.9 266.9,93.2 267.9,92.5 269.0,91.7 270.1,91.0 271.2,90.3 272.3,89.6 273.4,88.8 274.5,88.1 275.6,87.4 276.7,86.7 277.8,85.9 278.8,85.2 279.9,84.5 281.0,83.8 282.1,83.0 283.2,82.3 284.3,81.6 285.4,80.9 286.5,80.1 287.6,79.4 288.7,78.7 289.7,78.0 290.8,77.2 291.9,76.5 293.0,75.8 294.1,75.1 295.2,74.3 296.3,73.6 297.4,72.9 298.5,72.2 299.6,71.4 300.6,70.7 301.7,70.0 302.8,69.3 303.9,68.6 305.0,67.8 306.1,67.1 307.2,66.4 308.3,65.7 309.4,64.9 310.4,64.2 311.5,63.5 312.6,62.8 313.7,62.0 314.8,61.3 315.9,60.6 317.0,59.9 318.1,59.1 319.2,58.4 320.3,57.7 321.3,57.0 322.4,56.2 323.5,55.5 324.6,54.8 325.7,54.1 326.8,53.3 327.9,52.6 329.0,51.9 330.1,51.2 331.2,50.4 332.2,49.7 333.3,49.0 334.4,48.3 335.5,47.5 336.6,46.8 337.7,46.1 337.7,220.0"/><polyline class="curve" fill="none" points="76.2,220.0 77.2,219.3 78.3,218.6 79.4,217.8 80.5,217.1 81.6,216.4 82.7,215.7 83.8,214.9 84.9,214.2 86.0,213.5 87.1,212.8 88.1,212.0 89.2,211.3 90.3,210.6 91.4,209.9 92.5,209.1 93.6,208.4 94.7,207.7 95.8,207.0 96.9,206.2 97.9,205.5 99.0,204.8 100.1,204.1 101.2,203.3 102.3,202.6 103.4,201.9 104.5,201.2 105.6,200.4 106.7,199.7 107.8,199.0 108.8,198.3 109.9,197.5 111.0,196.8 112.1,196.1 113.2,195.4 114.3,194.6 115.4,193.9 116.5,193.2 117.6,192.5 118.7,191.7 119.7,191.0 120.8,190.3 121.9,189.6 123.0,188.8 124.1,188.1 125.2,187.4 126.3,186.7 127.4,185.9 128.5,185.2 129.6,184.5 130.6,183.8 131.7,183.0 132.8,182.3 133.9,181.6 135.0,180.9 136.1,180.1 137.2,179.4 138.3,178.7 139.4,178.0 140.4,177.2 141.5,176.5 142.6,175.8 143.7,175.1 144.8,174.3 145.9,173.6 147.0,172.9 148.1,172.2 149.2,171.4 150.3,170.7 151.3,170.0 152.4,169.3 153.5,168.6 154.6,167.8 155.7,167.1 156.8,166.4 157.9,165.7 159.0,164.9 160.1,164.2 161.2,163.5 162.2,162.8 163.3,162.0 164.4,161.3 165.5,160.6 166.6,159.9 167.7,159.1 168.8,158.4 169.9,157.7 171.0,157.0 172.1,156.2 173.1,155.5 174.2,154.8 175.3,154.1 176.4,153.3 177.5,152.6 178.6,151.9 179.7,151.2 180.8,150.4 181.9,149.7 182.9,149.0 184.0,148.3 185.1,147.5 186.2,146.8 187.3,146.1 188.4,145.4 189.5,144.6 190.6,143.9 191.7,143.2 192.8,142.5 193.8,141.7 194.9,141.0 196.0,140.3 197.1,139.6 198.2,138.8 199.3,138.1 200.4,137.4 201.5,136.7 202.6,135.9 203.7,135.2 204.7,134.5 205.8,133.8 206.9,133.0 208.0,132.3 209.1,131.6 210.2,130.9 211.3,130.1 212.4,129.4 213.5,128.7 214.6,128.0 215.6,127.2 216.7,126.5 217.8,125.8 218.9,125.1 220.0,124.3 221.1,123.6 222.2,122.9 223.3,122.2 224.4,121.4 225.4,120.7 226.5,120.0 227.6,119.3 228.7,118.6 229.8,117.8 230.9,117.1 232.0,116.4 233.1,115.7 234.2,114.9 235.3,114.2 236.3,113.5 237.4,112.8 238.5,112.0 239.6,111.3 240.7,110.6 241.8,109.9 242.9,109.1 244.0,108.4 245.1,107.7 246.2,107.0 247.2,106.2 248.3,105.5 249.4,104.8 250.5,104.1 251.6,103.3 252.7,102.6 253.8,101.9 254.9,101.2 256.0,100.4 257.1,99.7 258.1,99.0 259.2,98.3 260.3,97.5 261.4,96.8 262.5,96.1 263.6,95.4 264.7,94.6 265.8,93.9 266.9,93.2 267.9,92.5 269.0,91.7 270.1,91.0 271.2,90.3 272.3,89.6 273.4,88.8 274.5,88.1 275.6,87.4 276.7,86.7 277.8,85.9 278.8,85.2 279.9,84.5 281.0,83.8 282.1,83.0 283.2,82.3 284.3,81.6 285.4,80.9 286.5,80.1 287.6,79.4 288.7,78.7 289.7,78.0 290.8,77.2 291.9,76.5 293.0,75.8 294.1,75.1 295.2,74.3 296.3,73.6 297.4,72.9 298.5,72.2 299.6,71.4 300.6,70.7 301.7,70.0 302.8,69.3 303.9,68.6 305.0,67.8 306.1,67.1 307.2,66.4 308.3,65.7 309.4,64.9 310.4,64.2 311.5,63.5 312.6,62.8 313.7,62.0 314.8,61.3 315.9,60.6 317.0,59.9 318.1,59.1 319.2,58.4 320.3,57.7 321.3,57.0 322.4,56.2 323.5,55.5 324.6,54.8 325.7,54.1 326.8,53.3 327.9,52.6 329.0,51.9 330.1,51.2 331.2,50.4 332.2,49.7 333.3,49.0 334.4,48.3 335.5,47.5 336.6,46.8 337.7,46.1"/><line class="curve3" stroke-dasharray="5 4" x1="337.7" y1="220.0" x2="337.7" y2="46.1"/><text class="ink" x="193.8" y="120.0" font-size="12" text-anchor="end">f(x) = 2x</text><text class="ink" x="264.5" y="189.6" font-size="10" text-anchor="middle">P(0.5 ≤ X ≤ 1) = 0.75</text><text class="dim" x="89.2" y="33.0" font-size="10" text-anchor="start">total area 1</text></svg>
  <figcaption>The density f(x) = 2x on [0, 1]: larger values are more likely. The total area under the curve is 1 (a triangle: ½ · 1 · 2). The shaded area between 0.5 and 1 is 0.75.</figcaption>
</figure>

$P(0.5 \leq X \leq 1) = \int_{0.5}^{1} 2x \, dx = \big[x^2\big]_{0.5}^{1} = 1 - 0.25 = 0.75$.

Expectation and variance are written with integrals instead of sums:

$$
E[X] = \int x \, f(x) \, dx \qquad \operatorname{Var}(X) = \int x^2 f(x) \, dx - \mu^2
$$

For $f(x) = 2x$: $E[X] = \int_0^1 2x^2 \, dx = \frac{2}{3}$,
$E[X^2] = \int_0^1 2x^3 \, dx = \frac{1}{2}$, variance
$\frac{1}{2} - \frac{4}{9} = \frac{1}{18}$.

**The uniform distribution.** Equal density everywhere on $[0, 1]$,
$f(x) = 1$: $E[X] = \frac{1}{2}$, $\operatorname{Var}(X) = \frac{1}{3} -
\frac{1}{4} = \frac{1}{12}$. This is a computer's "random number"
generator.

**A density is not a probability.** $f(x)$ can be larger than $1$
($f(1) = 2$); probability is read only as area.

## Expectation in machine learning

**Expected loss.** A model's true performance is its **expected loss**
(risk) over all possible data. Since we cannot know it, we minimise the
average loss on the training data; that is estimating an expected value
with a sample mean.

**Stochastic gradients.** The gradient computed on a mini-batch is a random
variable; its expected value equals the gradient over all the data (an
unbiased estimate). As the batch grows its variance falls like
$\frac{1}{n}$: a large batch gives smoother steps, a small batch noisier
but cheaper ones.

**Dropout.** During training each neuron is kept on with probability $p$,
and if kept its output is scaled up by $\frac{1}{p}$. If the output is $a$,
the expected value is $p \cdot \frac{a}{p} + (1 - p) \cdot 0 = a$: at test
time, when nothing is switched off, the scale is not broken.

**Bias and variance.** A model's error comes from two sources: how far the
expected value of its prediction is from the truth (bias), and how much
its prediction fluctuates across different training sets (variance).
Simple models are biased, complex models variable.

## Common mistakes

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Wrong</h4>
      <p>$E[X^2] = (E[X])^2$</p>
      <p>$\operatorname{Var}(2X) = 2 \operatorname{Var}(X)$</p>
      <p>$\operatorname{Var}(X - Y) = \operatorname{Var}(X) - \operatorname{Var}(Y)$</p>
      <p>$f(x)$ is a probability</p>
    </div>
    <div class="ok">
      <h4>Right</h4>
      <p>the gap is the variance: $E[X^2] - \mu^2$</p>
      <p>$\operatorname{Var}(2X) = 4 \operatorname{Var}(X)$</p>
      <p>if independent, $\operatorname{Var}(X) + \operatorname{Var}(Y)$</p>
      <p>probability is area: $\int_a^b f(x) \, dx$</p>
    </div>
  </div>
  <figcaption>Expectation is linear; variance works with squares, so it squares a factor and adds up even for a difference.</figcaption>
</figure>

- **Taking the expected value to be "the most likely value".** A die's
  expected value is $3.5$, but the die never shows it.
- **Adding the variances of dependent variables.** The rule holds only
  under independence; otherwise a covariance term is added (the Covariance
  and Correlation section).

## Summary

- A random variable turns an outcome into a number; discrete or continuous.
- Discrete: $p(x)$, $\sum p(x) = 1$; continuous: $f(x)$, probability is
  area.
- $E[X] = \sum x p(x)$ or $\int x f(x) dx$; the long-run average.
- $E[aX + b] = aE[X] + b$ and $E[X + Y] = E[X] + E[Y]$ always.
- $\operatorname{Var}(X) = E[X^2] - \mu^2$; $\operatorname{Var}(aX + b) =
  a^2 \operatorname{Var}(X)$; for independent variables variances add.
- The variance of the mean of $n$ observations is $\frac{\sigma^2}{n}$.
- Expected loss, stochastic gradients, dropout and bias–variance are all
  stories about expected values.
