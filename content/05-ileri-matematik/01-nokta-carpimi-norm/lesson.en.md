# Dot Product, Length and Similarity

When a music app recommends a new song, when a search engine picks the page
most relevant to your query, or when a language model decides which words
in a sentence a word relates to, the same question is being asked: **how
similar are these two vectors?**

The mathematical answer to that question is the **dot product**. It is a
simple operation that takes two vectors and produces a single number; but
that number tells you how much the two vectors point the same way. In this
chapter we will look at the dot product, the angle between two vectors,
projection, cosine similarity and different measures of length (norms).

Prerequisites: the previous chapter (Vectors) and the **cosine**. The
cosine is covered in detail in the Trigonometry chapter of the Foundational Mathematics module; here I
will briefly recall the part we need.

## Definition: multiply and add

The **dot product** of two vectors is the sum of the products of their
matching components:

$$
\mathbf{a} \cdot \mathbf{b} = a_1 b_1 + a_2 b_2
$$

**Example:** for $\mathbf{a} = (3, 4)$ and $\mathbf{b} = (2, 1)$

$$
\mathbf{a} \cdot \mathbf{b} = 3 \cdot 2 + 4 \cdot 1 = 6 + 4 = 10
$$

The result is **not a vector but a single number** (a scalar). That is why
the dot product is also called the **scalar product**. Do not confuse
multiplying a vector by a scalar (previous chapter) with the dot product of
two vectors: the first gives a vector, the second a number.

Whatever the dimension, the definition is the same; all the products are
added:

$$
\mathbf{a} \cdot \mathbf{b} = \sum_{i=1}^{n} a_i b_i
\qquad
(1, 2, 3) \cdot (4, -5, 6) = 4 - 10 + 18 = 12
$$

The two vectors must have the **same dimension**; otherwise some components
have no partner.

### Properties

| Property | Written as |
|---|---|
| Commutative | $\mathbf{a} \cdot \mathbf{b} = \mathbf{b} \cdot \mathbf{a}$ |
| Distributive | $\mathbf{a} \cdot (\mathbf{b} + \mathbf{c}) = \mathbf{a} \cdot \mathbf{b} + \mathbf{a} \cdot \mathbf{c}$ |
| A scalar comes out | $(k\,\mathbf{a}) \cdot \mathbf{b} = k\,(\mathbf{a} \cdot \mathbf{b})$ |
| With itself | $\mathbf{a} \cdot \mathbf{a} = \|\mathbf{a}\|^2$ |

The last row matters: the dot product of a vector with itself is its
squared length. $(3, 4) \cdot (3, 4) = 9 + 16 = 25 = 5^2$. So length can be
written with the dot product:

$$
\|\mathbf{a}\| = \sqrt{\mathbf{a} \cdot \mathbf{a}}
$$

## Recalling the cosine

For the geometric meaning of the dot product we need the **cosine** of an
angle. Picture a circle centred at the origin with radius 1 (the unit
circle). Turn by an angle $\theta$ from the positive $x$ axis; the **$x$
coordinate** of the point you reach on the circle is $\cos \theta$.

| Angle $\theta$ | $0°$ | $60°$ | $90°$ | $120°$ | $180°$ |
|---|---|---|---|---|---|
| $\cos \theta$ | $1$ | $0.5$ | $0$ | $-0.5$ | $-1$ |

Three things to know:

- At $0°$ the cosine takes its largest value, $1$.
- Past $90°$ the cosine turns **negative**; at exactly $90°$ it is $0$.
- The cosine always lies between $-1$ and $1$.

## Geometric meaning: the angle

If $\theta$ is the angle between two vectors:

$$
\mathbf{a} \cdot \mathbf{b} = \|\mathbf{a}\|\,\|\mathbf{b}\|\,\cos \theta
$$

