# Systems of Equations

With two unknowns, one equation is not enough: infinitely many pairs $(x,
y)$ satisfy $x + y = 10$. Adding a second condition ($x - y = 4$) narrows
the solution down to a single pair. Asking several equations to hold **at
the same time** is called a **system of equations**. Drawing a line through
two points, finding the proportions in a mixture or recovering a model's
parameters from data all mean solving a system.

Prerequisite: Linear Equations.

## What is a system?

$$
\begin{cases}
x + y = 10 \\
x - y = 4
\end{cases}
$$

A solution is a pair $(x, y)$ that satisfies **both equations at once**.
$(6, 4)$ satisfies the first ($6 + 4 = 10$) but not the second ($6 - 4 =
2$). $(7, 3)$ satisfies both: it is the solution of the system.

## A system on a graph

Every linear equation draws a line in the plane. Every point on the line
satisfies that equation. The point satisfying both equations is where the
two lines **cross**.

<figure class="fig">
<svg viewBox="0 0 400 458.0" width="400"><line class="grid" x1="50.0" y1="420.0" x2="50.0" y2="20.0"/><line class="grid" x1="75.0" y1="420.0" x2="75.0" y2="20.0"/><line class="grid" x1="100.0" y1="420.0" x2="100.0" y2="20.0"/><line class="grid" x1="125.0" y1="420.0" x2="125.0" y2="20.0"/><line class="grid" x1="150.0" y1="420.0" x2="150.0" y2="20.0"/><line class="grid" x1="175.0" y1="420.0" x2="175.0" y2="20.0"/><line class="grid" x1="200.0" y1="420.0" x2="200.0" y2="20.0"/><line class="grid" x1="225.0" y1="420.0" x2="225.0" y2="20.0"/><line class="grid" x1="250.0" y1="420.0" x2="250.0" y2="20.0"/><line class="grid" x1="275.0" y1="420.0" x2="275.0" y2="20.0"/><line class="grid" x1="300.0" y1="420.0" x2="300.0" y2="20.0"/><line class="grid" x1="325.0" y1="420.0" x2="325.0" y2="20.0"/><line class="grid" x1="350.0" y1="420.0" x2="350.0" y2="20.0"/><line class="grid" x1="50.0" y1="420.0" x2="350.0" y2="420.0"/><line class="grid" x1="50.0" y1="395.0" x2="350.0" y2="395.0"/><line class="grid" x1="50.0" y1="370.0" x2="350.0" y2="370.0"/><line class="grid" x1="50.0" y1="345.0" x2="350.0" y2="345.0"/><line class="grid" x1="50.0" y1="320.0" x2="350.0" y2="320.0"/><line class="grid" x1="50.0" y1="295.0" x2="350.0" y2="295.0"/><line class="grid" x1="50.0" y1="270.0" x2="350.0" y2="270.0"/><line class="grid" x1="50.0" y1="245.0" x2="350.0" y2="245.0"/><line class="grid" x1="50.0" y1="220.0" x2="350.0" y2="220.0"/><line class="grid" x1="50.0" y1="195.0" x2="350.0" y2="195.0"/><line class="grid" x1="50.0" y1="170.0" x2="350.0" y2="170.0"/><line class="grid" x1="50.0" y1="145.0" x2="350.0" y2="145.0"/><line class="grid" x1="50.0" y1="120.0" x2="350.0" y2="120.0"/><line class="grid" x1="50.0" y1="95.0" x2="350.0" y2="95.0"/><line class="grid" x1="50.0" y1="70.0" x2="350.0" y2="70.0"/><line class="grid" x1="50.0" y1="45.0" x2="350.0" y2="45.0"/><line class="grid" x1="50.0" y1="20.0" x2="350.0" y2="20.0"/><line class="line" x1="50.0" y1="295.0" x2="350.0" y2="295.0"/><line class="line" x1="75.0" y1="420.0" x2="75.0" y2="20.0"/><text class="dim" x="125.0" y="308.0" font-size="9" text-anchor="middle">2</text><text class="dim" x="175.0" y="308.0" font-size="9" text-anchor="middle">4</text><text class="dim" x="225.0" y="308.0" font-size="9" text-anchor="middle">6</text><text class="dim" x="275.0" y="308.0" font-size="9" text-anchor="middle">8</text><text class="dim" x="325.0" y="308.0" font-size="9" text-anchor="middle">10</text><text class="dim" x="70.0" y="398.0" font-size="9" text-anchor="end">−4</text><text class="dim" x="70.0" y="248.0" font-size="9" text-anchor="end">2</text><text class="dim" x="70.0" y="198.0" font-size="9" text-anchor="end">4</text><text class="dim" x="70.0" y="148.0" font-size="9" text-anchor="end">6</text><text class="dim" x="70.0" y="98.0" font-size="9" text-anchor="end">8</text><text class="dim" x="70.0" y="48.0" font-size="9" text-anchor="end">10</text><line class="curve" x1="50.0" y1="20.0" x2="350.0" y2="320.0"/><line class="curve2" x1="50.0" y1="420.0" x2="350.0" y2="120.0"/><text class="ink" x="90.0" y="29.0" font-size="12" text-anchor="start">x + y = 10</text><text class="ink" x="330.0" y="134.0" font-size="12" text-anchor="end">x − y = 4</text><circle class="dot3" cx="250.0" cy="220.0" r="6"/><text class="ink" x="260.0" y="238.0" font-size="12" text-anchor="start">intersection (7, 3)</text><text class="dim" x="200" y="446.0" font-size="11" text-anchor="middle">the only point satisfying both equations</text></svg>
  <figcaption>The lines $x + y = 10$ (purple) and $x - y = 4$ (orange) cross at $(7, 3)$. Every point on the purple line satisfies the first equation and every point on the orange line the second; the only point on both is the crossing.</figcaption>
