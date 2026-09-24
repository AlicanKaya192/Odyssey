# The Coordinate Plane and Lines

The coordinate plane is the bridge between numbers and shapes. A point is
written with two numbers and a line with an equation; so we can solve a
geometry question with algebra and see an algebra question by drawing it.
Linear regression, the most basic model of machine learning, is exactly a
line too: it looks for the best line through the data. In this section we
will see the plane, the distance between two points, slope, the equation
of a line and how lines sit relative to each other.

Prerequisite: Roots, Systems of Equations, Functions.

## The coordinate plane

Two number lines crossing at right angles at zero: the horizontal one is
the $x$-axis, the vertical one the $y$-axis. The point where they cross is
the **origin**, $(0, 0)$. Every point is written as an **ordered pair**
$(x, y)$: first how far right (or left), then how far up (or down).

<figure class="fig">
<svg viewBox="0 0 400 340" width="400"><line class="grid" x1="40.0" y1="320.0" x2="40.0" y2="20.0"/><line class="grid" x1="40.0" y1="320.0" x2="340.0" y2="320.0"/><line class="grid" x1="70.0" y1="320.0" x2="70.0" y2="20.0"/><line class="grid" x1="40.0" y1="290.0" x2="340.0" y2="290.0"/><line class="grid" x1="100.0" y1="320.0" x2="100.0" y2="20.0"/><line class="grid" x1="40.0" y1="260.0" x2="340.0" y2="260.0"/><line class="grid" x1="130.0" y1="320.0" x2="130.0" y2="20.0"/><line class="grid" x1="40.0" y1="230.0" x2="340.0" y2="230.0"/><line class="grid" x1="160.0" y1="320.0" x2="160.0" y2="20.0"/><line class="grid" x1="40.0" y1="200.0" x2="340.0" y2="200.0"/><line class="grid" x1="190.0" y1="320.0" x2="190.0" y2="20.0"/><line class="grid" x1="40.0" y1="170.0" x2="340.0" y2="170.0"/><line class="grid" x1="220.0" y1="320.0" x2="220.0" y2="20.0"/><line class="grid" x1="40.0" y1="140.0" x2="340.0" y2="140.0"/><line class="grid" x1="250.0" y1="320.0" x2="250.0" y2="20.0"/><line class="grid" x1="40.0" y1="110.0" x2="340.0" y2="110.0"/><line class="grid" x1="280.0" y1="320.0" x2="280.0" y2="20.0"/><line class="grid" x1="40.0" y1="80.0" x2="340.0" y2="80.0"/><line class="grid" x1="310.0" y1="320.0" x2="310.0" y2="20.0"/><line class="grid" x1="40.0" y1="50.0" x2="340.0" y2="50.0"/><line class="grid" x1="340.0" y1="320.0" x2="340.0" y2="20.0"/><line class="grid" x1="40.0" y1="20.0" x2="340.0" y2="20.0"/><line class="line" x1="40.0" y1="170.0" x2="340.0" y2="170.0"/><line class="line" x1="190.0" y1="320.0" x2="190.0" y2="20.0"/><text class="dim" x="40.0" y="183.0" font-size="9" text-anchor="middle">−5</text><text class="dim" x="185.0" y="323.0" font-size="9" text-anchor="end">−5</text><text class="dim" x="70.0" y="183.0" font-size="9" text-anchor="middle">−4</text><text class="dim" x="185.0" y="293.0" font-size="9" text-anchor="end">−4</text><text class="dim" x="100.0" y="183.0" font-size="9" text-anchor="middle">−3</text><text class="dim" x="185.0" y="263.0" font-size="9" text-anchor="end">−3</text><text class="dim" x="130.0" y="183.0" font-size="9" text-anchor="middle">−2</text><text class="dim" x="185.0" y="233.0" font-size="9" text-anchor="end">−2</text><text class="dim" x="160.0" y="183.0" font-size="9" text-anchor="middle">−1</text><text class="dim" x="185.0" y="203.0" font-size="9" text-anchor="end">−1</text><text class="dim" x="220.0" y="183.0" font-size="9" text-anchor="middle">1</text><text class="dim" x="185.0" y="143.0" font-size="9" text-anchor="end">1</text><text class="dim" x="250.0" y="183.0" font-size="9" text-anchor="middle">2</text><text class="dim" x="185.0" y="113.0" font-size="9" text-anchor="end">2</text><text class="dim" x="280.0" y="183.0" font-size="9" text-anchor="middle">3</text><text class="dim" x="185.0" y="83.0" font-size="9" text-anchor="end">3</text><text class="dim" x="310.0" y="183.0" font-size="9" text-anchor="middle">4</text><text class="dim" x="185.0" y="53.0" font-size="9" text-anchor="end">4</text><text class="dim" x="340.0" y="183.0" font-size="9" text-anchor="middle">5</text><text class="dim" x="185.0" y="23.0" font-size="9" text-anchor="end">5</text><text class="dim" x="289.0" y="41.0" font-size="11" text-anchor="middle">quadrant I</text><text class="dim" x="91.0" y="41.0" font-size="11" text-anchor="middle">quadrant II</text><text class="dim" x="91.0" y="305.0" font-size="11" text-anchor="middle">quadrant III</text><text class="dim" x="289.0" y="305.0" font-size="11" text-anchor="middle">quadrant IV</text><circle class="dot" cx="280.0" cy="110.0" r="5"/><text class="ink" x="288.0" y="103.0" font-size="11" text-anchor="start">A(3, 2)</text><circle class="dot2" cx="130.0" cy="140.0" r="5"/><text class="ink" x="138.0" y="133.0" font-size="11" text-anchor="start">B(−2, 1)</text><circle class="dot3" cx="100.0" cy="230.0" r="5"/><text class="ink" x="108.0" y="223.0" font-size="11" text-anchor="start">C(−3, −2)</text><circle class="dot" cx="250.0" cy="260.0" r="5"/><text class="ink" x="258.0" y="253.0" font-size="11" text-anchor="start">D(2, −3)</text><text class="ink" x="348.0" y="174.0" font-size="12" text-anchor="start">x</text><text class="ink" x="190.0" y="14.0" font-size="12" text-anchor="middle">y</text></svg>
  <figcaption>The axes split the plane into four quadrants. A(3, 2) is right and up, B(−2, 1) left and up, C(−3, −2) left and down, D(2, −3) right and down.</figcaption>