<figure class="fig">
<svg viewBox="0 0 292 252" width="292"><line class="grid" x1="26" y1="226" x2="26" y2="26"/><line class="line" x1="66" y1="226" x2="66" y2="26"/><line class="grid" x1="106" y1="226" x2="106" y2="26"/><line class="grid" x1="146" y1="226" x2="146" y2="26"/><line class="grid" x1="186" y1="226" x2="186" y2="26"/><line class="grid" x1="226" y1="226" x2="226" y2="26"/><line class="grid" x1="266" y1="226" x2="266" y2="26"/><line class="grid" x1="26" y1="226" x2="266" y2="226"/><line class="line" x1="26" y1="186" x2="266" y2="186"/><line class="grid" x1="26" y1="146" x2="266" y2="146"/><line class="grid" x1="26" y1="106" x2="266" y2="106"/><line class="grid" x1="26" y1="66" x2="266" y2="66"/><line class="grid" x1="26" y1="26" x2="266" y2="26"/><text class="dim" x="26" y="200" font-size="10" text-anchor="middle">-1</text><text class="dim" x="106" y="200" font-size="10" text-anchor="middle">1</text><text class="dim" x="146" y="200" font-size="10" text-anchor="middle">2</text><text class="dim" x="186" y="200" font-size="10" text-anchor="middle">3</text><text class="dim" x="226" y="200" font-size="10" text-anchor="middle">4</text><text class="dim" x="266" y="200" font-size="10" text-anchor="middle">5</text><text class="dim" x="60" y="230" font-size="10" text-anchor="end">-1</text><text class="dim" x="60" y="150" font-size="10" text-anchor="end">1</text><text class="dim" x="60" y="110" font-size="10" text-anchor="end">2</text><text class="dim" x="60" y="70" font-size="10" text-anchor="end">3</text><text class="dim" x="60" y="30" font-size="10" text-anchor="end">4</text><path class="curve3" d="M108.7,175.3 L108.2,173.6 L107.6,171.8 L107.0,170.1 L106.3,168.4 L105.5,166.7 L104.7,165.1 L103.8,163.5 L102.8,161.9 L101.8,160.4 L100.7,158.9 L99.5,157.5 L98.3,156.1 L97.0,154.8 L95.7,153.5 L94.3,152.3 L92.9,151.1 L91.4,150.1 L89.8,149.0 L88.3,148.1 L86.7,147.2 L85.0,146.3 L83.4,145.6 L81.6,144.9 L79.9,144.3"/><line class="curve" x1="66" y1="186" x2="217.5" y2="148.1"/><polygon class="dot" points="226,146 217.3,152.8 215.2,144.1"/><line class="curve2" x1="66" y1="186" x2="103.2" y2="74.3"/><polygon class="dot2" points="106,66 107.1,76.9 98.6,74.1"/><text class="ink" x="111.5" y="148.9" font-size="15" text-anchor="middle">θ</text><text class="ink" x="232" y="150" font-size="14" text-anchor="start">a</text><text class="ink" x="112" y="66" font-size="14" text-anchor="start">b</text></svg>
  <figcaption>The angle $\theta$ between the purple $\mathbf{a} = (4, 1)$ and the orange $\mathbf{b} = (1, 3)$. The dot product packs this angle, together with the two lengths, into a single number.</figcaption>
</figure>

On one side a simple calculation with components ($a_1 b_1 + a_2 b_2$), on
the other lengths and an angle. It is not at all obvious that the two are
equal; let us see where it comes from.

### Why is it true?

The **law of cosines** is Pythagoras' theorem generalised to triangles
without a right angle. In a triangle with sides $a$, $b$ and angle
$\theta$ between them, the third side $c$ satisfies:

$$
c^2 = a^2 + b^2 - 2ab\cos\theta
$$

If $\theta = 90°$ then $\cos\theta = 0$ and the formula turns into
Pythagoras: $c^2 = a^2 + b^2$.

Now build a triangle from the vectors $\mathbf{a}$ and $\mathbf{b}$. The
third side is the vector $\mathbf{a} - \mathbf{b}$ joining their tips. The
law of cosines gives:

$$
\|\mathbf{a} - \mathbf{b}\|^2 = \|\mathbf{a}\|^2 + \|\mathbf{b}\|^2 - 2\,\|\mathbf{a}\|\,\|\mathbf{b}\|\cos\theta
$$

Expand the left side with the rules of the dot product
($\|\mathbf{v}\|^2 = \mathbf{v} \cdot \mathbf{v}$ and distributivity):