</figure>

The graphical method is good for understanding the idea, but when the
crossing is not at whole numbers it is hard to read. For an exact result
there are two algebraic routes.

## Substitution

Get one unknown on its own in one equation and substitute it into the
other. An equation in one unknown remains.

$$
\begin{cases}
y = 2x - 1 \\
3x + y = 14
\end{cases}
$$

The first equation already gives $y$. In the second, write $2x - 1$ in
place of $y$:

$$
\begin{aligned}
3x + (2x - 1) &= 14 \\
5x &= 15 \\
x &= 3
\end{aligned}
$$

Then $y = 2 \cdot 3 - 1 = 5$. The solution is $(3, 5)$.

**Check:** in both equations: $5 = 6 - 1$ ✓, $9 + 5 = 14$ ✓.

## Elimination

Add or subtract the equations to eliminate one unknown. If the
coefficients are opposites, just add:

$$
\begin{aligned}
2x + 3y &= 12 \\
4x - 3y &= 6
\end{aligned}
$$

Add: $6x = 18$, $x = 3$. From the first equation $6 + 3y = 12$, $y = 2$.

**If the coefficients do not match, multiply first.** Multiplying an
equation by a number does not change its solutions.

$$
\begin{aligned}
3x + 2y &= 16 &&\text{(} \times 2\text{)} \\
2x + 5y &= 18 &&\text{(} \times 3\text{)}
\end{aligned}
$$

$$
\begin{aligned}
6x + 4y &= 32 \\
6x + 15y &= 54
\end{aligned}
$$

Subtract the first from the second: $11y = 22$, $y = 2$. Then $3x + 4 =
16$, $x = 4$. The solution is $(4, 2)$.

**Which to choose?** If an unknown is already on its own or has
coefficient $1$, substitute; if the coefficients are easy to match,
eliminate. Both give the same result.

## How many solutions can there be?

