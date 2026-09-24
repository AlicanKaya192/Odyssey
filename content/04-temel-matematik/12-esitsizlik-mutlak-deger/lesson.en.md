# Inequalities and Absolute Value

An equation asks for a single value: "for which $x$ are they equal?" An
**inequality** asks for a range: "for which $x$s is it smaller?" Most
limits in daily life are like this: a speed limit, a budget, an age range.
In machine learning, thresholds ("say yes if the probability is above
$0.5$"), error tolerances ("the error is at most $0.1$") and clipping are
all written with inequalities. In this section we will solve inequalities,
show their solutions on the number line and write "distance" conditions
with absolute value.

Prerequisite: Integers (absolute value), Linear Equations.

## Inequality signs

| Sign | Read as | Example |
|---|---|---|
| $<$ | less than | $2 < 5$ |
| $>$ | greater than | $-1 > -4$ |
| $\le$ | less than or equal to | $x \le 3$: $3$ is included |
| $\ge$ | greater than or equal to | $x \ge 0$: the non-negative numbers |

The solution of an inequality is usually not one number but a **range**:
**every** number greater than $2$ satisfies $x > 2$.

<figure class="fig">
<svg viewBox="0 0 500 160" width="500"><text class="ink" x="247.0" y="22" font-size="12" text-anchor="middle">x > 2: 2 not included (open circle)</text><line class="line" x1="18" y1="44" x2="476" y2="44"/><line class="line" x1="26" y1="39" x2="26" y2="49"/><text class="dim" x="26" y="64" font-size="10" text-anchor="middle">−6</text><line class="line" x1="60" y1="39" x2="60" y2="49"/><text class="dim" x="60" y="64" font-size="10" text-anchor="middle">−5</text><line class="line" x1="94" y1="39" x2="94" y2="49"/><text class="dim" x="94" y="64" font-size="10" text-anchor="middle">−4</text><line class="line" x1="128" y1="39" x2="128" y2="49"/><text class="dim" x="128" y="64" font-size="10" text-anchor="middle">−3</text><line class="line" x1="162" y1="39" x2="162" y2="49"/><text class="dim" x="162" y="64" font-size="10" text-anchor="middle">−2</text><line class="line" x1="196" y1="39" x2="196" y2="49"/><text class="dim" x="196" y="64" font-size="10" text-anchor="middle">−1</text><line class="line" x1="230" y1="39" x2="230" y2="49"/><text class="ink" x="230" y="64" font-size="10" text-anchor="middle">0</text><line class="line" x1="264" y1="39" x2="264" y2="49"/><text class="dim" x="264" y="64" font-size="10" text-anchor="middle">1</text><line class="line" x1="298" y1="39" x2="298" y2="49"/><text class="dim" x="298" y="64" font-size="10" text-anchor="middle">2</text><line class="line" x1="332" y1="39" x2="332" y2="49"/><text class="dim" x="332" y="64" font-size="10" text-anchor="middle">3</text><line class="line" x1="366" y1="39" x2="366" y2="49"/><text class="dim" x="366" y="64" font-size="10" text-anchor="middle">4</text><line class="line" x1="400" y1="39" x2="400" y2="49"/><text class="dim" x="400" y="64" font-size="10" text-anchor="middle">5</text><line class="line" x1="434" y1="39" x2="434" y2="49"/><text class="dim" x="434" y="64" font-size="10" text-anchor="middle">6</text><line class="line" x1="468" y1="39" x2="468" y2="49"/><text class="dim" x="468" y="64" font-size="10" text-anchor="middle">7</text><line class="curve" x1="298" y1="44" x2="474.8" y2="44" style="stroke-width:5"/><polygon class="dot" points="484,44 472,37 472,51"/><circle class="box" cx="298" cy="44" r="6" style="stroke-width:2.5"/><circle class="curve" cx="298" cy="44" r="6" style="stroke-width:2.5"/><text class="ink" x="247.0" y="106" font-size="12" text-anchor="middle">−1 ≤ x < 3: −1 included (filled), 3 not (open)</text><line class="line" x1="18" y1="128" x2="476" y2="128"/><line class="line" x1="26" y1="123" x2="26" y2="133"/><text class="dim" x="26" y="148" font-size="10" text-anchor="middle">−6</text><line class="line" x1="60" y1="123" x2="60" y2="133"/><text class="dim" x="60" y="148" font-size="10" text-anchor="middle">−5</text><line class="line" x1="94" y1="123" x2="94" y2="133"/><text class="dim" x="94" y="148" font-size="10" text-anchor="middle">−4</text><line class="line" x1="128" y1="123" x2="128" y2="133"/><text class="dim" x="128" y="148" font-size="10" text-anchor="middle">−3</text><line class="line" x1="162" y1="123" x2="162" y2="133"/><text class="dim" x="162" y="148" font-size="10" text-anchor="middle">−2</text><line class="line" x1="196" y1="123" x2="196" y2="133"/><text class="dim" x="196" y="148" font-size="10" text-anchor="middle">−1</text><line class="line" x1="230" y1="123" x2="230" y2="133"/><text class="ink" x="230" y="148" font-size="10" text-anchor="middle">0</text><line class="line" x1="264" y1="123" x2="264" y2="133"/><text class="dim" x="264" y="148" font-size="10" text-anchor="middle">1</text><line class="line" x1="298" y1="123" x2="298" y2="133"/><text class="dim" x="298" y="148" font-size="10" text-anchor="middle">2</text><line class="line" x1="332" y1="123" x2="332" y2="133"/><text class="dim" x="332" y="148" font-size="10" text-anchor="middle">3</text><line class="line" x1="366" y1="123" x2="366" y2="133"/><text class="dim" x="366" y="148" font-size="10" text-anchor="middle">4</text><line class="line" x1="400" y1="123" x2="400" y2="133"/><text class="dim" x="400" y="148" font-size="10" text-anchor="middle">5</text><line class="line" x1="434" y1="123" x2="434" y2="133"/><text class="dim" x="434" y="148" font-size="10" text-anchor="middle">6</text><line class="line" x1="468" y1="123" x2="468" y2="133"/><text class="dim" x="468" y="148" font-size="10" text-anchor="middle">7</text><line class="curve" x1="196" y1="128" x2="332" y2="128" style="stroke-width:5"/><circle class="dot" cx="196" cy="128" r="6"/><circle class="box" cx="332" cy="128" r="6" style="stroke-width:2.5"/><circle class="curve" cx="332" cy="128" r="6" style="stroke-width:2.5"/></svg>
  <figcaption>The solution set on the number line: an open circle means the number is not included ($<$, $>$), a filled circle means it is ($\le$, $\ge$). Top: every number greater than $2$. Bottom: from $-1$ to $3$, including $-1$ but not $3$.</figcaption>
</figure>

**Interval notation:** a square bracket means included, a round one means
excluded.

| Inequality | Interval |
|---|---|
| $x > 2$ | $(2, \infty)$ |
| $x \le 3$ | $(-\infty, 3]$ |
| $-1 \le x < 3$ | $[-1, 3)$ |

Infinity is never "included"; it always has a round bracket.

## Solving inequalities

The equation rules hold, **with one difference**: if you multiply or
divide both sides by a **negative** number, the inequality **flips**.

Why? $2 < 5$ is true. Multiply both sides by $-1$: $-2$ and $-5$. But $-2 >
-5$; going negative reverses the order on the number line.

$$
\begin{aligned}
-3x + 5 &\ge 14 \\
-3x &\ge 9 &&\text{(subtract } 5 \text{ from both sides)} \\
x &\le -3 &&\text{(divide by } -3\text{, it flips)}
\end{aligned}
$$

**Check:** try a value at the boundary and one inside. $x = -3$: $9 + 5 =
14 \ge 14$ ✓. $x = -4$: $12 + 5 = 17 \ge 14$ ✓. From outside, $x = 0$: $5
\ge 14$ is false ✓.

**You can also avoid flipping:** collect the unknown on the side where its
coefficient stays positive. $-3x + 5 \ge 14 \Rightarrow 5 - 14 \ge 3x
\Rightarrow -9 \ge 3x \Rightarrow -3 \ge x$. The same result.

### Double inequalities

In an inequality such as $-1 \le 2x + 3 < 9$, the same operation is done
to all three parts:

$$
\begin{aligned}
-1 &\le 2x + 3 < 9 \\
-4 &\le 2x < 6 &&\text{(subtract } 3 \text{ from all three)} \\
-2 &\le x < 3 &&\text{(divide all three by } 2\text{)}
\end{aligned}
$$

## Absolute value: distance

From the Integers section: $|a|$ is the distance of $a$ from zero; $|a -
b|$ is the distance between $a$ and $b$. Reading absolute value as
"distance" is the key to solving equations and inequalities with it.

**An absolute-value equation.** $|x| = 3$: the numbers at distance $3$ from
zero, $x = 3$ or $x = -3$. In general

$$
|A| = r \quad (r \ge 0) \quad\Longleftrightarrow\quad A = r \text{ or } A = -r
$$

$|x - 2| = 5$: $x - 2 = 5$ or $x - 2 = -5$, so $x = 7$ or $x = -3$. On the
number line, $5$ units right and left of $2$.

If $r$ is negative (as in $|x| = -1$) there is no solution: a distance
cannot be negative.

## Absolute-value inequalities

<figure class="fig">
<svg viewBox="0 0 500 152" width="500"><text class="ink" x="247.0" y="20" font-size="12" text-anchor="middle">|x − 2| ≤ 3: numbers at most 3 away from 2</text><line class="line" x1="18" y1="86" x2="476" y2="86"/><line class="line" x1="26" y1="81" x2="26" y2="91"/><text class="dim" x="26" y="106" font-size="10" text-anchor="middle">−6</text><line class="line" x1="60" y1="81" x2="60" y2="91"/><text class="dim" x="60" y="106" font-size="10" text-anchor="middle">−5</text><line class="line" x1="94" y1="81" x2="94" y2="91"/><text class="dim" x="94" y="106" font-size="10" text-anchor="middle">−4</text><line class="line" x1="128" y1="81" x2="128" y2="91"/><text class="dim" x="128" y="106" font-size="10" text-anchor="middle">−3</text><line class="line" x1="162" y1="81" x2="162" y2="91"/><text class="dim" x="162" y="106" font-size="10" text-anchor="middle">−2</text><line class="line" x1="196" y1="81" x2="196" y2="91"/><text class="dim" x="196" y="106" font-size="10" text-anchor="middle">−1</text><line class="line" x1="230" y1="81" x2="230" y2="91"/><text class="ink" x="230" y="106" font-size="10" text-anchor="middle">0</text><line class="line" x1="264" y1="81" x2="264" y2="91"/><text class="dim" x="264" y="106" font-size="10" text-anchor="middle">1</text><line class="line" x1="298" y1="81" x2="298" y2="91"/><text class="dim" x="298" y="106" font-size="10" text-anchor="middle">2</text><line class="line" x1="332" y1="81" x2="332" y2="91"/><text class="dim" x="332" y="106" font-size="10" text-anchor="middle">3</text><line class="line" x1="366" y1="81" x2="366" y2="91"/><text class="dim" x="366" y="106" font-size="10" text-anchor="middle">4</text><line class="line" x1="400" y1="81" x2="400" y2="91"/><text class="dim" x="400" y="106" font-size="10" text-anchor="middle">5</text><line class="line" x1="434" y1="81" x2="434" y2="91"/><text class="dim" x="434" y="106" font-size="10" text-anchor="middle">6</text><line class="line" x1="468" y1="81" x2="468" y2="91"/><text class="dim" x="468" y="106" font-size="10" text-anchor="middle">7</text><line class="curve" x1="196" y1="86" x2="400" y2="86" style="stroke-width:5"/><circle class="dot" cx="196" cy="86" r="6"/><circle class="dot" cx="400" cy="86" r="6"/><circle class="dot2" cx="298" cy="86" r="5"/><line class="curve2" x1="298" y1="60" x2="204" y2="60"/><polygon class="dot2" points="196,60 205,55 205,65"/><text class="ink" x="247.0" y="53" font-size="12" text-anchor="middle">3</text><line class="curve2" x1="298" y1="60" x2="392" y2="60"/><polygon class="dot2" points="400,60 391,55 391,65"/><text class="ink" x="349.0" y="53" font-size="12" text-anchor="middle">3</text><line class="curve3" stroke-dasharray="3 3" x1="298" y1="52" x2="298" y2="86"/><text class="dim" x="298" y="122" font-size="11" text-anchor="middle">centre 2</text><text class="ink" x="298" y="140" font-size="13" text-anchor="middle">−1 ≤ x ≤ 5</text></svg>
  <figcaption>$|x - 2| \le 3$ says that the distance from $x$ to $2$ is at most $3$: a region of $3$ units on each side of $2$. Centre $2$, radius $3$; the solution is $-1 \le x \le 5$.</figcaption>
</figure>

| Condition | Meaning | Solution |
|---|---|---|
| $\lvert x - a \rvert \le r$ | distance from $a$ at most $r$ | $a - r \le x \le a + r$ |
| $\lvert x - a \rvert \ge r$ | distance from $a$ at least $r$ | $x \le a - r$ or $x \ge a + r$ |

"Less than" gives **one interval** (inside), "greater than" gives **two
separate pieces** (outside).

**Example:** $|2x - 1| \le 5$.

$$
\begin{aligned}
-5 &\le 2x - 1 \le 5 \\
-4 &\le 2x \le 6 \\
-2 &\le x \le 3
\end{aligned}
$$

**Example:** $|x + 1| > 4$. $x + 1 > 4$ or $x + 1 < -4$: $x > 3$ or $x < -5$.

## Inequalities in machine learning

**Threshold.** A classifier says "yes" when the probability $p \ge 0.5$.
Raising the threshold to $0.8$ means a more cautious model: it has to be
more certain before saying "yes".

**Tolerance.** The condition "the prediction is within $0.5$ of the truth"
is written $|\hat{y} - y| \le 0.5$. If the true value is $12$, the accepted
predictions are $11.5 \le \hat{y} \le 12.5$.

**Clipping.** To prevent very large steps in training, a value is clipped
to the interval $[-1, 1]$: below $-1$ it becomes $-1$, above $1$ it becomes
$1$. This forces the value to satisfy $|g| \le 1$.

## Common mistakes

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Wrong</h4>
      <p>$-2x < 6 \Rightarrow x < -3$</p>
      <p>$|x| < 3 \Rightarrow x < 3$</p>
      <p>$|x - 2| \ge 3 \Rightarrow -1 \ge x \ge 5$</p>
      <p>$x > 2$: a filled circle at $2$</p>
    </div>
    <div class="ok">
      <h4>Right</h4>
      <p>$-2x < 6 \Rightarrow x > -3$ (it flips)</p>
      <p>$|x| < 3 \Rightarrow -3 < x < 3$</p>
      <p>$x \le -1$ or $x \ge 5$ (two pieces)</p>
      <p>$x > 2$: an open circle at $2$</p>
    </div>
  </div>
  <figcaption>Multiplying or dividing by a negative flips the inequality; absolute value limits both sides at once.</figcaption>
</figure>

- **Forgetting to flip.** If you are unsure, try one number on each side of
  the boundary.
- **Squeezing an "or" into one inequality.** The set $x \le -1$ or $x \ge
  5$ cannot be written $-1 \ge x \ge 5$; no number is like that.
- **Thinking an absolute value can be negative.** $|x - 3| < -2$ has no
  solution.

## Summary

- The solution of an inequality is a range; on the number line an open circle excludes, a filled one includes.
- Interval notation: $[\ ]$ included, $(\ )$ excluded; $\infty$ always with $($.
- The equation rules hold; multiplying or dividing by a negative flips the inequality.
- In a double inequality, do the same to all three parts.
- $|A| = r$: $A = r$ or $A = -r$ ($r \ge 0$).
- $|x - a| \le r$: $a - r \le x \le a + r$ (inside); $|x - a| \ge r$: $x \le a - r$ or $x \ge a + r$ (outside).
- Thresholds, tolerances and clipping are written with inequalities.
