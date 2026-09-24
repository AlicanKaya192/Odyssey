# Limits and Continuity

Linear algebra described the **shape** of data: vectors, matrices,
transformations. Calculus describes **change**: when an input changes a
little, how much does the output change? Training a model is done with
exactly the answer to this question; the derivative tells us which way to
push each weight to bring the loss down a little. At the base of the
derivative is the **limit**: the question "what happens as we get
infinitely close to a point?"

In this section we will look at limits by intuition and by calculation,
and get to know behaviour at infinity and continuity.

Prerequisite: the Functions and Factoring sections of MATH 1.

## Getting close: limits with numbers

Consider the function $f(x) = \dfrac{x^2 - 1}{x - 1}$. Putting in $x = 1$
gives $\dfrac{0}{0}$: the function is **undefined** there. But what
happens at values close to $1$?

| $x$ | $0.9$ | $0.99$ | $0.999$ | $1$ | $1.001$ | $1.01$ | $1.1$ |
|---|---|---|---|---|---|---|---|
| $f(x)$ | $1.9$ | $1.99$ | $1.999$ | undefined | $2.001$ | $2.01$ | $2.1$ |

Whichever side $x$ comes from, as it approaches $1$, $f(x)$ approaches
$2$. We write this as:

$$
\lim_{x \to 1} \frac{x^2 - 1}{x - 1} = 2
$$

<figure class="fig">
<svg viewBox="0 0 380 314" width="380"><line class="grid" x1="40.0" y1="260.0" x2="40.0" y2="20.0"/><line class="grid" x1="115.0" y1="260.0" x2="115.0" y2="20.0"/><line class="grid" x1="190.0" y1="260.0" x2="190.0" y2="20.0"/><line class="grid" x1="265.0" y1="260.0" x2="265.0" y2="20.0"/><line class="grid" x1="340.0" y1="260.0" x2="340.0" y2="20.0"/><line class="grid" x1="40.0" y1="236.0" x2="340.0" y2="236.0"/><line class="grid" x1="40.0" y1="188.0" x2="340.0" y2="188.0"/><line class="grid" x1="40.0" y1="140.0" x2="340.0" y2="140.0"/><line class="grid" x1="40.0" y1="92.0" x2="340.0" y2="92.0"/><line class="grid" x1="40.0" y1="44.0" x2="340.0" y2="44.0"/><line class="line" x1="40.0" y1="236.0" x2="340.0" y2="236.0"/><line class="line" x1="115.0" y1="260.0" x2="115.0" y2="20.0"/><text class="dim" x="40.0" y="249.0" font-size="9" text-anchor="middle">−1</text><text class="dim" x="190.0" y="249.0" font-size="9" text-anchor="middle">1</text><text class="dim" x="265.0" y="249.0" font-size="9" text-anchor="middle">2</text><text class="dim" x="340.0" y="249.0" font-size="9" text-anchor="middle">3</text><text class="dim" x="110.0" y="191.0" font-size="9" text-anchor="end">1</text><text class="dim" x="110.0" y="143.0" font-size="9" text-anchor="end">2</text><text class="dim" x="110.0" y="95.0" font-size="9" text-anchor="end">3</text><text class="dim" x="110.0" y="47.0" font-size="9" text-anchor="end">4</text><polyline class="curve" fill="none" points="40.0,236.0 41.3,235.2 42.5,234.4 43.8,233.6 45.0,232.8 46.2,232.0 47.5,231.2 48.8,230.4 50.0,229.6 51.2,228.8 52.5,228.0 53.8,227.2 55.0,226.4 56.2,225.6 57.5,224.8 58.8,224.0 60.0,223.2 61.2,222.4 62.5,221.6 63.8,220.8 65.0,220.0 66.2,219.2 67.5,218.4 68.8,217.6 70.0,216.8 71.2,216.0 72.5,215.2 73.8,214.4 75.0,213.6 76.2,212.8 77.5,212.0 78.8,211.2 80.0,210.4 81.2,209.6 82.5,208.8 83.8,208.0 85.0,207.2 86.2,206.4 87.5,205.6 88.8,204.8 90.0,204.0 91.2,203.2 92.5,202.4 93.8,201.6 95.0,200.8 96.2,200.0 97.5,199.2 98.8,198.4 100.0,197.6 101.2,196.8 102.5,196.0 103.8,195.2 105.0,194.4 106.2,193.6 107.5,192.8 108.8,192.0 110.0,191.2 111.2,190.4 112.5,189.6 113.8,188.8 115.0,188.0 116.2,187.2 117.5,186.4 118.8,185.6 120.0,184.8 121.2,184.0 122.5,183.2 123.8,182.4 125.0,181.6 126.2,180.8 127.5,180.0 128.8,179.2 130.0,178.4 131.2,177.6 132.5,176.8 133.8,176.0 135.0,175.2 136.2,174.4 137.5,173.6 138.8,172.8 140.0,172.0 141.2,171.2 142.5,170.4 143.8,169.6 145.0,168.8 146.2,168.0 147.5,167.2 148.8,166.4 150.0,165.6 151.2,164.8 152.5,164.0 153.8,163.2 155.0,162.4 156.2,161.6 157.5,160.8 158.8,160.0 160.0,159.2 161.2,158.4 162.5,157.6 163.8,156.8 165.0,156.0 166.2,155.2 167.5,154.4 168.8,153.6 170.0,152.8 171.2,152.0 172.5,151.2 173.8,150.4 175.0,149.6 176.2,148.8 177.5,148.0 178.8,147.2 180.0,146.4 181.2,145.6 182.5,144.8 183.8,144.0"/><polyline class="curve" fill="none" points="196.2,136.0 197.5,135.2 198.8,134.4 200.0,133.6 201.2,132.8 202.5,132.0 203.7,131.2 205.0,130.4 206.2,129.6 207.5,128.8 208.8,128.0 210.0,127.2 211.2,126.4 212.5,125.6 213.8,124.8 215.0,124.0 216.2,123.2 217.5,122.4 218.8,121.6 220.0,120.8 221.2,120.0 222.5,119.2 223.8,118.4 225.0,117.6 226.2,116.8 227.5,116.0 228.8,115.2 230.0,114.4 231.2,113.6 232.5,112.8 233.8,112.0 235.0,111.2 236.2,110.4 237.5,109.6 238.8,108.8 240.0,108.0 241.2,107.2 242.5,106.4 243.8,105.6 245.0,104.8 246.2,104.0 247.5,103.2 248.8,102.4 250.0,101.6 251.3,100.8 252.5,100.0 253.8,99.2 255.0,98.4 256.2,97.6 257.5,96.8 258.8,96.0 260.0,95.2 261.2,94.4 262.5,93.6 263.8,92.8 265.0,92.0 266.2,91.2 267.5,90.4 268.8,89.6 270.0,88.8 271.2,88.0 272.5,87.2 273.8,86.4 275.0,85.6 276.2,84.8 277.5,84.0 278.8,83.2 280.0,82.4 281.2,81.6 282.5,80.8 283.8,80.0 285.0,79.2 286.2,78.4 287.5,77.6 288.8,76.8 290.0,76.0 291.2,75.2 292.5,74.4 293.8,73.6 295.0,72.8 296.2,72.0 297.5,71.2 298.8,70.4 300.0,69.6 301.2,68.8 302.5,68.0 303.8,67.2 305.0,66.4 306.2,65.6 307.5,64.8 308.8,64.0 310.0,63.2 311.2,62.4 312.5,61.6 313.8,60.8 315.0,60.0 316.2,59.2 317.5,58.4 318.8,57.6 320.0,56.8 321.2,56.0 322.5,55.2 323.8,54.4 325.0,53.6 326.2,52.8 327.5,52.0 328.8,51.2 330.0,50.4 331.2,49.6 332.5,48.8 333.8,48.0 335.0,47.2 336.2,46.4 337.5,45.6 338.8,44.8 340.0,44.0"/><circle class="curve" fill="none" stroke-width="2" cx="190.0" cy="140.0" r="5"/><line class="curve3" stroke-dasharray="5 4" x1="190.0" y1="236.0" x2="190.0" y2="140.0"/><line class="curve3" stroke-dasharray="5 4" x1="115.0" y1="140.0" x2="190.0" y2="140.0"/><line class="curve2" x1="130.0" y1="209.6" x2="173.7" y2="166.6"/><polygon class="dot2" points="178.8,161.6 175.5,170.0 170.4,164.7"/><line class="curve2" x1="250.0" y1="70.4" x2="206.3" y2="113.4"/><polygon class="dot2" points="201.2,118.4 204.5,110.0 209.6,115.3"/><text class="ink" x="130.0" y="225.6" font-size="11" text-anchor="middle">from the left</text><text class="ink" x="257.8" y="66.4" font-size="11" text-anchor="start">from the right</text><text class="ink" x="190" y="286" font-size="12" text-anchor="middle">f(1) is undefined: a hole in the graph</text><text class="dim" x="190" y="304" font-size="12" text-anchor="middle">as x approaches 1, f(x) approaches 2</text></svg>
  <figcaption>The graph is the line y = x + 1 with a single hole at x = 1. Approaching from the left or from the right, the height goes to 2; the limit looks not at the value at that point but at the behaviour around it.</figcaption>