$$
(\mathbf{a} - \mathbf{b}) \cdot (\mathbf{a} - \mathbf{b})
= \mathbf{a} \cdot \mathbf{a} - 2\,\mathbf{a} \cdot \mathbf{b} + \mathbf{b} \cdot \mathbf{b}
= \|\mathbf{a}\|^2 - 2\,\mathbf{a} \cdot \mathbf{b} + \|\mathbf{b}\|^2
$$

The two expressions are equal. $\|\mathbf{a}\|^2$ and $\|\mathbf{b}\|^2$
appear on both sides and cancel:

$$
-2\,\mathbf{a} \cdot \mathbf{b} = -2\,\|\mathbf{a}\|\,\|\mathbf{b}\|\cos\theta
\quad\Rightarrow\quad
\mathbf{a} \cdot \mathbf{b} = \|\mathbf{a}\|\,\|\mathbf{b}\|\cos\theta
$$

The simple multiply-and-add with components carries the angle hidden
inside it.

## What the sign tells you

Lengths are never negative, so the **sign** of the dot product is decided
by $\cos\theta$ alone:

<figure class="fig">
  <div class="versus">
    <div>
      <h4>Positive: acute angle</h4>
<svg viewBox="0 0 244 172" width="244"><line class="grid" x1="26" y1="146" x2="26" y2="26"/><line class="grid" x1="50" y1="146" x2="50" y2="26"/><line class="grid" x1="74" y1="146" x2="74" y2="26"/><line class="grid" x1="98" y1="146" x2="98" y2="26"/><line class="line" x1="122" y1="146" x2="122" y2="26"/><line class="grid" x1="146" y1="146" x2="146" y2="26"/><line class="grid" x1="170" y1="146" x2="170" y2="26"/><line class="grid" x1="194" y1="146" x2="194" y2="26"/><line class="grid" x1="218" y1="146" x2="218" y2="26"/><line class="grid" x1="26" y1="146" x2="218" y2="146"/><line class="line" x1="26" y1="122" x2="218" y2="122"/><line class="grid" x1="26" y1="98" x2="218" y2="98"/><line class="grid" x1="26" y1="74" x2="218" y2="74"/><line class="grid" x1="26" y1="50" x2="218" y2="50"/><line class="grid" x1="26" y1="26" x2="218" y2="26"/><path class="curve3" d="M147.6,115.6 L147.5,115.0 L147.3,114.5 L147.1,113.9 L146.9,113.3 L146.7,112.8 L146.5,112.2 L146.3,111.7 L146.1,111.1 L145.8,110.6 L145.5,110.0 L145.3,109.5 L145.0,109.0 L144.7,108.5 L144.4,108.0 L144.0,107.5 L143.7,107.0 L143.4,106.5 L143.0,106.0 L142.6,105.5 L142.3,105.1 L141.9,104.6 L141.5,104.2 L141.1,103.8 L140.7,103.3"/><line class="curve" x1="122" y1="122" x2="209.5" y2="100.1"/><polygon class="dot" points="218,98 209.3,104.8 207.2,96.1"/><line class="curve2" x1="122" y1="122" x2="187.8" y2="56.2"/><polygon class="dot2" points="194,50 190.1,60.3 183.7,53.9"/></svg>
      <p>$\theta < 90°$. The vectors point roughly the same way.</p>
    </div>
    <div>
      <h4>Zero: perpendicular</h4>
<svg viewBox="0 0 244 172" width="244"><line class="grid" x1="26" y1="146" x2="26" y2="26"/><line class="grid" x1="50" y1="146" x2="50" y2="26"/><line class="grid" x1="74" y1="146" x2="74" y2="26"/><line class="grid" x1="98" y1="146" x2="98" y2="26"/><line class="line" x1="122" y1="146" x2="122" y2="26"/><line class="grid" x1="146" y1="146" x2="146" y2="26"/><line class="grid" x1="170" y1="146" x2="170" y2="26"/><line class="grid" x1="194" y1="146" x2="194" y2="26"/><line class="grid" x1="218" y1="146" x2="218" y2="26"/><line class="grid" x1="26" y1="146" x2="218" y2="146"/><line class="line" x1="26" y1="122" x2="218" y2="122"/><line class="grid" x1="26" y1="98" x2="218" y2="98"/><line class="grid" x1="26" y1="74" x2="218" y2="74"/><line class="grid" x1="26" y1="50" x2="218" y2="50"/><line class="grid" x1="26" y1="26" x2="218" y2="26"/><path class="curve3" d="M134.5,117.8 L130.3,105.3 L117.8,109.5"/><line class="curve" x1="122" y1="122" x2="185.7" y2="100.8"/><polygon class="dot" points="194,98 185.9,105.4 183.1,96.9"/><line class="curve2" x1="122" y1="122" x2="100.8" y2="58.3"/><polygon class="dot2" points="98,50 105.4,58.1 96.9,60.9"/></svg>
      <p>$\theta = 90°$. The vectors point in independent directions.</p>
    </div>
    <div>
      <h4>Negative: obtuse angle</h4>