</figure>

| Quadrant | $x$ | $y$ | Example |
|---|---|---|---|
| I | $+$ | $+$ | $(3, 2)$ |
| II | $-$ | $+$ | $(-2, 1)$ |
| III | $-$ | $-$ | $(-3, -2)$ |
| IV | $+$ | $-$ | $(2, -3)$ |

**Order matters:** $(3, 2)$ and $(2, 3)$ are different points. Points on
an axis belong to no quadrant: on the $x$-axis $y = 0$, on the $y$-axis
$x = 0$.

## The distance between two points

The segment joining two points is the hypotenuse of a right triangle whose
legs are the horizontal and vertical differences. Pythagoras gives the
distance.

<figure class="fig">
<svg viewBox="0 0 400 296.0" width="400"><line class="grid" x1="40.0" y1="260.0" x2="40.0" y2="20.0"/><line class="grid" x1="40.0" y1="260.0" x2="280.0" y2="260.0"/><line class="grid" x1="74.3" y1="260.0" x2="74.3" y2="20.0"/><line class="grid" x1="40.0" y1="225.7" x2="280.0" y2="225.7"/><line class="grid" x1="108.6" y1="260.0" x2="108.6" y2="20.0"/><line class="grid" x1="40.0" y1="191.4" x2="280.0" y2="191.4"/><line class="grid" x1="142.9" y1="260.0" x2="142.9" y2="20.0"/><line class="grid" x1="40.0" y1="157.1" x2="280.0" y2="157.1"/><line class="grid" x1="177.1" y1="260.0" x2="177.1" y2="20.0"/><line class="grid" x1="40.0" y1="122.9" x2="280.0" y2="122.9"/><line class="grid" x1="211.4" y1="260.0" x2="211.4" y2="20.0"/><line class="grid" x1="40.0" y1="88.6" x2="280.0" y2="88.6"/><line class="grid" x1="245.7" y1="260.0" x2="245.7" y2="20.0"/><line class="grid" x1="40.0" y1="54.3" x2="280.0" y2="54.3"/><line class="grid" x1="280.0" y1="260.0" x2="280.0" y2="20.0"/><line class="grid" x1="40.0" y1="20.0" x2="280.0" y2="20.0"/><line class="line" x1="40.0" y1="225.7" x2="280.0" y2="225.7"/><line class="line" x1="74.3" y1="260.0" x2="74.3" y2="20.0"/><text class="dim" x="40.0" y="238.7" font-size="9" text-anchor="middle">−1</text><text class="dim" x="69.3" y="263.0" font-size="9" text-anchor="end">−1</text><text class="dim" x="108.6" y="238.7" font-size="9" text-anchor="middle">1</text><text class="dim" x="69.3" y="194.4" font-size="9" text-anchor="end">1</text><text class="dim" x="142.9" y="238.7" font-size="9" text-anchor="middle">2</text><text class="dim" x="69.3" y="160.1" font-size="9" text-anchor="end">2</text><text class="dim" x="177.1" y="238.7" font-size="9" text-anchor="middle">3</text><text class="dim" x="69.3" y="125.9" font-size="9" text-anchor="end">3</text><text class="dim" x="211.4" y="238.7" font-size="9" text-anchor="middle">4</text><text class="dim" x="69.3" y="91.6" font-size="9" text-anchor="end">4</text><text class="dim" x="245.7" y="238.7" font-size="9" text-anchor="middle">5</text><text class="dim" x="69.3" y="57.3" font-size="9" text-anchor="end">5</text><text class="dim" x="280.0" y="238.7" font-size="9" text-anchor="middle">6</text><text class="dim" x="69.3" y="23.0" font-size="9" text-anchor="end">6</text><polygon class="curve2" fill="none" points="108.6,191.4 211.4,191.4 211.4,54.3"/><line class="curve" x1="108.6" y1="191.4" x2="211.4" y2="54.3"/><polyline class="dim" fill="none" stroke-width="1" points="202.9,191.4 202.9,182.9 211.4,182.9"/><circle class="dot" cx="108.6" cy="191.4" r="5"/><circle class="dot" cx="211.4" cy="54.3" r="5"/><text class="ink" x="100.6" y="183.4" font-size="11" text-anchor="end">P(1, 1)</text><text class="ink" x="219.4" y="50.3" font-size="11" text-anchor="start">Q(4, 5)</text><text class="ink" x="160.0" y="208.4" font-size="11" text-anchor="middle">Δx = 4 − 1 = 3</text><text class="ink" x="219.4" y="126.9" font-size="11" text-anchor="start">Δy = 5 − 1 = 4</text><text class="ink" x="160.0" y="286.0" font-size="13" text-anchor="middle">d = √(3² + 4²) = 5</text></svg>
  <figcaption>Between P(1, 1) and Q(4, 5) the horizontal difference is 3 and the vertical difference 4. These two sides form a right triangle; the hypotenuse, the distance PQ, is 5.</figcaption>