</figure>

**A limit does not ask about the point itself.** $\lim_{x \to a} f(x) = L$
means: if $x$ is chosen close enough to $a$ (but different from $a$),
$f(x)$ gets as close to $L$ as we like. $f(a)$ may be undefined, or even a
number different from $L$; the limit does not care.

## One-sided limits

Sometimes approaching from the left and from the right give different
results. Say shipping costs $50$ up to $1$ kg and $80$ above $1$ kg:

$$
\lim_{x \to 1^-} f(x) = 50, \qquad \lim_{x \to 1^+} f(x) = 80
$$

$1^-$ means "from the left", $1^+$ "from the right". **For the limit to
exist, both sides must go to the same number.** Here they do not, so
$\lim_{x \to 1} f(x)$ does not exist.

## Calculating limits

**1. Substitute first.** If the function is well behaved at the point (a
polynomial, a fraction whose denominator is not zero, a root inside its
domain), the limit is the value itself:

$$
\lim_{x \to 2} (x^2 + 3x) = 4 + 6 = 10
$$

**2. If you get $\frac{0}{0}$, simplify.** $\frac{0}{0}$ is not an
answer but a sign to "work harder". It means the top and bottom share a
factor:

$$
\lim_{x \to 3} \frac{x^2 - 9}{x - 3} = \lim_{x \to 3} \frac{(x - 3)(x + 3)}{x - 3} = \lim_{x \to 3} (x + 3) = 6
$$

Cancelling is allowed, because in the limit $x \neq 3$; $x - 3$ is not
zero.

**3. With a root, multiply by the conjugate.** Multiplying $\sqrt{a} - b$
by $\sqrt{a} + b$ removes the root:

$$
\frac{\sqrt{x} - 2}{x - 4} \cdot \frac{\sqrt{x} + 2}{\sqrt{x} + 2} = \frac{x - 4}{(x - 4)(\sqrt{x} + 2)} = \frac{1}{\sqrt{x} + 2}
$$

As $x \to 4$ this goes to $\frac{1}{4}$.

**Limit rules.** When the limits exist, the limit of a sum is the sum of
the limits, the limit of a product the product of the limits, and the
limit of a quotient (if the bottom limit is not zero) the quotient of the
limits. A constant factor comes out: $\lim 5f(x) = 5 \lim f(x)$.

## Limits at infinity

What happens as $x$ grows without bound? $\dfrac{1}{x}$: at $x = 10$ it
is $0.1$, at $x = 1000$ it is $0.001$. It gets as close to zero as we
like:

$$
\lim_{x \to \infty} \frac{1}{x} = 0
$$

**In fractions, divide by the highest power.** Dividing top and bottom by
the highest power of $x$ sends the small terms to zero:

$$
\lim_{x \to \infty} \frac{3x^2 + 1}{x^2 + 5} = \lim_{x \to \infty} \frac{3 + \frac{1}{x^2}}{1 + \frac{5}{x^2}} = \frac{3}{1} = 3
$$