<svg viewBox="0 0 244 172" width="244"><line class="grid" x1="26" y1="146" x2="26" y2="26"/><line class="grid" x1="50" y1="146" x2="50" y2="26"/><line class="grid" x1="74" y1="146" x2="74" y2="26"/><line class="grid" x1="98" y1="146" x2="98" y2="26"/><line class="line" x1="122" y1="146" x2="122" y2="26"/><line class="grid" x1="146" y1="146" x2="146" y2="26"/><line class="grid" x1="170" y1="146" x2="170" y2="26"/><line class="grid" x1="194" y1="146" x2="194" y2="26"/><line class="grid" x1="218" y1="146" x2="218" y2="26"/><line class="grid" x1="26" y1="146" x2="218" y2="146"/><line class="line" x1="26" y1="122" x2="218" y2="122"/><line class="grid" x1="26" y1="98" x2="218" y2="98"/><line class="grid" x1="26" y1="74" x2="218" y2="74"/><line class="grid" x1="26" y1="50" x2="218" y2="50"/><line class="grid" x1="26" y1="26" x2="218" y2="26"/><path class="curve3" d="M147.0,113.7 L146.0,111.1 L144.8,108.7 L143.3,106.4 L141.5,104.2 L139.6,102.3 L137.4,100.6 L135.1,99.1 L132.7,97.9 L130.1,96.9 L127.5,96.2 L124.7,95.7 L122.0,95.6 L119.3,95.7 L116.5,96.2 L113.9,96.9 L111.3,97.9 L108.9,99.1 L106.6,100.6 L104.4,102.3 L102.5,104.2 L100.7,106.4 L99.2,108.7 L98.0,111.1 L97.0,113.7"/><line class="curve" x1="122" y1="122" x2="185.7" y2="100.8"/><polygon class="dot" points="194,98 185.9,105.4 183.1,96.9"/><line class="curve2" x1="122" y1="122" x2="58.3" y2="100.8"/><polygon class="dot2" points="50,98 60.9,96.9 58.1,105.4"/></svg>
      <p>$\theta > 90°$. The vectors point roughly opposite ways.</p>
    </div>
  </div>
  <figcaption>The sign of the dot product says whether the angle between the two vectors is smaller or larger than $90°$.</figcaption>
</figure>

The vectors in the figures: for the acute angle $(4, 1) \cdot (3, 3) = 15$ (positive), for the right angle
$(3, 1) \cdot (-1, 3) = -3 + 3 = 0$, for the obtuse angle
$(3, 1) \cdot (-3, 1) = -9 + 1 = -8$ (negative).

### Perpendicularity

Two vectors are perpendicular **if and only if** their dot product is zero
(apart from the zero vector):

$$
\mathbf{a} \perp \mathbf{b} \iff \mathbf{a} \cdot \mathbf{b} = 0
$$

A perpendicularity check without measuring or drawing:
$(2, 3) \cdot (-3, 2) = -6 + 6 = 0$, so they are perpendicular. A practical
way to find a vector perpendicular to $(p, q)$ in the plane is to swap the
components and flip the sign of one: $(-q, p)$.

In machine learning perpendicular vectors represent directions that "say
nothing about each other"; in the PCA chapter we will look for mutually
perpendicular directions.

## Finding the angle between two vectors

Solving the formula for $\cos\theta$:

$$
\cos\theta = \frac{\mathbf{a} \cdot \mathbf{b}}{\|\mathbf{a}\|\,\|\mathbf{b}\|}
$$