</figure>

$$
d = \sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}
$$

For $P(1, 1)$ and $Q(4, 5)$, $d = \sqrt{3^2 + 4^2} = \sqrt{25} = 5$.
Because the differences are squared, it does not matter which point is
written first.

**The midpoint.** The exact middle of two points is the average of the
coordinates:

$$
M = \left( \frac{x_1 + x_2}{2}, \ \frac{y_1 + y_2}{2} \right)
$$

For $A(-2, 3)$ and $B(4, 7)$, $M = \left( \frac{2}{2}, \frac{10}{2} \right) = (1, 5)$.

## Slope

The **slope** of a line is how many units it rises when you go one unit to
the right. It is worked out from two of its points: the vertical change
divided by the horizontal change.

$$
m = \frac{\Delta y}{\Delta x} = \frac{y_2 - y_1}{x_2 - x_1}
$$

<figure class="fig">
<svg viewBox="0 0 440 322.0" width="440"><line class="grid" x1="40.0" y1="280.0" x2="40.0" y2="20.0"/><line class="grid" x1="40.0" y1="280.0" x2="300.0" y2="280.0"/><line class="grid" x1="63.6" y1="280.0" x2="63.6" y2="20.0"/><line class="grid" x1="40.0" y1="256.4" x2="300.0" y2="256.4"/><line class="grid" x1="87.3" y1="280.0" x2="87.3" y2="20.0"/><line class="grid" x1="40.0" y1="232.7" x2="300.0" y2="232.7"/><line class="grid" x1="110.9" y1="280.0" x2="110.9" y2="20.0"/><line class="grid" x1="40.0" y1="209.1" x2="300.0" y2="209.1"/><line class="grid" x1="134.5" y1="280.0" x2="134.5" y2="20.0"/><line class="grid" x1="40.0" y1="185.5" x2="300.0" y2="185.5"/><line class="grid" x1="158.2" y1="280.0" x2="158.2" y2="20.0"/><line class="grid" x1="40.0" y1="161.8" x2="300.0" y2="161.8"/><line class="grid" x1="181.8" y1="280.0" x2="181.8" y2="20.0"/><line class="grid" x1="40.0" y1="138.2" x2="300.0" y2="138.2"/><line class="grid" x1="205.5" y1="280.0" x2="205.5" y2="20.0"/><line class="grid" x1="40.0" y1="114.5" x2="300.0" y2="114.5"/><line class="grid" x1="229.1" y1="280.0" x2="229.1" y2="20.0"/><line class="grid" x1="40.0" y1="90.9" x2="300.0" y2="90.9"/><line class="grid" x1="252.7" y1="280.0" x2="252.7" y2="20.0"/><line class="grid" x1="40.0" y1="67.3" x2="300.0" y2="67.3"/><line class="grid" x1="276.4" y1="280.0" x2="276.4" y2="20.0"/><line class="grid" x1="40.0" y1="43.6" x2="300.0" y2="43.6"/><line class="grid" x1="300.0" y1="280.0" x2="300.0" y2="20.0"/><line class="grid" x1="40.0" y1="20.0" x2="300.0" y2="20.0"/><line class="line" x1="40.0" y1="256.4" x2="300.0" y2="256.4"/><line class="line" x1="63.6" y1="280.0" x2="63.6" y2="20.0"/><text class="dim" x="110.9" y="269.4" font-size="9" text-anchor="middle">2</text><text class="dim" x="58.6" y="212.1" font-size="9" text-anchor="end">2</text><text class="dim" x="158.2" y="269.4" font-size="9" text-anchor="middle">4</text><text class="dim" x="58.6" y="164.8" font-size="9" text-anchor="end">4</text><text class="dim" x="205.5" y="269.4" font-size="9" text-anchor="middle">6</text><text class="dim" x="58.6" y="117.5" font-size="9" text-anchor="end">6</text><text class="dim" x="252.7" y="269.4" font-size="9" text-anchor="middle">8</text><text class="dim" x="58.6" y="70.3" font-size="9" text-anchor="end">8</text><text class="dim" x="300.0" y="269.4" font-size="9" text-anchor="middle">10</text><text class="dim" x="58.6" y="23.0" font-size="9" text-anchor="end">10</text><line class="curve" x1="51.8" y1="256.4" x2="170.0" y2="20.0"/><line class="curve2" x1="87.3" y1="185.5" x2="158.2" y2="185.5"/><line class="curve2" x1="158.2" y1="185.5" x2="158.2" y2="43.6"/><circle class="dot" cx="87.3" cy="185.5" r="5"/><circle class="dot" cx="158.2" cy="43.6" r="5"/><circle class="dot3" cx="63.6" cy="232.7" r="5"/><text class="ink" x="129.8" y="201.5" font-size="11" text-anchor="middle">run Δx = 3</text><text class="ink" x="166.2" y="118.5" font-size="11" text-anchor="start">rise Δy = 6</text><text class="ink" x="81.3" y="177.5" font-size="11" text-anchor="end">(1, 3)</text><text class="ink" x="150.2" y="37.6" font-size="11" text-anchor="end">(4, 9)</text><text class="dim" x="73.6" y="248.7" font-size="11" text-anchor="start">y-intercept b = 1</text><text class="ink" x="193.6" y="310.0" font-size="13" text-anchor="middle">slope m = 6 / 3 = 2</text></svg>
  <figcaption>Between (1, 3) and (4, 9), going 3 units right the line rises 6 units; the slope is 6 / 3 = 2. The line crosses the y-axis at 1.</figcaption>