Shortcut: if the top and bottom have the same degree, the limit is the
ratio of the leading coefficients; if the bottom's degree is larger, it is
$0$; if the top's is larger, the expression grows without bound.

<figure class="fig">
<svg viewBox="0 0 460 236" width="460"><line class="grid" x1="40.0" y1="220.0" x2="40.0" y2="20.0"/><line class="grid" x1="67.1" y1="220.0" x2="67.1" y2="20.0"/><line class="grid" x1="94.3" y1="220.0" x2="94.3" y2="20.0"/><line class="grid" x1="121.4" y1="220.0" x2="121.4" y2="20.0"/><line class="grid" x1="148.6" y1="220.0" x2="148.6" y2="20.0"/><line class="grid" x1="175.7" y1="220.0" x2="175.7" y2="20.0"/><line class="grid" x1="202.9" y1="220.0" x2="202.9" y2="20.0"/><line class="grid" x1="230.0" y1="220.0" x2="230.0" y2="20.0"/><line class="grid" x1="257.1" y1="220.0" x2="257.1" y2="20.0"/><line class="grid" x1="284.3" y1="220.0" x2="284.3" y2="20.0"/><line class="grid" x1="311.4" y1="220.0" x2="311.4" y2="20.0"/><line class="grid" x1="338.6" y1="220.0" x2="338.6" y2="20.0"/><line class="grid" x1="365.7" y1="220.0" x2="365.7" y2="20.0"/><line class="grid" x1="392.9" y1="220.0" x2="392.9" y2="20.0"/><line class="grid" x1="420.0" y1="220.0" x2="420.0" y2="20.0"/><line class="grid" x1="40.0" y1="220.0" x2="420.0" y2="220.0"/><line class="grid" x1="40.0" y1="186.7" x2="420.0" y2="186.7"/><line class="grid" x1="40.0" y1="153.3" x2="420.0" y2="153.3"/><line class="grid" x1="40.0" y1="120.0" x2="420.0" y2="120.0"/><line class="grid" x1="40.0" y1="86.7" x2="420.0" y2="86.7"/><line class="grid" x1="40.0" y1="53.3" x2="420.0" y2="53.3"/><line class="grid" x1="40.0" y1="20.0" x2="420.0" y2="20.0"/><line class="line" x1="40.0" y1="186.7" x2="420.0" y2="186.7"/><line class="line" x1="230.0" y1="220.0" x2="230.0" y2="20.0"/><text class="dim" x="67.1" y="199.7" font-size="9" text-anchor="middle">−6</text><text class="dim" x="121.4" y="199.7" font-size="9" text-anchor="middle">−4</text><text class="dim" x="175.7" y="199.7" font-size="9" text-anchor="middle">−2</text><text class="dim" x="284.3" y="199.7" font-size="9" text-anchor="middle">2</text><text class="dim" x="338.6" y="199.7" font-size="9" text-anchor="middle">4</text><text class="dim" x="392.9" y="199.7" font-size="9" text-anchor="middle">6</text><text class="dim" x="225.0" y="56.3" font-size="9" text-anchor="end">1</text><line class="curve3" stroke-dasharray="5 4" x1="40.0" y1="53.3" x2="420.0" y2="53.3"/><polyline class="curve" fill="none" points="40.0,186.5 41.6,186.5 43.2,186.5 44.7,186.5 46.3,186.5 47.9,186.5 49.5,186.5 51.1,186.5 52.7,186.5 54.3,186.5 55.8,186.4 57.4,186.4 59.0,186.4 60.6,186.4 62.2,186.4 63.8,186.4 65.3,186.4 66.9,186.3 68.5,186.3 70.1,186.3 71.7,186.3 73.2,186.3 74.8,186.2 76.4,186.2 78.0,186.2 79.6,186.1 81.2,186.1 82.8,186.1 84.3,186.0 85.9,186.0 87.5,186.0 89.1,185.9 90.7,185.9 92.2,185.8 93.8,185.8 95.4,185.7 97.0,185.7 98.6,185.6 100.2,185.6 101.8,185.5 103.3,185.4 104.9,185.4 106.5,185.3 108.1,185.2 109.7,185.1 111.2,185.0 112.8,184.9 114.4,184.8 116.0,184.7 117.6,184.6 119.2,184.5 120.7,184.3 122.3,184.2 123.9,184.0 125.5,183.9 127.1,183.7 128.7,183.6 130.2,183.4 131.8,183.2 133.4,183.0 135.0,182.8 136.6,182.5 138.2,182.3 139.8,182.0 141.3,181.8 142.9,181.5 144.5,181.2 146.1,180.9 147.7,180.5 149.2,180.2 150.8,179.8 152.4,179.4 154.0,179.0 155.6,178.6 157.2,178.1 158.8,177.7 160.3,177.2 161.9,176.6 163.5,176.1 165.1,175.5 166.7,174.9 168.2,174.2 169.8,173.6 171.4,172.9 173.0,172.1 174.6,171.3 176.2,170.5 177.8,169.7 179.3,168.8 180.9,167.9 182.5,166.9 184.1,165.9 185.7,164.9 187.2,163.8 188.8,162.7 190.4,161.5 192.0,160.3 193.6,159.0 195.2,157.7 196.8,156.4 198.3,155.0 199.9,153.6 201.5,152.1 203.1,150.6 204.7,149.0 206.2,147.4 207.8,145.8 209.4,144.1 211.0,142.4 212.6,140.7 214.2,138.9 215.8,137.1 217.3,135.3 218.9,133.4 220.5,131.5 222.1,129.7 223.7,127.7 225.2,125.8 226.8,123.9 228.4,121.9 230.0,120.0 231.6,118.1 233.2,116.1 234.7,114.2 236.3,112.3 237.9,110.3 239.5,108.5 241.1,106.6 242.7,104.7 244.2,102.9 245.8,101.1 247.4,99.3 249.0,97.6 250.6,95.9 252.2,94.2 253.8,92.6 255.3,91.0 256.9,89.4 258.5,87.9 260.1,86.4 261.7,85.0 263.2,83.6 264.8,82.3 266.4,81.0 268.0,79.7 269.6,78.5 271.2,77.3 272.8,76.2 274.3,75.1 275.9,74.1 277.5,73.1 279.1,72.1 280.7,71.2 282.2,70.3 283.8,69.5 285.4,68.7 287.0,67.9 288.6,67.1 290.2,66.4 291.8,65.8 293.3,65.1 294.9,64.5 296.5,63.9 298.1,63.4 299.7,62.8 301.2,62.3 302.8,61.9 304.4,61.4 306.0,61.0 307.6,60.6 309.2,60.2 310.8,59.8 312.3,59.5 313.9,59.1 315.5,58.8 317.1,58.5 318.7,58.2 320.2,58.0 321.8,57.7 323.4,57.5 325.0,57.2 326.6,57.0 328.2,56.8 329.8,56.6 331.3,56.4 332.9,56.3 334.5,56.1 336.1,56.0 337.7,55.8 339.2,55.7 340.8,55.5 342.4,55.4 344.0,55.3 345.6,55.2 347.2,55.1 348.8,55.0 350.3,54.9 351.9,54.8 353.5,54.7 355.1,54.6 356.7,54.6 358.2,54.5 359.8,54.4 361.4,54.4 363.0,54.3 364.6,54.3 366.2,54.2 367.8,54.2 369.3,54.1 370.9,54.1 372.5,54.0 374.1,54.0 375.7,54.0 377.2,53.9 378.8,53.9 380.4,53.9 382.0,53.8 383.6,53.8 385.2,53.8 386.8,53.7 388.3,53.7 389.9,53.7 391.5,53.7 393.1,53.7 394.7,53.6 396.2,53.6 397.8,53.6 399.4,53.6 401.0,53.6 402.6,53.6 404.2,53.6 405.8,53.5 407.3,53.5 408.9,53.5 410.5,53.5 412.1,53.5 413.7,53.5 415.2,53.5 416.8,53.5 418.4,53.5 420.0,53.5"/><circle class="dot2" cx="230.0" cy="120.0" r="4.5"/><text class="ink" x="238.0" y="136.0" font-size="11" text-anchor="start">σ(0) = 0.5</text><text class="ink" x="414.6" y="45.3" font-size="11" text-anchor="end">as x → ∞, σ(x) → 1</text><text class="ink" x="45.4" y="178.7" font-size="11" text-anchor="start">as x → −∞, σ(x) → 0</text></svg>
  <figcaption>The sigmoid σ(x) = 1 / (1 + e<sup>−x</sup>). As x grows, e<sup>−x</sup> goes to zero and σ approaches 1; when x is very negative, e<sup>−x</sup> grows without bound and σ approaches 0. It never reaches either value.</figcaption>
