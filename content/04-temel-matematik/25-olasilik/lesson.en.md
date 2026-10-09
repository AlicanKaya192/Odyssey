# Introduction to Probability

Probability is the way to talk about uncertainty with numbers. Sentences
such as "a $70$ percent chance of rain tomorrow" or "this e-mail is spam
with probability $95$ percent" appear in daily life and in machine learning
alike. A classifier often does not say "this is a cat"; it says "this is a
cat with probability $92$ percent". In this section we will see the sample
space and events, the two interpretations of probability, the complement,
union and intersection rules, independence, probability trees and a first
look at conditional probability. The probability and statistics part of
the Advanced Mathematics module is built on this foundation.

Prerequisites: Fractions, Sets and Logic, Counting: Permutations and
Combinations.

## Experiment, sample space, event

- **Experiment:** a process whose result is not known for certain in
  advance; rolling a die, drawing a card, whether a customer will buy.
- **Sample space** $S$: the set of all possible outcomes. For a die
  $S = \{1, 2, 3, 4, 5, 6\}$.
- **Event:** a subset of the sample space. The event "an even number" is
  $A = \{2, 4, 6\}$.

Since events are sets, the operations of Sets and Logic apply as they are:
$A \cup B$ is "$A$ or $B$", $A \cap B$ "$A$ and $B$", $A'$ "not $A$".

## What is probability?

**The classical definition.** If all outcomes are equally likely:

$$
P(A) = \frac{n(A)}{n(S)} = \frac{\text{number of outcomes in the event}}{\text{number of all outcomes}}
$$

The probability of an even number on a die is $\frac{3}{6} = \frac{1}{2}$.
The tools of Counting are used to count the outcomes.

**The frequency interpretation.** If the experiment is repeated many times,
the share of times the event happens approaches its probability. This is
the observable meaning of the sentence "the probability is $0.5$".