</figure>

The sign of the slope tells the direction of the line:

| Slope | Line | Example |
|---|---|---|
| $m > 0$ | rises to the right | $y = 2x + 1$ |
| $m < 0$ | falls to the right | $y = -x + 4$ |
| $m = 0$ | horizontal | $y = 3$ |
| undefined | vertical | $x = 2$ |

On a vertical line $\Delta x = 0$; since we cannot divide by zero, the
slope is undefined. The "following the slope" of the Systems of Equations
section was this: each time $x$ goes up by one, $y$ changes by the slope.

## The equation of a line

**Slope–intercept form.** The line with slope $m$ crossing the $y$-axis at
$b$:

$$
y = mx + b
$$

The line above has slope $2$; putting in the point $(1, 3)$ gives $3 = 2
\cdot 1 + b$, so $b = 1$. The equation is $y = 2x + 1$.

**Point–slope form.** The line with a known point $(x_1, y_1)$ and slope
$m$:

$$
y - y_1 = m(x - x_1)
$$

The line with slope $3$ through $(2, 5)$: $y - 5 = 3(x - 2)$, that is,
$y = 3x - 1$.

**General form.** $ax + by + c = 0$, for example $2x + 3y - 6 = 0$.
Getting $y$ on its own gives $y = -\frac{2}{3}x + 2$: slope $-\frac{2}{3}$.
The axis crossings are easy too: $x = 0$ gives $y = 2$, and $y = 0$ gives
$x = 3$.