</figure>

**Infinite limits.** $\dfrac{1}{x^2}$ grows without bound as $x \to 0$:
$\lim_{x \to 0} \dfrac{1}{x^2} = \infty$. This is not a number but a short
way of saying "no bound". On the graph, $x = 0$ is a **vertical
asymptote**.

**An important limit: the number $e$.** If you split 100% interest into
$n$ parts over a year and add each part as it comes, one unit of money
becomes $\left(1 + \frac{1}{n}\right)^n$ by the end of the year:

| $n$ | $1$ | $2$ | $12$ | $365$ | $10\,000$ |
|---|---|---|---|---|---|
| $\left(1 + \frac{1}{n}\right)^n$ | $2$ | $2.25$ | $2.613$ | $2.7146$ | $2.7181$ |

$$
\lim_{n \to \infty} \left(1 + \frac{1}{n}\right)^n = e \approx 2.71828
$$

This is where $e$, the base of the natural logarithm, comes from; in the
derivatives section we will see why it is so special.

## Continuity

A function is continuous at a point if its graph can be drawn there
**without lifting the pen**. The precise version is three conditions:

1. $f(a)$ is defined,
2. $\lim_{x \to a} f(x)$ exists,
3. the two are equal: $\lim_{x \to a} f(x) = f(a)$.