**Example:** $\mathbf{a} = (1, 0)$ and $\mathbf{b} = (1, 1)$.

$$
\cos\theta = \frac{1 \cdot 1 + 0 \cdot 1}{1 \cdot \sqrt{2}} = \frac{1}{\sqrt{2}} \approx 0.707
\quad\Rightarrow\quad \theta = 45°
$$

The picture confirms it: $(1, 1)$ runs exactly diagonally, at $45°$ to the
$x$ axis.

**Example:** $\mathbf{a} = (3, 4)$, $\mathbf{b} = (2, 1)$.
$\mathbf{a} \cdot \mathbf{b} = 10$, $\|\mathbf{a}\| = 5$,
$\|\mathbf{b}\| = \sqrt{5} \approx 2.236$:

$$
\cos\theta = \frac{10}{5 \cdot 2.236} \approx 0.894
\quad\Rightarrow\quad \theta \approx 26.6°
$$

Going from the cosine to the angle uses the calculator's $\cos^{-1}$
(arccos) key. Often you do not need the angle itself: the cosine value
already answers "how much do they point the same way".

## The Cauchy–Schwarz inequality

Because the cosine lies between $-1$ and $1$:

$$
|\mathbf{a} \cdot \mathbf{b}| \le \|\mathbf{a}\|\,\|\mathbf{b}\|
$$

The size of the dot product can **never exceed** the product of the
lengths. Equality holds only when the two vectors point the same way or
exactly opposite ways ($\cos\theta = \pm 1$). This inequality is used in
the proof of the triangle inequality from the previous chapter, and it
explains why cosine similarity always comes out between $-1$ and $1$.

## Projection: one vector's share in another's direction

Think of the shadow a stick casts on the ground when the sun is directly
overhead. A **projection** is a vector's "shadow" along the direction of
another vector.

<figure class="fig">
<svg viewBox="0 0 292 292" width="292"><line class="grid" x1="26" y1="266" x2="26" y2="26"/><line class="line" x1="66" y1="266" x2="66" y2="26"/><line class="grid" x1="106" y1="266" x2="106" y2="26"/><line class="grid" x1="146" y1="266" x2="146" y2="26"/><line class="grid" x1="186" y1="266" x2="186" y2="26"/><line class="grid" x1="226" y1="266" x2="226" y2="26"/><line class="grid" x1="266" y1="266" x2="266" y2="26"/><line class="grid" x1="26" y1="266" x2="266" y2="266"/><line class="line" x1="26" y1="226" x2="266" y2="226"/><line class="grid" x1="26" y1="186" x2="266" y2="186"/><line class="grid" x1="26" y1="146" x2="266" y2="146"/><line class="grid" x1="26" y1="106" x2="266" y2="106"/><line class="grid" x1="26" y1="66" x2="266" y2="66"/><line class="grid" x1="26" y1="26" x2="266" y2="26"/><text class="dim" x="26" y="240" font-size="10" text-anchor="middle">-1</text><text class="dim" x="106" y="240" font-size="10" text-anchor="middle">1</text><text class="dim" x="146" y="240" font-size="10" text-anchor="middle">2</text><text class="dim" x="186" y="240" font-size="10" text-anchor="middle">3</text><text class="dim" x="226" y="240" font-size="10" text-anchor="middle">4</text><text class="dim" x="266" y="240" font-size="10" text-anchor="middle">5</text><text class="dim" x="60" y="270" font-size="10" text-anchor="end">-1</text><text class="dim" x="60" y="190" font-size="10" text-anchor="end">1</text><text class="dim" x="60" y="150" font-size="10" text-anchor="end">2</text><text class="dim" x="60" y="110" font-size="10" text-anchor="end">3</text><text class="dim" x="60" y="70" font-size="10" text-anchor="end">4</text><text class="dim" x="60" y="30" font-size="10" text-anchor="end">5</text><line class="curve2" x1="66" y1="226" x2="219.8" y2="72.2"/><polygon class="dot2" points="226,66 222.1,76.3 215.7,69.9"/><line class="curve4" x1="66" y1="226" x2="139.8" y2="152.2"/><polygon class="dot3" points="146,146 142.1,156.3 135.7,149.9"/><line class="curve" x1="66" y1="226" x2="177.7" y2="188.8"/><polygon class="dot" points="186,186 177.9,193.4 175.1,184.9"/><line class="curve3" stroke-dasharray="5 4" x1="186" y1="186" x2="146" y2="146"/><path class="curve3" d="M137.5,154.5 L146.0,163.0 L154.5,154.5"/><text class="ink" x="192" y="190" font-size="14" text-anchor="start">a</text><text class="ink" x="232" y="66" font-size="14" text-anchor="start">b</text><text class="ink" x="136" y="140" font-size="12" text-anchor="end">projection</text></svg>
  <figcaption>The projection of the purple $\mathbf{a} = (3, 1)$ onto the direction of the orange $\mathbf{b} = (4, 4)$ is the green $(2, 2)$. The dashed line drops perpendicular to $\mathbf{b}$.</figcaption>