**Horizontal and vertical lines.** $y = 4$ is a horizontal line with slope
$0$. $x = 3$ is a vertical line; its slope is undefined and it cannot be
written as $y = mx + b$. Remember the vertical line test: the line $x = 3$
is not the graph of a function.

**Is the point on the line?** Put its coordinates into the equation; if
the equality holds, it is on the line. For $(2, 5)$ and $y = 2x + 1$: $2
\cdot 2 + 1 = 5$ ✓.

## Parallel and perpendicular lines

<figure class="fig">
<svg viewBox="0 0 400 385" width="400"><line class="grid" x1="40.0" y1="320.0" x2="40.0" y2="20.0"/><line class="grid" x1="40.0" y1="320.0" x2="340.0" y2="320.0"/><line class="grid" x1="70.0" y1="320.0" x2="70.0" y2="20.0"/><line class="grid" x1="40.0" y1="290.0" x2="340.0" y2="290.0"/><line class="grid" x1="100.0" y1="320.0" x2="100.0" y2="20.0"/><line class="grid" x1="40.0" y1="260.0" x2="340.0" y2="260.0"/><line class="grid" x1="130.0" y1="320.0" x2="130.0" y2="20.0"/><line class="grid" x1="40.0" y1="230.0" x2="340.0" y2="230.0"/><line class="grid" x1="160.0" y1="320.0" x2="160.0" y2="20.0"/><line class="grid" x1="40.0" y1="200.0" x2="340.0" y2="200.0"/><line class="grid" x1="190.0" y1="320.0" x2="190.0" y2="20.0"/><line class="grid" x1="40.0" y1="170.0" x2="340.0" y2="170.0"/><line class="grid" x1="220.0" y1="320.0" x2="220.0" y2="20.0"/><line class="grid" x1="40.0" y1="140.0" x2="340.0" y2="140.0"/><line class="grid" x1="250.0" y1="320.0" x2="250.0" y2="20.0"/><line class="grid" x1="40.0" y1="110.0" x2="340.0" y2="110.0"/><line class="grid" x1="280.0" y1="320.0" x2="280.0" y2="20.0"/><line class="grid" x1="40.0" y1="80.0" x2="340.0" y2="80.0"/><line class="grid" x1="310.0" y1="320.0" x2="310.0" y2="20.0"/><line class="grid" x1="40.0" y1="50.0" x2="340.0" y2="50.0"/><line class="grid" x1="340.0" y1="320.0" x2="340.0" y2="20.0"/><line class="grid" x1="40.0" y1="20.0" x2="340.0" y2="20.0"/><line class="line" x1="40.0" y1="170.0" x2="340.0" y2="170.0"/><line class="line" x1="190.0" y1="320.0" x2="190.0" y2="20.0"/><text class="dim" x="40.0" y="183.0" font-size="9" text-anchor="middle">−5</text><text class="dim" x="185.0" y="323.0" font-size="9" text-anchor="end">−5</text><text class="dim" x="70.0" y="183.0" font-size="9" text-anchor="middle">−4</text><text class="dim" x="185.0" y="293.0" font-size="9" text-anchor="end">−4</text><text class="dim" x="100.0" y="183.0" font-size="9" text-anchor="middle">−3</text><text class="dim" x="185.0" y="263.0" font-size="9" text-anchor="end">−3</text><text class="dim" x="130.0" y="183.0" font-size="9" text-anchor="middle">−2</text><text class="dim" x="185.0" y="233.0" font-size="9" text-anchor="end">−2</text><text class="dim" x="160.0" y="183.0" font-size="9" text-anchor="middle">−1</text><text class="dim" x="185.0" y="203.0" font-size="9" text-anchor="end">−1</text><text class="dim" x="220.0" y="183.0" font-size="9" text-anchor="middle">1</text><text class="dim" x="185.0" y="143.0" font-size="9" text-anchor="end">1</text><text class="dim" x="250.0" y="183.0" font-size="9" text-anchor="middle">2</text><text class="dim" x="185.0" y="113.0" font-size="9" text-anchor="end">2</text><text class="dim" x="280.0" y="183.0" font-size="9" text-anchor="middle">3</text><text class="dim" x="185.0" y="83.0" font-size="9" text-anchor="end">3</text><text class="dim" x="310.0" y="183.0" font-size="9" text-anchor="middle">4</text><text class="dim" x="185.0" y="53.0" font-size="9" text-anchor="end">4</text><text class="dim" x="340.0" y="183.0" font-size="9" text-anchor="middle">5</text><text class="dim" x="185.0" y="23.0" font-size="9" text-anchor="end">5</text><line class="curve" x1="100.0" y1="320.0" x2="250.0" y2="20.0"/><line class="curve" x1="160.0" y1="320.0" x2="310.0" y2="20.0"/><line class="curve3" x1="40.0" y1="65.0" x2="340.0" y2="215.0"/><text class="ink" x="236.0" y="36.0" font-size="11" text-anchor="end">y = 2x + 1</text><text class="ink" x="316.0" y="56.0" font-size="11" text-anchor="start">y = 2x − 3</text><text class="ink" x="43.0" y="57.0" font-size="11" text-anchor="start">y = −½x + 1</text><text class="ink" x="190" y="355" font-size="12" text-anchor="middle">parallel: same slope (m = 2)</text><text class="ink" x="190" y="375" font-size="12" text-anchor="middle">perpendicular: slopes multiply to −1 (2 · (−½) = −1)</text></svg>
  <figcaption>The lines y = 2x + 1 and y = 2x − 3 have the same slope (2) and differ only where they cross the y-axis: they are parallel and never meet. The third line has slope −½; its product with 2 is −1, so it is perpendicular to the others.</figcaption>