<figure class="fig">
<svg viewBox="0 0 500 213.66666666666666" width="500"><line class="line" x1="20.0" y1="138.3" x2="150.0" y2="138.3"/><line class="line" x1="41.7" y1="181.7" x2="41.7" y2="30.0"/><line class="curve" x1="20.0" y1="127.5" x2="150.0" y2="62.5"/><line class="curve2" x1="20.0" y1="30.0" x2="150.0" y2="160.0"/><circle class="dot3" cx="85.0" cy="95.0" r="5"/><text class="ink" x="85" y="18" font-size="13" text-anchor="middle">one solution</text><text class="dim" x="85" y="201.66666666666666" font-size="11" text-anchor="middle">the lines cross</text><line class="line" x1="180.0" y1="138.3" x2="310.0" y2="138.3"/><line class="line" x1="201.7" y1="181.7" x2="201.7" y2="30.0"/><line class="curve" x1="180.0" y1="108.0" x2="310.0" y2="30.0"/><line class="curve2" x1="180.0" y1="173.0" x2="310.0" y2="95.0"/><text class="ink" x="245" y="18" font-size="13" text-anchor="middle">no solution</text><text class="dim" x="245" y="201.66666666666666" font-size="11" text-anchor="middle">parallel lines</text><line class="line" x1="340.0" y1="138.3" x2="470.0" y2="138.3"/><line class="line" x1="361.7" y1="181.7" x2="361.7" y2="30.0"/><line class="curve" x1="340.0" y1="62.5" x2="470.0" y2="127.5"/><line class="curve2" stroke-dasharray="7 5" x1="340.0" y1="62.5" x2="470.0" y2="127.5"/><text class="ink" x="405" y="18" font-size="13" text-anchor="middle">infinitely many</text><text class="dim" x="405" y="201.66666666666666" font-size="11" text-anchor="middle">the same line</text></svg>
  <figcaption>Two lines either cross at one point (one solution), or are parallel and never meet (no solution), or are the same line with every point shared (infinitely many solutions).</figcaption>
</figure>

In algebra these cases show up during elimination:

| After eliminating | Meaning | Example |
|---|---|---|
| a value such as $x = 3$ | one solution | the examples above |
| something false like $0 = 7$ | no solution (parallel) | $x + y = 2$ and $x + y = 9$ |
| $0 = 0$ | infinitely many (same line) | $x + y = 2$ and $2x + 2y = 4$ |

## Turning word problems into systems

Two unknowns, two pieces of information: each piece is an equation.

**Example:** $120$ tickets were sold for a concert; a full ticket costs
$50$ and a student ticket $30$; the total takings were $5\,000$. How many
full tickets were sold?

$t$ = full, $s$ = student.

$$
\begin{cases}
t + s = 120 \\
50t + 30s = 5\,000
\end{cases}
$$

From the first, $s = 120 - t$; substitute into the second: $50t + 3\,600 -
30t = 5\,000$, $20t = 1\,400$, $t = 70$, $s = 50$.

## Systems of equations in machine learning

**A line through two points.** Let the model $\hat{y} = wx + b$ pass
through $(1, 5)$ and $(3, 11)$:

$$
\begin{cases}
w + b = 5 \\
3w + b = 11
\end{cases}
$$

Subtract: $2w = 6$, $w = 3$, $b = 2$. The model is $\hat{y} = 3x + 2$.

**Many data points, few unknowns.** Real data has hundreds of points but a
line has only two parameters. There is usually no line through all the
points: the system has no exact solution. Linear regression instead looks
for the $w$ and $b$ that make the error as small as possible; that too
comes down to solving a system in two unknowns. Systems with many unknowns
come in Advanced Mathematics (Gaussian elimination).

## Common mistakes

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Wrong</h4>
      <p>Finding only $x$ and stopping</p>
      <p>Changing the sign of one term when subtracting</p>
      <p>Putting $y$ back into the equation it came from</p>
      <p>Checking in one equation only</p>
    </div>
    <div class="ok">
      <h4>Right</h4>
      <p>The solution is a pair: $(x, y)$</p>
      <p>Subtract the whole equation: every sign changes</p>
      <p>Put $y$ into the <b>other</b> equation</p>
      <p>Check in both equations</p>
    </div>
  </div>
  <figcaption>A solution of a system must satisfy both equations; check in both.</figcaption>
</figure>

- **Substituting into the same equation.** Putting $y = 2x - 1$ into itself
  gives $2x - 1 = 2x - 1$: no information.
- **Skipping a term when multiplying.** When multiplying an equation,
  every term is multiplied, **the right-hand side included**.

## Summary

- A system of equations: several equations holding at once; a solution is a pair $(x, y)$.
- On a graph, the solution is where two lines cross.
- Substitution: get one unknown alone, put it into the other equation.
- Elimination: match coefficients, add or subtract; one unknown disappears.
- One solution (crossing), no solution (parallel, $0 = 7$), infinitely many (same line, $0 = 0$).
- In a word problem each piece of information is an equation; two unknowns need two independent pieces.
- Finding the line through two points is a system in two unknowns.