<figure class="fig">
<svg viewBox="0 0 440 234" width="440"><line class="grid" x1="50.0" y1="220.0" x2="50.0" y2="20.0"/><line class="grid" x1="122.0" y1="220.0" x2="122.0" y2="20.0"/><line class="grid" x1="194.0" y1="220.0" x2="194.0" y2="20.0"/><line class="grid" x1="266.0" y1="220.0" x2="266.0" y2="20.0"/><line class="grid" x1="338.0" y1="220.0" x2="338.0" y2="20.0"/><line class="grid" x1="410.0" y1="220.0" x2="410.0" y2="20.0"/><line class="grid" x1="50.0" y1="220.0" x2="410.0" y2="220.0"/><line class="grid" x1="50.0" y1="170.0" x2="410.0" y2="170.0"/><line class="grid" x1="50.0" y1="120.0" x2="410.0" y2="120.0"/><line class="grid" x1="50.0" y1="70.0" x2="410.0" y2="70.0"/><line class="grid" x1="50.0" y1="20.0" x2="410.0" y2="20.0"/><line class="line" x1="50.0" y1="220.0" x2="410.0" y2="220.0"/><line class="line" x1="50.0" y1="220.0" x2="50.0" y2="20.0"/><text class="dim" x="122.0" y="233.0" font-size="9" text-anchor="middle">100</text><text class="dim" x="194.0" y="233.0" font-size="9" text-anchor="middle">200</text><text class="dim" x="266.0" y="233.0" font-size="9" text-anchor="middle">300</text><text class="dim" x="338.0" y="233.0" font-size="9" text-anchor="middle">400</text><text class="dim" x="410.0" y="233.0" font-size="9" text-anchor="middle">500</text><text class="dim" x="45.0" y="173.0" font-size="9" text-anchor="end">0.25</text><text class="dim" x="45.0" y="123.0" font-size="9" text-anchor="end">0.5</text><text class="dim" x="45.0" y="73.0" font-size="9" text-anchor="end">0.75</text><text class="dim" x="45.0" y="23.0" font-size="9" text-anchor="end">1</text><line class="curve2" stroke-dasharray="5 4" x1="50.0" y1="120.0" x2="410.0" y2="120.0"/><polyline class="curve" fill="none" points="50.7,20.0 51.4,120.0 52.2,86.7 52.9,120.0 53.6,140.0 54.3,120.0 55.0,105.7 55.8,120.0 56.5,108.9 57.2,100.0 57.9,110.9 58.6,103.3 59.4,112.3 60.1,105.7 60.8,113.3 61.5,107.5 62.2,114.1 63.0,120.0 63.7,125.3 64.4,130.0 65.1,134.3 65.8,129.1 66.6,133.0 67.3,136.7 68.0,132.0 68.7,127.7 69.4,131.1 70.2,127.1 70.9,130.3 71.6,133.3 72.3,136.1 73.0,138.8 73.8,135.2 74.5,137.6 75.2,134.3 75.9,136.7 76.6,138.9 77.4,135.8 78.1,132.8 78.8,130.0 79.5,132.2 80.2,129.5 81.0,131.6 81.7,129.1 82.4,131.1 83.1,128.7 83.8,126.4 84.6,128.3 85.3,130.2 86.0,132.0 86.7,133.7 87.4,135.4 88.2,137.0 88.9,138.5 89.6,140.0 90.3,137.9 91.0,139.3 91.8,140.7 92.5,142.0 93.2,143.3 93.9,144.6 94.6,142.6 95.4,143.8 96.1,145.0 96.8,143.1 97.5,141.2 98.2,142.4 99.0,143.5 99.7,141.7 100.4,142.9 101.1,141.1 101.8,139.4 102.6,137.8 103.3,138.9 104.0,140.0 104.7,138.4 105.4,139.5 106.2,137.9 106.9,139.0 107.6,137.5 108.3,138.5 109.0,139.5 109.8,140.5 110.5,141.4 111.2,140.0 111.9,138.6 112.6,139.5 113.4,138.2 114.1,136.9 114.8,135.6 115.5,136.5 116.2,135.2 117.0,134.0 117.7,134.9 118.4,133.7 119.1,134.6 119.8,135.5 120.6,134.3 121.3,133.1 122.0,134.0 122.7,134.9 123.4,135.7 124.2,136.5 124.9,137.3 125.6,138.1 126.3,138.9 127.0,137.8 127.8,138.5 128.5,137.4 129.2,136.4 129.9,137.1 130.6,137.9 131.4,138.6 132.1,137.5 132.8,136.5 133.5,137.2 134.2,136.2 135.0,136.9 135.7,137.6 136.4,136.7 137.1,137.4 137.8,136.4 138.6,137.1 139.3,136.1 140.0,136.8 140.7,137.5 141.4,136.5 142.2,135.6 142.9,136.3 143.6,136.9 144.3,136.0 145.0,135.2 145.8,135.8 146.5,134.9 147.2,134.1 147.9,133.2 148.6,132.4 149.4,133.0 150.1,132.2 150.8,131.4 151.5,132.1 152.2,131.3 153.0,131.9 153.7,132.5 154.4,131.7 155.1,131.0 155.8,131.6 156.6,130.8 157.3,130.1 158.0,129.3 158.7,129.9 159.4,129.2 160.2,128.5 160.9,127.8 161.6,128.4 162.3,127.7 163.0,128.3 163.8,127.6 164.5,126.9 165.2,127.5 165.9,128.1 166.6,127.4 167.4,126.7 168.1,126.1 168.8,126.7 169.5,126.0 170.2,126.6 171.0,127.1 171.7,126.5 172.4,125.9 173.1,126.4 173.8,127.0 174.6,127.5 175.3,126.9 176.0,126.3 176.7,125.7 177.4,126.2 178.2,125.6 178.9,125.0 179.6,124.4 180.3,123.9 181.0,123.3 181.8,123.8 182.5,123.3 183.2,122.7 183.9,123.2 184.6,123.7 185.4,124.3 186.1,123.7 186.8,124.2 187.5,124.7 188.2,124.2 189.0,124.7 189.7,125.2 190.4,125.6 191.1,126.1 191.8,125.6 192.6,125.1 193.3,124.5 194.0,124.0 194.7,124.5 195.4,124.0 196.2,124.4 196.9,123.9 197.6,124.4 198.3,124.9 199.0,125.3 199.8,125.8 200.5,126.2 201.2,126.7 201.9,126.2 202.6,126.6 203.4,126.1 204.1,125.6 204.8,126.0 205.5,126.5 206.2,126.0 207.0,126.4 207.7,126.8 208.4,126.4 209.1,125.9 209.8,126.3 210.6,125.8 211.3,126.2 212.0,125.8 212.7,125.3 213.4,125.7 214.2,126.1 214.9,125.7 215.6,126.1 216.3,126.5 217.0,126.9 217.8,127.3 218.5,126.8 219.2,127.2 219.9,127.6 220.6,127.2 221.4,126.7 222.1,126.3 222.8,126.7 223.5,126.2 224.2,125.8 225.0,126.2 225.7,125.7 226.4,125.3 227.1,124.9 227.8,124.5 228.6,124.0 229.3,124.4 230.0,124.8 230.7,124.4 231.4,124.8 232.2,124.3 232.9,123.9 233.6,123.5 234.3,123.9 235.0,124.3 235.8,123.9 236.5,123.5 237.2,123.1 237.9,122.7 238.6,123.1 239.4,123.4 240.1,123.0 240.8,122.6 241.5,122.3 242.2,121.9 243.0,122.2 243.7,122.6 244.4,122.2 245.1,122.6 245.8,122.9 246.6,122.6 247.3,122.2 248.0,121.8 248.7,122.2 249.4,121.8 250.2,122.2 250.9,121.8 251.6,121.4 252.3,121.8 253.0,122.1 253.8,121.8 254.5,121.4 255.2,121.1 255.9,121.4 256.6,121.7 257.4,121.4 258.1,121.7 258.8,122.1 259.5,121.7 260.2,121.4 261.0,121.0 261.7,121.4 262.4,121.7 263.1,122.0 263.8,122.4 264.6,122.7 265.3,123.0 266.0,123.3 266.7,123.0 267.4,123.3 268.2,123.0 268.9,122.6 269.6,123.0 270.3,122.6 271.0,122.3 271.8,121.9 272.5,122.3 273.2,121.9 273.9,121.6 274.6,121.9 275.4,121.6 276.1,121.9 276.8,122.2 277.5,122.5 278.2,122.8 279.0,123.1 279.7,123.4 280.4,123.1 281.1,123.4 281.8,123.7 282.6,124.0 283.3,123.7 284.0,124.0 284.7,124.3 285.4,124.0 286.2,123.7 286.9,124.0 287.6,124.2 288.3,123.9 289.0,123.6 289.8,123.3 290.5,123.6 291.2,123.9 291.9,123.6 292.6,123.3 293.4,123.0 294.1,122.7 294.8,122.4 295.5,122.1 296.2,122.3 297.0,122.6 297.7,122.3 298.4,122.6 299.1,122.3 299.8,122.6 300.6,122.9 301.3,123.2 302.0,123.4 302.7,123.1 303.4,123.4 304.2,123.7 304.9,123.4 305.6,123.1 306.3,123.4 307.0,123.6 307.8,123.9 308.5,123.6 309.2,123.9 309.9,123.6 310.6,123.3 311.4,123.0 312.1,123.3 312.8,123.0 313.5,122.7 314.2,123.0 315.0,123.3 315.7,123.0 316.4,123.2 317.1,123.0 317.8,123.2 318.6,123.5 319.3,123.2 320.0,122.9 320.7,122.7 321.4,122.4 322.2,122.1 322.9,121.8 323.6,121.6 324.3,121.3 325.0,121.6 325.8,121.3 326.5,121.6 327.2,121.3 327.9,121.6 328.6,121.3 329.4,121.5 330.1,121.8 330.8,122.1 331.5,121.8 332.2,122.0 333.0,122.3 333.7,122.0 334.4,122.3 335.1,122.5 335.8,122.3 336.6,122.0 337.3,121.8 338.0,122.0 338.7,122.2 339.4,122.5 340.2,122.7 340.9,122.5 341.6,122.2 342.3,122.0 343.0,121.7 343.8,122.0 344.5,122.2 345.2,122.4 345.9,122.2 346.6,122.4 347.4,122.2 348.1,121.9 348.8,122.2 349.5,121.9 350.2,121.7 351.0,121.9 351.7,121.7 352.4,121.4 353.1,121.7 353.8,121.9 354.6,121.7 355.3,121.4 356.0,121.2 356.7,120.9 357.4,120.7 358.2,120.9 358.9,121.2 359.6,120.9 360.3,121.2 361.0,120.9 361.8,120.7 362.5,120.9 363.2,120.7 363.9,120.9 364.6,121.1 365.4,120.9 366.1,121.1 366.8,120.9 367.5,121.1 368.2,121.4 369.0,121.1 369.7,121.4 370.4,121.6 371.1,121.8 371.8,121.6 372.6,121.8 373.3,122.0 374.0,122.2 374.7,122.4 375.4,122.2 376.2,122.0 376.9,121.8 377.6,122.0 378.3,122.2 379.0,122.4 379.8,122.2 380.5,122.4 381.2,122.6 381.9,122.4 382.6,122.6 383.4,122.8 384.1,122.6 384.8,122.8 385.5,122.6 386.2,122.4 387.0,122.6 387.7,122.8 388.4,123.0 389.1,123.2 389.8,123.0 390.6,122.7 391.3,122.5 392.0,122.3 392.7,122.5 393.4,122.7 394.2,122.9 394.9,123.1 395.6,122.9 396.3,122.7 397.0,122.5 397.8,122.7 398.5,122.5 399.2,122.7 399.9,122.5 400.6,122.7 401.4,122.5 402.1,122.2 402.8,122.0 403.5,122.2 404.2,122.4 405.0,122.2 405.7,122.4 406.4,122.2 407.1,122.0 407.8,121.8 408.6,121.6 409.3,121.8 410.0,122.0"/><text class="ink" x="410.0" y="112.0" font-size="11" text-anchor="end">true probability 0.5</text><text class="dim" x="410.0" y="214.0" font-size="10" text-anchor="end">number of flips</text><text class="dim" x="56.0" y="30.0" font-size="10" text-anchor="start">share of heads</text></svg>
  <figcaption>A coin was tossed 500 times on a computer. The share of heads is 0.6 after 10 tosses, 0.43 after 100 and 0.49 after 500. With few tosses the share jumps around; with more it settles around 0.5.</figcaption>