</figure>

- **Parallel:** equal slopes, $m_1 = m_2$ (and different $b$; if $b$ is
  the same too, the two equations are the same line).
- **Perpendicular:** the slopes multiply to $-1$, that is, $m_2 =
  -\dfrac{1}{m_1}$. Flip the slope and change its sign: perpendicular to
  $2$ is $-\frac{1}{2}$, perpendicular to $-\frac{3}{4}$ is $\frac{4}{3}$.

A horizontal and a vertical line are also perpendicular; there one slope
is undefined, so the product rule is not used.

## Where two lines meet

The intersection point satisfies both equations at once; this is a system
of equations. For $y = 2x + 1$ and $y = -x + 7$, set the right-hand sides
equal:

$$
\begin{aligned}
&2x + 1 = -x + 7 \\
\Rightarrow\; &3x = 6 \\
\Rightarrow\; &x = 2
\end{aligned}
$$

$y = 2 \cdot 2 + 1 = 5$; they meet at $(2, 5)$. If the slopes are equal,
the lines either never meet (parallel) or are the same line.

## Lines in machine learning

**Linear regression is a line.** In the model $\hat{y} = wx + b$, $w$ is
the slope and $b$ where it crosses the $y$-axis. The model $\hat{y} = 3x +
50$ (in thousands), predicting a house price from its floor area, says
"each square metre adds 3 thousand to the price, from a base of 50
thousand". Training is finding the best $w$ and $b$ for a line through the
points.