</figure>

**Scalar projection** (the length of the shadow):

$$
\text{proj}_{\mathbf{b}}\,\mathbf{a} = \frac{\mathbf{a} \cdot \mathbf{b}}{\|\mathbf{b}\|}
= \|\mathbf{a}\|\cos\theta
$$

**Vector projection** (the shadow itself): multiply that length by the unit
vector in the direction of $\mathbf{b}$:

$$
\text{proj}_{\mathbf{b}}\,\mathbf{a} = \frac{\mathbf{a} \cdot \mathbf{b}}{\mathbf{b} \cdot \mathbf{b}}\,\mathbf{b}
$$

The calculation in the figure: $\mathbf{a} \cdot \mathbf{b} = 12 + 4 = 16$,
$\mathbf{b} \cdot \mathbf{b} = 32$, so the projection is
$\frac{16}{32}(4, 4) = (2, 2)$. Its length is $\sqrt{8} \approx 2.83$.

If $\mathbf{b}$ is a unit vector things simplify a lot: the scalar
projection is simply $\mathbf{a} \cdot \mathbf{b}$. For example, the
projection of $(4, 2)$ onto the $x$ axis ($\mathbf{i} = (1, 0)$) is
$(4, 2) \cdot (1, 0) = 4$: exactly the vector's $x$ component. **A vector's
components are its projections onto the basic unit vectors.**

## Cosine similarity

In machine learning the similarity of two vectors is often measured by
their **angle**, not their length:

$$
\text{similarity}(\mathbf{a}, \mathbf{b}) = \cos\theta = \frac{\mathbf{a} \cdot \mathbf{b}}{\|\mathbf{a}\|\,\|\mathbf{b}\|}
$$

A value close to $1$ means they point the same way (very similar), $0$
means unrelated, $-1$ means opposite.

### Why angle rather than length?

Let us write three documents as vectors by how many times the words
"football", "match" and "cooking" appear in them:

| Document | football | match | cooking | Vector |
|---|---|---|---|---|
| Short sports report | 2 | 1 | 0 | $(2, 1, 0)$ |
| Long sports report | 4 | 2 | 0 | $(4, 2, 0)$ |
| Recipe | 0 | 1 | 3 | $(0, 1, 3)$ |

The two sports reports are on the same topic; one is twice as long as the
other.

- **Euclidean distance:** between the short and the long report
  $\sqrt{5} \approx 2.24$, between the short report and the recipe
  $\sqrt{13} \approx 3.61$. Distance sees the two sports reports as quite
  far apart.
- **Cosine similarity:** between $(2, 1, 0)$ and $(4, 2, 0)$ **exactly $1$**
  ($(4, 2, 0) = 2 \cdot (2, 1, 0)$, the same direction). Between the short
  report and the recipe only $0.14$.

Cosine similarity does not care about a document's **length**; it looks
only at **what it is about** (its direction). For text, recommender
systems and word embeddings this is usually the right measure.

If you first turn the vectors into unit vectors (normalisation, previous
chapter), cosine similarity becomes a plain dot product; large systems do
the calculation this way for speed.

## Other measures of length: norms

So far we have used Pythagoras for length. That is only one of **many**
measures of length; three come up often in machine learning.