<figure class="fig">
<svg viewBox="0 0 570 220" width="570"><line class="grid" x1="20.0" y1="170.0" x2="20.0" y2="20.0"/><line class="grid" x1="57.5" y1="170.0" x2="57.5" y2="20.0"/><line class="grid" x1="95.0" y1="170.0" x2="95.0" y2="20.0"/><line class="grid" x1="132.5" y1="170.0" x2="132.5" y2="20.0"/><line class="grid" x1="170.0" y1="170.0" x2="170.0" y2="20.0"/><line class="grid" x1="20.0" y1="170.0" x2="170.0" y2="170.0"/><line class="grid" x1="20.0" y1="140.0" x2="170.0" y2="140.0"/><line class="grid" x1="20.0" y1="110.0" x2="170.0" y2="110.0"/><line class="grid" x1="20.0" y1="80.0" x2="170.0" y2="80.0"/><line class="grid" x1="20.0" y1="50.0" x2="170.0" y2="50.0"/><line class="grid" x1="20.0" y1="20.0" x2="170.0" y2="20.0"/><line class="line" x1="20.0" y1="140.0" x2="170.0" y2="140.0"/><line class="line" x1="57.5" y1="170.0" x2="57.5" y2="20.0"/><line class="grid" x1="210.0" y1="170.0" x2="210.0" y2="20.0"/><line class="grid" x1="247.5" y1="170.0" x2="247.5" y2="20.0"/><line class="grid" x1="285.0" y1="170.0" x2="285.0" y2="20.0"/><line class="grid" x1="322.5" y1="170.0" x2="322.5" y2="20.0"/><line class="grid" x1="360.0" y1="170.0" x2="360.0" y2="20.0"/><line class="grid" x1="210.0" y1="170.0" x2="360.0" y2="170.0"/><line class="grid" x1="210.0" y1="140.0" x2="360.0" y2="140.0"/><line class="grid" x1="210.0" y1="110.0" x2="360.0" y2="110.0"/><line class="grid" x1="210.0" y1="80.0" x2="360.0" y2="80.0"/><line class="grid" x1="210.0" y1="50.0" x2="360.0" y2="50.0"/><line class="grid" x1="210.0" y1="20.0" x2="360.0" y2="20.0"/><line class="line" x1="210.0" y1="140.0" x2="360.0" y2="140.0"/><line class="line" x1="247.5" y1="170.0" x2="247.5" y2="20.0"/><line class="grid" x1="400.0" y1="170.0" x2="400.0" y2="20.0"/><line class="grid" x1="437.5" y1="170.0" x2="437.5" y2="20.0"/><line class="grid" x1="475.0" y1="170.0" x2="475.0" y2="20.0"/><line class="grid" x1="512.5" y1="170.0" x2="512.5" y2="20.0"/><line class="grid" x1="550.0" y1="170.0" x2="550.0" y2="20.0"/><line class="grid" x1="400.0" y1="170.0" x2="550.0" y2="170.0"/><line class="grid" x1="400.0" y1="140.0" x2="550.0" y2="140.0"/><line class="grid" x1="400.0" y1="110.0" x2="550.0" y2="110.0"/><line class="grid" x1="400.0" y1="80.0" x2="550.0" y2="80.0"/><line class="grid" x1="400.0" y1="50.0" x2="550.0" y2="50.0"/><line class="grid" x1="400.0" y1="20.0" x2="550.0" y2="20.0"/><line class="line" x1="400.0" y1="140.0" x2="550.0" y2="140.0"/><line class="line" x1="437.5" y1="170.0" x2="437.5" y2="20.0"/><polyline class="curve" fill="none" points="20.0,140.0 20.6,139.5 21.2,139.0 21.9,138.5 22.5,138.0 23.1,137.5 23.8,137.0 24.4,136.5 25.0,136.0 25.6,135.5 26.2,135.0 26.9,134.5 27.5,134.0 28.1,133.5 28.8,133.0 29.4,132.5 30.0,132.0 30.6,131.5 31.2,131.0 31.9,130.5 32.5,130.0 33.1,129.5 33.8,129.0 34.4,128.5 35.0,128.0 35.6,127.5 36.2,127.0 36.9,126.5 37.5,126.0 38.1,125.5 38.8,125.0 39.4,124.5 40.0,124.0 40.6,123.5 41.2,123.0 41.9,122.5 42.5,122.0 43.1,121.5 43.8,121.0 44.4,120.5 45.0,120.0 45.6,119.5 46.2,119.0 46.9,118.5 47.5,118.0 48.1,117.5 48.8,117.0 49.4,116.5 50.0,116.0 50.6,115.5 51.2,115.0 51.9,114.5 52.5,114.0 53.1,113.5 53.8,113.0 54.4,112.5 55.0,112.0 55.6,111.5 56.2,111.0 56.9,110.5 57.5,110.0 58.1,109.5 58.8,109.0 59.4,108.5 60.0,108.0 60.6,107.5 61.2,107.0 61.9,106.5 62.5,106.0 63.1,105.5 63.8,105.0 64.4,104.5 65.0,104.0 65.6,103.5 66.2,103.0 66.9,102.5 67.5,102.0 68.1,101.5 68.8,101.0 69.4,100.5 70.0,100.0 70.6,99.5 71.2,99.0 71.9,98.5 72.5,98.0 73.1,97.5 73.8,97.0 74.4,96.5 75.0,96.0 75.6,95.5 76.2,95.0 76.9,94.5 77.5,94.0 78.1,93.5 78.8,93.0 79.4,92.5 80.0,92.0 80.6,91.5 81.2,91.0 81.9,90.5 82.5,90.0 83.1,89.5 83.8,89.0 84.4,88.5 85.0,88.0 85.6,87.5 86.2,87.0 86.9,86.5 87.5,86.0 88.1,85.5 88.8,85.0 89.4,84.5 90.0,84.0 90.6,83.5 91.2,83.0"/><polyline class="curve" fill="none" points="98.8,77.0 99.4,76.5 100.0,76.0 100.6,75.5 101.2,75.0 101.9,74.5 102.5,74.0 103.1,73.5 103.8,73.0 104.4,72.5 105.0,72.0 105.6,71.5 106.2,71.0 106.9,70.5 107.5,70.0 108.1,69.5 108.8,69.0 109.4,68.5 110.0,68.0 110.6,67.5 111.2,67.0 111.9,66.5 112.5,66.0 113.1,65.5 113.8,65.0 114.4,64.5 115.0,64.0 115.6,63.5 116.3,63.0 116.9,62.5 117.5,62.0 118.1,61.5 118.8,61.0 119.4,60.5 120.0,60.0 120.6,59.5 121.2,59.0 121.9,58.5 122.5,58.0 123.1,57.5 123.8,57.0 124.4,56.5 125.0,56.0 125.6,55.5 126.2,55.0 126.9,54.5 127.5,54.0 128.1,53.5 128.8,53.0 129.4,52.5 130.0,52.0 130.6,51.5 131.2,51.0 131.9,50.5 132.5,50.0 133.1,49.5 133.8,49.0 134.4,48.5 135.0,48.0 135.6,47.5 136.2,47.0 136.9,46.5 137.5,46.0 138.1,45.5 138.8,45.0 139.4,44.5 140.0,44.0 140.6,43.5 141.2,43.0 141.9,42.5 142.5,42.0 143.1,41.5 143.8,41.0 144.4,40.5 145.0,40.0 145.6,39.5 146.2,39.0 146.9,38.5 147.5,38.0 148.1,37.5 148.8,37.0 149.4,36.5 150.0,36.0 150.6,35.5 151.2,35.0 151.9,34.5 152.5,34.0 153.1,33.5 153.8,33.0 154.4,32.5 155.0,32.0 155.6,31.5 156.2,31.0 156.9,30.5 157.5,30.0 158.1,29.5 158.8,29.0 159.4,28.5 160.0,28.0 160.6,27.5 161.2,27.0 161.9,26.5 162.5,26.0 163.1,25.5 163.8,25.0 164.4,24.5 165.0,24.0 165.6,23.5 166.2,23.0 166.9,22.5 167.5,22.0 168.1,21.5 168.8,21.0 169.4,20.5 170.0,20.0"/><circle class="curve" fill="none" stroke-width="2" cx="95.0" cy="80.0" r="5"/><circle class="dot2" cx="95.0" cy="44.0" r="4.5"/><polyline class="curve" fill="none" points="210.0,110.0 210.3,110.0 210.6,110.0 210.9,110.0 211.2,110.0 211.6,110.0 211.9,110.0 212.2,110.0 212.5,110.0 212.8,110.0 213.1,110.0 213.4,110.0 213.8,110.0 214.1,110.0 214.4,110.0 214.7,110.0 215.0,110.0 215.3,110.0 215.6,110.0 215.9,110.0 216.2,110.0 216.6,110.0 216.9,110.0 217.2,110.0 217.5,110.0 217.8,110.0 218.1,110.0 218.4,110.0 218.8,110.0 219.1,110.0 219.4,110.0 219.7,110.0 220.0,110.0 220.3,110.0 220.6,110.0 220.9,110.0 221.2,110.0 221.6,110.0 221.9,110.0 222.2,110.0 222.5,110.0 222.8,110.0 223.1,110.0 223.4,110.0 223.8,110.0 224.1,110.0 224.4,110.0 224.7,110.0 225.0,110.0 225.3,110.0 225.6,110.0 225.9,110.0 226.2,110.0 226.6,110.0 226.9,110.0 227.2,110.0 227.5,110.0 227.8,110.0 228.1,110.0 228.4,110.0 228.8,110.0 229.1,110.0 229.4,110.0 229.7,110.0 230.0,110.0 230.3,110.0 230.6,110.0 230.9,110.0 231.2,110.0 231.6,110.0 231.9,110.0 232.2,110.0 232.5,110.0 232.8,110.0 233.1,110.0 233.4,110.0 233.8,110.0 234.1,110.0 234.4,110.0 234.7,110.0 235.0,110.0 235.3,110.0 235.6,110.0 235.9,110.0 236.2,110.0 236.6,110.0 236.9,110.0 237.2,110.0 237.5,110.0 237.8,110.0 238.1,110.0 238.4,110.0 238.8,110.0 239.1,110.0 239.4,110.0 239.7,110.0 240.0,110.0 240.3,110.0 240.6,110.0 240.9,110.0 241.2,110.0 241.6,110.0 241.9,110.0 242.2,110.0 242.5,110.0 242.8,110.0 243.1,110.0 243.4,110.0 243.8,110.0 244.1,110.0 244.4,110.0 244.7,110.0 245.0,110.0 245.3,110.0 245.6,110.0 245.9,110.0 246.2,110.0 246.6,110.0 246.9,110.0 247.2,110.0 247.5,110.0 247.8,110.0 248.1,110.0 248.4,110.0 248.8,110.0 249.1,110.0 249.4,110.0 249.7,110.0 250.0,110.0 250.3,110.0 250.6,110.0 250.9,110.0 251.2,110.0 251.6,110.0 251.9,110.0 252.2,110.0 252.5,110.0 252.8,110.0 253.1,110.0 253.4,110.0 253.8,110.0 254.1,110.0 254.4,110.0 254.7,110.0 255.0,110.0 255.3,110.0 255.6,110.0 255.9,110.0 256.2,110.0 256.6,110.0 256.9,110.0 257.2,110.0 257.5,110.0 257.8,110.0 258.1,110.0 258.4,110.0 258.8,110.0 259.1,110.0 259.4,110.0 259.7,110.0 260.0,110.0 260.3,110.0 260.6,110.0 260.9,110.0 261.2,110.0 261.6,110.0 261.9,110.0 262.2,110.0 262.5,110.0 262.8,110.0 263.1,110.0 263.4,110.0 263.8,110.0 264.1,110.0 264.4,110.0 264.7,110.0 265.0,110.0 265.3,110.0 265.6,110.0 265.9,110.0 266.2,110.0 266.6,110.0 266.9,110.0 267.2,110.0 267.5,110.0 267.8,110.0 268.1,110.0 268.4,110.0 268.8,110.0 269.1,110.0 269.4,110.0 269.7,110.0 270.0,110.0 270.3,110.0 270.6,110.0 270.9,110.0 271.2,110.0 271.6,110.0 271.9,110.0 272.2,110.0 272.5,110.0 272.8,110.0 273.1,110.0 273.4,110.0 273.8,110.0 274.1,110.0 274.4,110.0 274.7,110.0 275.0,110.0 275.3,110.0 275.6,110.0 275.9,110.0 276.2,110.0 276.6,110.0 276.9,110.0 277.2,110.0 277.5,110.0 277.8,110.0 278.1,110.0 278.4,110.0 278.8,110.0 279.1,110.0 279.4,110.0 279.7,110.0 280.0,110.0 280.3,110.0 280.6,110.0 280.9,110.0 281.2,110.0 281.6,110.0 281.9,110.0 282.2,110.0 282.5,110.0 282.8,110.0 283.1,110.0 283.4,110.0 283.8,110.0 284.1,110.0 284.4,110.0 284.7,110.0 285.0,110.0"/><polyline class="curve" fill="none" points="285.0,56.0 285.3,56.0 285.6,56.0 285.9,56.0 286.2,56.0 286.6,56.0 286.9,56.0 287.2,56.0 287.5,56.0 287.8,56.0 288.1,56.0 288.4,56.0 288.8,56.0 289.1,56.0 289.4,56.0 289.7,56.0 290.0,56.0 290.3,56.0 290.6,56.0 290.9,56.0 291.2,56.0 291.6,56.0 291.9,56.0 292.2,56.0 292.5,56.0 292.8,56.0 293.1,56.0 293.4,56.0 293.8,56.0 294.1,56.0 294.4,56.0 294.7,56.0 295.0,56.0 295.3,56.0 295.6,56.0 295.9,56.0 296.2,56.0 296.6,56.0 296.9,56.0 297.2,56.0 297.5,56.0 297.8,56.0 298.1,56.0 298.4,56.0 298.8,56.0 299.1,56.0 299.4,56.0 299.7,56.0 300.0,56.0 300.3,56.0 300.6,56.0 300.9,56.0 301.2,56.0 301.6,56.0 301.9,56.0 302.2,56.0 302.5,56.0 302.8,56.0 303.1,56.0 303.4,56.0 303.8,56.0 304.1,56.0 304.4,56.0 304.7,56.0 305.0,56.0 305.3,56.0 305.6,56.0 305.9,56.0 306.2,56.0 306.6,56.0 306.9,56.0 307.2,56.0 307.5,56.0 307.8,56.0 308.1,56.0 308.4,56.0 308.8,56.0 309.1,56.0 309.4,56.0 309.7,56.0 310.0,56.0 310.3,56.0 310.6,56.0 310.9,56.0 311.2,56.0 311.6,56.0 311.9,56.0 312.2,56.0 312.5,56.0 312.8,56.0 313.1,56.0 313.4,56.0 313.8,56.0 314.1,56.0 314.4,56.0 314.7,56.0 315.0,56.0 315.3,56.0 315.6,56.0 315.9,56.0 316.2,56.0 316.6,56.0 316.9,56.0 317.2,56.0 317.5,56.0 317.8,56.0 318.1,56.0 318.4,56.0 318.8,56.0 319.1,56.0 319.4,56.0 319.7,56.0 320.0,56.0 320.3,56.0 320.6,56.0 320.9,56.0 321.2,56.0 321.6,56.0 321.9,56.0 322.2,56.0 322.5,56.0 322.8,56.0 323.1,56.0 323.4,56.0 323.8,56.0 324.1,56.0 324.4,56.0 324.7,56.0 325.0,56.0 325.3,56.0 325.6,56.0 325.9,56.0 326.2,56.0 326.6,56.0 326.9,56.0 327.2,56.0 327.5,56.0 327.8,56.0 328.1,56.0 328.4,56.0 328.8,56.0 329.1,56.0 329.4,56.0 329.7,56.0 330.0,56.0 330.3,56.0 330.6,56.0 330.9,56.0 331.2,56.0 331.6,56.0 331.9,56.0 332.2,56.0 332.5,56.0 332.8,56.0 333.1,56.0 333.4,56.0 333.8,56.0 334.1,56.0 334.4,56.0 334.7,56.0 335.0,56.0 335.3,56.0 335.6,56.0 335.9,56.0 336.2,56.0 336.6,56.0 336.9,56.0 337.2,56.0 337.5,56.0 337.8,56.0 338.1,56.0 338.4,56.0 338.8,56.0 339.1,56.0 339.4,56.0 339.7,56.0 340.0,56.0 340.3,56.0 340.6,56.0 340.9,56.0 341.2,56.0 341.6,56.0 341.9,56.0 342.2,56.0 342.5,56.0 342.8,56.0 343.1,56.0 343.4,56.0 343.8,56.0 344.1,56.0 344.4,56.0 344.7,56.0 345.0,56.0 345.3,56.0 345.6,56.0 345.9,56.0 346.2,56.0 346.6,56.0 346.9,56.0 347.2,56.0 347.5,56.0 347.8,56.0 348.1,56.0 348.4,56.0 348.8,56.0 349.1,56.0 349.4,56.0 349.7,56.0 350.0,56.0 350.3,56.0 350.6,56.0 350.9,56.0 351.2,56.0 351.6,56.0 351.9,56.0 352.2,56.0 352.5,56.0 352.8,56.0 353.1,56.0 353.4,56.0 353.8,56.0 354.1,56.0 354.4,56.0 354.7,56.0 355.0,56.0 355.3,56.0 355.6,56.0 355.9,56.0 356.2,56.0 356.6,56.0 356.9,56.0 357.2,56.0 357.5,56.0 357.8,56.0 358.1,56.0 358.4,56.0 358.8,56.0 359.1,56.0 359.4,56.0 359.7,56.0 360.0,56.0"/><circle class="curve" fill="none" stroke-width="2" cx="285.0" cy="110.0" r="5"/><circle class="dot" cx="285.0" cy="56.0" r="4.5"/><polyline class="curve" fill="none" points="400.0,132.5 400.6,132.4 401.2,132.2 401.9,132.1 402.5,132.0 403.1,131.8 403.8,131.7 404.4,131.5 405.0,131.4 405.6,131.2 406.2,131.1 406.9,130.9 407.5,130.7 408.1,130.6 408.8,130.4 409.4,130.2 410.0,130.0 410.6,129.8 411.2,129.6 411.9,129.4 412.5,129.2 413.1,129.0 413.8,128.8 414.4,128.5 415.0,128.3 415.6,128.0 416.2,127.8 416.9,127.5 417.5,127.2 418.1,127.0 418.8,126.7 419.4,126.4 420.0,126.1 420.6,125.7 421.2,125.4 421.9,125.1 422.5,124.7 423.1,124.3 423.8,123.9 424.4,123.5 425.0,123.1 425.6,122.7 426.2,122.2 426.9,121.8 427.5,121.3 428.1,120.8 428.8,120.3 429.4,119.7 430.0,119.2 430.6,118.6 431.2,118.0 431.9,117.3 432.5,116.6 433.1,115.9 433.8,115.2 434.4,114.4 435.0,113.6 435.6,112.8 436.2,111.9 436.9,111.0 437.5,110.0 438.1,109.0 438.8,107.9 439.4,106.8 440.0,105.6 440.6,104.3 441.2,103.0 441.9,101.6 442.5,100.1 443.1,98.5 443.8,96.8 444.4,95.0 445.0,93.1 445.6,91.1 446.2,89.0 446.9,86.7 447.5,84.2 448.1,81.6 448.8,78.8 449.4,75.8 450.0,72.5 450.6,69.0 451.2,65.2 451.9,61.1 452.5,56.7 453.1,51.8 453.8,46.6 454.4,40.8 455.0,34.5 455.6,27.6 456.2,20.0"/><polyline class="curve" fill="none" points="493.8,20.0 494.4,27.6 495.0,34.5 495.6,40.8 496.2,46.6 496.9,51.8 497.5,56.7 498.1,61.1 498.8,65.2 499.4,69.0 500.0,72.5 500.6,75.8 501.2,78.8 501.9,81.6 502.5,84.2 503.1,86.7 503.8,89.0 504.4,91.1 505.0,93.1 505.6,95.0 506.2,96.8 506.9,98.5 507.5,100.1 508.1,101.6 508.8,103.0 509.4,104.3 510.0,105.6 510.6,106.8 511.2,107.9 511.9,109.0 512.5,110.0 513.1,111.0 513.8,111.9 514.4,112.8 515.0,113.6 515.6,114.4 516.2,115.2 516.9,115.9 517.5,116.6 518.1,117.3 518.8,118.0 519.4,118.6 520.0,119.2 520.6,119.7 521.2,120.3 521.9,120.8 522.5,121.3 523.1,121.8 523.8,122.2 524.4,122.7 525.0,123.1 525.6,123.5 526.2,123.9 526.9,124.3 527.5,124.7 528.1,125.1 528.8,125.4 529.4,125.7 530.0,126.1 530.6,126.4 531.2,126.7 531.9,127.0 532.5,127.2 533.1,127.5 533.8,127.8 534.4,128.0 535.0,128.3 535.6,128.5 536.2,128.8 536.9,129.0 537.5,129.2 538.1,129.4 538.8,129.6 539.4,129.8 540.0,130.0 540.6,130.2 541.2,130.4 541.9,130.6 542.5,130.7 543.1,130.9 543.8,131.1 544.4,131.2 545.0,131.4 545.6,131.5 546.2,131.7 546.9,131.8 547.5,132.0 548.1,132.1 548.8,132.2 549.4,132.4 550.0,132.5"/><line class="curve3" stroke-dasharray="5 4" x1="475.0" y1="170.0" x2="475.0" y2="20.0"/><text class="ink" x="95.0" y="192" font-size="13" text-anchor="middle">hole</text><text class="dim" x="95.0" y="210" font-size="10.5" text-anchor="middle">the limit exists but f(1) ≠ limit</text><text class="ink" x="285.0" y="192" font-size="13" text-anchor="middle">jump</text><text class="dim" x="285.0" y="210" font-size="10.5" text-anchor="middle">different from left and right</text><text class="ink" x="475.0" y="192" font-size="13" text-anchor="middle">infinite</text><text class="dim" x="475.0" y="210" font-size="10.5" text-anchor="middle">the value runs off to infinity</text></svg>
  <figcaption>Three kinds of discontinuity. At a hole the limit exists but the value is somewhere else (or missing). At a jump the left and right limits differ. At an infinite discontinuity the function grows without bound at the asymptote.</figcaption>