**The error is a vertical distance.** The vertical difference $y_i -
\hat{y}_i$ between a data point $(x_i, y_i)$ and the line is the error on
that example. The loss function adds up the squares of these differences.

**The distance formula is everywhere.** The $k$-nearest neighbours method
classifies a new example by looking at the examples closest to it;
"closest" is measured with the distance formula we saw here (the
Euclidean distance).

**A decision boundary is a line.** A classifier with two features splits
the plane in two with the line $w_1 x_1 + w_2 x_2 + b = 0$: one side is
one class, the other side the other class. This is the general form of a
line.

## Common mistakes

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Wrong</h4>
      <p>$m = \dfrac{x_2 - x_1}{y_2 - y_1}$</p>
      <p>$m = \dfrac{y_2 - y_1}{x_1 - x_2}$</p>
      <p>$d = (x_2 - x_1) + (y_2 - y_1)$</p>
      <p>Perpendicular slope: $2 \to -2$</p>
    </div>
    <div class="ok">
      <h4>Right</h4>
      <p>$m = \dfrac{y_2 - y_1}{x_2 - x_1}$</p>
      <p>The same order on top and bottom</p>
      <p>$d = \sqrt{\Delta x^2 + \Delta y^2}$</p>
      <p>Perpendicular slope: $2 \to -\dfrac{1}{2}$</p>
    </div>
  </div>
  <figcaption>In the slope the vertical change goes on top, and both differences take the points in the same order.</figcaption>
</figure>

- **Reading the ordered pair backwards.** In $(3, 2)$, $x$ comes first:
  right $3$, up $2$.
- **Giving a vertical line a slope.** The slope of the line $x = 3$ is not
  $0$ but undefined. The line with slope $0$ is a horizontal line.

## Summary

- A point $(x, y)$: horizontal first, then vertical; the signs change across the four quadrants.
- Distance $d = \sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}$; the midpoint is the average of the coordinates.
- Slope $m = \dfrac{y_2 - y_1}{x_2 - x_1}$; $0$ for horizontal, undefined for vertical.
- A line: $y = mx + b$, $y - y_1 = m(x - x_1)$ or $ax + by + c = 0$.
- Parallel lines have equal slopes; perpendicular slopes multiply to $-1$.
- The intersection is found by solving the system of the two lines.
- Linear regression is a line, the error a vertical distance, a decision boundary a line equation.