| Norm | Formula | For $(3, -4)$ | Name |
|---|---|---|---|
| $L_2$ | $\sqrt{a_1^2 + a_2^2 + \cdots}$ | $5$ | Euclidean length |
| $L_1$ | $\lvert a_1\rvert + \lvert a_2\rvert + \cdots$ | $7$ | Manhattan length |
| $L_\infty$ | the largest $\lvert a_i\rvert$ | $4$ | Largest component |

The name **Manhattan** comes from city streets: in a grid-shaped city you
do not travel as the crow flies but along the streets (first east-west,
then north-south). The $L_1$ distance is the length of that route. In the
previous chapter we said "adding the components is not the length"; more
precisely, it is not the **Euclidean** length. Adding the absolute values
of the components is another measure of length, $L_1$.

The three always come in the same order: $L_\infty \le L_2 \le L_1$.

In machine learning:

- **$L_2$** is the most common distance; nearest neighbours, clustering.
- **$L_1$** is less sensitive to outliers; because it does not square, one large difference does not dominate.
- **Regularisation:** to keep a model's weights small, the $L_2$ or $L_1$ norm of the weight vector is added to the penalty (Ridge and Lasso).

## The dot product in machine learning

- **Linear model:** prediction $= \mathbf{w} \cdot \mathbf{x} + b$. The dot
  product of the weight vector and the feature vector. With
  $\mathbf{w} = (0.02, 0.5, -0.1)$, $\mathbf{x} = (120, 3, 10)$ and $b = 1$
  the prediction is $2.4 + 1.5 - 1 + 1 = 3.9$.
- **A neuron in a neural network:** a weighted sum of the inputs, that is
  again a dot product, then passed through a function.
- **Recommender systems:** the dot product of a user vector and a product
  vector estimates "how much will this person like this product".
- **Attention in language models:** how much one word "attends" to another
  is calculated with the dot product of two vectors.

## Common mistakes

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Wrong</h4>
      <p>$(3, 4) \cdot (2, 1) = (6, 4)$</p>
      <p>If $\mathbf{a} \cdot \mathbf{b} = 0$ one of the vectors is zero</p>
      <p>Judging similarity by distance alone</p>
      <p>$\cos\theta = \mathbf{a} \cdot \mathbf{b}$</p>
    </div>
    <div class="ok">
      <h4>Right</h4>
      <p>$(3, 4) \cdot (2, 1) = 6 + 4 = 10$, a number</p>
      <p>If zero, they are perpendicular (or one is the zero vector)</p>
      <p>Cosine similarity when length does not matter</p>
      <p>$\cos\theta = \dfrac{\mathbf{a} \cdot \mathbf{b}}{\|\mathbf{a}\|\,\|\mathbf{b}\|}$</p>
    </div>
  </div>
  <figcaption>The dot product multiplies the components, adds them and gives a single number.</figcaption>
</figure>

- **Forgetting to add the products.** Multiplying matching components and
  leaving them as a vector is not the dot product (that is a different
  operation).
- **Forgetting to divide by the lengths.** $\mathbf{a} \cdot \mathbf{b}$ on
  its own is not the cosine; only if both vectors have unit length.
- **Vectors of different dimensions.** Undefined.

## Summary

- $\mathbf{a} \cdot \mathbf{b} = \sum a_i b_i$: multiply matching components, add; the result is a number.
- $\mathbf{a} \cdot \mathbf{a} = \|\mathbf{a}\|^2$.
- $\mathbf{a} \cdot \mathbf{b} = \|\mathbf{a}\|\,\|\mathbf{b}\|\cos\theta$ (from the law of cosines).
- The sign tells the angle: positive acute, zero perpendicular, negative obtuse.
- $\cos\theta = \dfrac{\mathbf{a} \cdot \mathbf{b}}{\|\mathbf{a}\|\,\|\mathbf{b}\|}$: cosine similarity, independent of length.
- Projection $\dfrac{\mathbf{a} \cdot \mathbf{b}}{\mathbf{b} \cdot \mathbf{b}}\,\mathbf{b}$; components are projections onto the unit vectors.
- Norms: $L_2$ (Euclidean), $L_1$ (Manhattan), $L_\infty$ (largest component).
- ML: linear model $\mathbf{w} \cdot \mathbf{x} + b$, neuron, recommendation, attention.