</figure>

Polynomials, exponential functions, sine and cosine are continuous
everywhere. Fractions are continuous wherever the denominator is not
zero, roots and logarithms within their domains. Sums, products and
compositions of continuous functions are continuous too.

**The intermediate value theorem.** A function continuous on $[a, b]$
takes every value between $f(a)$ and $f(b)$ somewhere. For example, if
$f(1) < 0$ and $f(2) > 0$, there is a root between $1$ and $2$. Halving
the interval at each step and keeping the half where the sign changes
(the **bisection method**) finds the root to any precision we want.

## Limits and continuity in machine learning

**The derivative is a limit.** The topic of the next section, the rate of
change of the loss with respect to a weight, is defined by the limit

$$
\lim_{h \to 0} \frac{f(x + h) - f(x)}{h}
$$

Substituting here gives $\frac{0}{0}$ as well; the simplifying skills of
this section are needed exactly there.

**The choice of activation is about continuity.** The first artificial
neurons used a step function: a discontinuous function that jumps from
$0$ to $1$ at $0$. At the jump the slope is undefined and everywhere else
it is zero; gradient-based learning cannot make progress. The sigmoid is
a continuous, smooth version of the step. ReLU $\max(0, x)$ is
continuous but has a kink at $0$; we will see in the derivatives section
why that is not a problem.