</figure>

This is called the **law of large numbers**: as the number of repetitions
grows, the observed share approaches the true probability. This is also
what test accuracy means in machine learning; as the test set grows, the
measured accuracy approaches the model's true success rate.

**Basic rules.** For every event $0 \leq P(A) \leq 1$. An impossible event
has probability $0$ and the certain event ($S$) probability $1$. The
probabilities of all the outcomes add up to $1$.

## The complement

The event "not $A$", $A'$, is the **complement** of $A$. One of the two
certainly happens and they never happen together:

$$
P(A') = 1 - P(A)
$$

The complement greatly shortens "at least one" questions. A coin is tossed
three times; what is the probability of at least one head? The opposite is
"no heads", that is three tails: $\left( \frac{1}{2} \right)^3 =
\frac{1}{8}$. The answer is $1 - \frac{1}{8} = \frac{7}{8}$.

**The birthday question.** In a class of $23$, what is the probability that
at least two people share a birthday? The complement is "all different":
$\frac{365}{365} \cdot \frac{364}{365} \cdots \frac{343}{365} \approx 0.493$.
The answer is $1 - 0.493 \approx 0.507$; far larger than intuition says.

## Union and intersection

For "$A$ or $B$", adding the two probabilities is not enough; the outcomes
in both are counted twice:

$$
P(A \cup B) = P(A) + P(B) - P(A \cap B)
$$

<figure class="fig">
<svg viewBox="0 0 440 258" width="440"><rect class="box" x="20" y="20" width="400" height="200" rx="10"/><circle class="dot" opacity="0.28" cx="170" cy="120" r="78"/><circle class="dot2" opacity="0.28" cx="270" cy="120" r="78"/><text class="ink" x="125" y="125" font-size="16" text-anchor="middle">2</text><text class="ink" x="220" y="105" font-size="16" text-anchor="middle">4</text><text class="ink" x="220" y="145" font-size="16" text-anchor="middle">6</text><text class="ink" x="315" y="125" font-size="16" text-anchor="middle">5</text><text class="ink" x="60" y="175" font-size="16" text-anchor="middle">1</text><text class="ink" x="385" y="175" font-size="16" text-anchor="middle">3</text><text class="ink" x="120" y="46" font-size="12" text-anchor="middle">A: even</text><text class="ink" x="320" y="46" font-size="12" text-anchor="middle">B: 4 or more</text><text class="dim" x="30" y="210" font-size="10" text-anchor="start">S: all outcomes</text><text class="ink" x="220" y="246" font-size="12" text-anchor="middle">P(A ∪ B) = 3/6 + 3/6 − 2/6 = 4/6</text></svg>
  <figcaption>A die is rolled. A is the even numbers, B is 4 or more. 4 and 6 are in both sets; when adding they are counted twice, so they are subtracted once. The result is 4/6: {2, 4, 5, 6}.</figcaption>
</figure>

**Disjoint events.** Events that cannot happen at the same time are called
**disjoint**: $A \cap B = \varnothing$. Then $P(A \cup B) = P(A) + P(B)$.
On a die, "$1$" and "$6$" are disjoint: $\frac{1}{6} + \frac{1}{6} =
\frac{1}{3}$.

## Independent events

Two events are **independent** if one happening does not change the
probability of the other. Then the probability of both is the product:

$$
P(A \cap B) = P(A) \cdot P(B)
$$

A coin and a die: the probability of heads and a $6$ is
$\frac{1}{2} \cdot \frac{1}{6} = \frac{1}{12}$. The coin does not know what
the die will show.

**Do not confuse disjoint and independent.** Disjoint events are **not**
independent: when one happens the other becomes impossible, its probability
drops to $0$. On a die, "$1$" and "$6$" are disjoint, but knowing one fully
determines the other.

**The gambler's fallacy.** A coin came up heads five times; the probability
of tails on the sixth toss does not go up, it is still $\frac{1}{2}$. The
tosses are independent; the coin has no memory.

## Probability trees

For experiments that proceed step by step, the probability of each step is
written on its branch. The probability of a path is the **product** of the
probabilities along it; the probability of an event is the **sum** of the
paths that make it up.

A bag has $3$ red and $2$ blue balls; two balls are drawn **without
replacement**.

<figure class="fig">
<svg viewBox="0 0 470 262" width="470"><line class="curve3" x1="40" y1="140" x2="160" y2="75"/><line class="curve3" x1="40" y1="140" x2="160" y2="205"/><line class="curve3" x1="160" y1="75" x2="280" y2="40"/><line class="curve3" x1="160" y1="75" x2="280" y2="110"/><line class="curve3" x1="160" y1="205" x2="280" y2="170"/><line class="curve3" x1="160" y1="205" x2="280" y2="240"/><circle class="box" cx="40" cy="140" r="6"/><text class="dim" x="100.0" y="101.5" font-size="11" text-anchor="middle">3/5</text><circle class="box" cx="160" cy="75" r="13"/><text class="ink" x="160" y="79" font-size="11" text-anchor="middle">R</text><text class="dim" x="100.0" y="166.5" font-size="11" text-anchor="middle">2/5</text><circle class="box" cx="160" cy="205" r="13"/><text class="ink" x="160" y="209" font-size="11" text-anchor="middle">B</text><text class="dim" x="220.0" y="51.5" font-size="11" text-anchor="middle">2/4</text><circle class="box" cx="280" cy="40" r="13"/><text class="ink" x="280" y="44" font-size="11" text-anchor="middle">R</text><text class="dim" x="220.0" y="86.5" font-size="11" text-anchor="middle">2/4</text><circle class="box" cx="280" cy="110" r="13"/><text class="ink" x="280" y="114" font-size="11" text-anchor="middle">B</text><text class="dim" x="220.0" y="181.5" font-size="11" text-anchor="middle">3/4</text><circle class="box" cx="280" cy="170" r="13"/><text class="ink" x="280" y="174" font-size="11" text-anchor="middle">R</text><text class="dim" x="220.0" y="216.5" font-size="11" text-anchor="middle">1/4</text><circle class="box" cx="280" cy="240" r="13"/><text class="ink" x="280" y="244" font-size="11" text-anchor="middle">B</text><text class="ink" x="302" y="44" font-size="11" text-anchor="start">RR: 3/5 · 2/4 = 6/20</text><text class="ink" x="302" y="114" font-size="11" text-anchor="start">RB: 3/5 · 2/4 = 6/20</text><text class="ink" x="302" y="174" font-size="11" text-anchor="start">BR: 2/5 · 3/4 = 6/20</text><text class="ink" x="302" y="244" font-size="11" text-anchor="start">BB: 2/5 · 1/4 = 2/20</text><text class="dim" x="160" y="22" font-size="10" text-anchor="middle">1st draw</text><text class="dim" x="280" y="16" font-size="10" text-anchor="middle">2nd draw</text></svg>
  <figcaption>Red on the first draw is 3/5. If red was drawn, 2 red and 2 blue are left, and red on the second draw is 2/4. The four paths add up to 20/20 = 1.</figcaption>
</figure>

- Both red: $\frac{3}{5} \cdot \frac{2}{4} = \frac{6}{20} = \frac{3}{10}$.
  The same as $\frac{\binom{3}{2}}{\binom{5}{2}}$ from Counting.
- One of each: the RB and BR paths, $\frac{6}{20} + \frac{6}{20} =
  \frac{3}{5}$.

**With replacement** the second draw would not be affected by the first
(independent): both red $\frac{3}{5} \cdot \frac{3}{5} = \frac{9}{25}$.

## A first look at conditional probability

"The probability of $B$ given that $A$ happened" is written $P(B \mid A)$.
The information shrinks the sample space: now we only look inside $A$.

$$
P(B \mid A) = \frac{P(A \cap B)}{P(A)}
$$

The die came up even; what is the probability it is $4$ or more? The evens
are $\{2, 4, 6\}$, and those that are $4$ or more are $\{4, 6\}$:
$\frac{2}{3}$. With the formula $\frac{2/6}{3/6} = \frac{2}{3}$. The second
branches of the probability tree are conditional probabilities too: "if the
first ball is red, the second is red" is $\frac{2}{4}$.

**A two-way table.** Of $100$ e-mails, $30$ are spam. The word "winner"
appears in $24$ of the spam ones and in $7$ of the $70$ that are not spam.

| | "winner" present | absent | total |
|---|---|---|---|
| spam | $24$ | $6$ | $30$ |
| not spam | $7$ | $63$ | $70$ |
| total | $31$ | $69$ | $100$ |

- $P(\text{spam}) = 0.30$.
- $P(\text{word} \mid \text{spam}) = \frac{24}{30} = 0.80$: most spam
  contains the word.
- $P(\text{spam} \mid \text{word}) = \frac{24}{31} \approx 0.77$: this is
  the question a filter that sees the word asks.

The two conditional probabilities are different numbers; the way to get one
from the other is **Bayes' rule** in the Advanced Mathematics module.

## Probability in machine learning

**Models that give probabilities.** Logistic regression and neural networks
give class probabilities; "cat $0.92$, dog $0.08$" is a distribution that
adds up to $1$. The decision is made against a threshold.

**Accuracy is a probability.** $94$ percent accuracy on test data is an
estimate of the probability that a new example is classified correctly.
The frequency interpretation makes this estimate reliable as the test set
grows.

**The independence assumption.** A Naive Bayes classifier assumes that the
words in an e-mail are independent of each other (given the class) and
multiplies their probabilities. The assumption is not quite true, but the
method works surprisingly well.

**Randomness.** Shuffling the training data, initialising weights at random
and switching off each neuron with probability $p$ in dropout are all done
with probability.

## Common mistakes

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Wrong</h4>
      <p>$P(A \cup B) = P(A) + P(B)$ (always)</p>
      <p>disjoint events are independent</p>
      <p>after 5 heads, tails is more likely</p>
      <p>$P(B \mid A) = P(A \mid B)$</p>
    </div>
    <div class="ok">
      <h4>Right</h4>
      <p>subtract the overlap once</p>
      <p>disjoint events exclude each other; they are dependent</p>
      <p>the tosses are independent: still $\frac{1}{2}$</p>
      <p>$\frac{24}{31} \neq \frac{24}{30}$</p>
    </div>
  </div>
  <figcaption>The addition rule corrects for shared outcomes; independence means "not affecting each other", disjointness "not happening together".</figcaption>
</figure>

- **Treating unequally likely outcomes as equal.** The sum of two dice takes
  $11$ values from $2$ to $12$, but $7$ is six times as likely as $2$.
- **Forgetting about replacement.** Without replacement, the probabilities
  of the second draw change.

## Summary

- The sample space is all outcomes, an event is a subset; with equally
  likely outcomes $P(A) = \frac{n(A)}{n(S)}$.
- With many repetitions the observed share approaches the probability (law
  of large numbers).
- $P(A') = 1 - P(A)$; use the complement for "at least one".
- $P(A \cup B) = P(A) + P(B) - P(A \cap B)$; for disjoint events the
  intersection is $0$.
- If independent, $P(A \cap B) = P(A) P(B)$; disjoint events are not
  independent.
- In a tree, multiply along a path and add the paths.
- $P(B \mid A) = \frac{P(A \cap B)}{P(A)}$; $P(B \mid A)$ and $P(A \mid B)$
  are different.