**Behaviour at infinity describes saturation.** Because $\sigma(x) \to 1$,
the sigmoid is almost flat for very large inputs; the input changes but
the output does not. This is called **saturation**, and it slows learning
in deep networks.

**Convergence is a limit.** The loss settling step by step on a value
during training means that $\lim_{t \to \infty} L_t$ exists.

## Common mistakes

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Wrong</h4>
      <p>$\dfrac{0}{0} = 0$ or $1$</p>
      <p>If $f(a)$ is undefined, there is no limit</p>
      <p>$\lim_{x \to a} f(x) = f(a)$, always</p>
      <p>$\infty - \infty = 0$</p>
    </div>
    <div class="ok">
      <h4>Right</h4>
      <p>$\dfrac{0}{0}$ is indeterminate: simplify</p>
      <p>The limit looks around the point</p>
      <p>That equality is continuity</p>
      <p>Indeterminate: rewrite the expression</p>
    </div>
  </div>
  <figcaption>Indeterminate forms (0/0, ∞/∞, ∞ − ∞) are not a result but a sign to write the expression another way.</figcaption>
</figure>

- **Not checking one-sided limits.** For piecewise functions, work out
  both sides separately at the boundary point.
- **Treating $\infty$ as a number.** $\frac{\infty}{\infty}$ or $\infty
  \cdot 0$ is not a value; a rewrite such as dividing by the highest power
  is needed.

## Summary

- $\lim_{x \to a} f(x) = L$: as $x$ approaches $a$, $f(x)$ approaches $L$; what $f(a)$ is does not matter.
- For a limit, the left and right limits must be the same.
- Calculation: substitute first; if you get $\frac{0}{0}$, factor or multiply by the conjugate.
- At infinity: divide by the highest power; comparing degrees is the shortcut.
- $e = \lim_{n \to \infty} \left(1 + \frac{1}{n}\right)^n \approx 2.718$.
- Continuity: $f(a)$ defined, the limit exists, the two are equal. Kinds: hole, jump, infinite.
- The derivative is a limit; the sigmoid is a continuous step; saturation is behaviour at infinity.
