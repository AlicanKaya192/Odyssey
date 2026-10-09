# Vectors

In machine learning, data almost always sits in **vectors**. A house's
floor area, number of rooms and age are three numbers; written side by
side they become a single object: $(120,\ 3,\ 10)$. A photo is a vector of
thousands of pixel values, a word is a vector of hundreds of numbers, and
the weights a model learns are a vector too.

That is why vectors are the first topic of the Advanced Mathematics module. In this chapter you will
see what a vector is, how it is written, how vectors are added and scaled,
and how their length is found. In the next chapter (Dot Product) we will
learn to measure how similar two vectors are.

Before starting you need three things from the Foundational Mathematics module: the **coordinate plane**
(writing a point as $(x, y)$), **Pythagoras' theorem** ($a^2 + b^2 = c^2$)
and **square roots**. I will remind you of each as we go.

## Scalars and vectors

Some quantities are described by a single number. The room temperature is
22 degrees, a box weighs 3 kilograms, a house costs 4 million. These are
called **scalars**: they carry only a **magnitude**.

For some quantities one number is not enough. "The wind is blowing at 20
kilometres an hour" is incomplete: **which way**? North or east? Velocity,
force and displacement have both a **magnitude** and a **direction**. They
are called **vectors**.

<figure class="fig">
  <div class="versus">
    <div>
      <h4>Scalar</h4>
      <p>A single number. Only "how much".</p>
      <p>Temperature: 22°<br>Mass: 3 kg<br>Price: 4 million</p>
    </div>
    <div>
      <h4>Vector</h4>
      <p>Ordered numbers. "How much" and "which way".</p>
      <p>Wind: 3 east, 4 north<br>Position: $(2, 5)$<br>House: $(120, 3, 10)$</p>
    </div>
  </div>
  <figcaption>A scalar is one number; a vector is a list of numbers whose order matters.</figcaption>
</figure>

## Writing a vector

In the plane a vector is written with **two numbers**: how far it goes
horizontally and how far it goes vertically. These numbers are the
vector's **components**.

$$
\mathbf{v} = (3,\ 4)
$$

Here the first component is $v_1 = 3$ (3 units right) and the second is
$v_2 = 4$ (4 units up). To tell vectors apart from ordinary numbers we write
them in bold ($\mathbf{v}$) or with an arrow on top ($\vec{v}$). By hand
on paper the arrow is more practical.

The same vector can also be written vertically; this is called a **column
vector**, and later in the Advanced Mathematics module, when we work with matrices, this form will
be used:

$$
\mathbf{v} = \begin{bmatrix} 3 \\ 4 \end{bmatrix}
$$

Both forms describe the same vector; the only difference is the layout on
the page.

### Drawing it as an arrow

A vector is drawn as an **arrow**. The arrow leaves the origin $(0, 0)$,
goes 3 right and 4 up, and ends at the point $(3, 4)$:

<figure class="fig">
<svg viewBox="0 0 332 292" width="332"><line class="grid" x1="26" y1="266" x2="26" y2="26"/><line class="line" x1="66" y1="266" x2="66" y2="26"/><line class="grid" x1="106" y1="266" x2="106" y2="26"/><line class="grid" x1="146" y1="266" x2="146" y2="26"/><line class="grid" x1="186" y1="266" x2="186" y2="26"/><line class="grid" x1="226" y1="266" x2="226" y2="26"/><line class="grid" x1="266" y1="266" x2="266" y2="26"/><line class="grid" x1="306" y1="266" x2="306" y2="26"/><line class="grid" x1="26" y1="266" x2="306" y2="266"/><line class="line" x1="26" y1="226" x2="306" y2="226"/><line class="grid" x1="26" y1="186" x2="306" y2="186"/><line class="grid" x1="26" y1="146" x2="306" y2="146"/><line class="grid" x1="26" y1="106" x2="306" y2="106"/><line class="grid" x1="26" y1="66" x2="306" y2="66"/><line class="grid" x1="26" y1="26" x2="306" y2="26"/><text class="dim" x="26" y="240" font-size="10" text-anchor="middle">-1</text><text class="dim" x="106" y="240" font-size="10" text-anchor="middle">1</text><text class="dim" x="146" y="240" font-size="10" text-anchor="middle">2</text><text class="dim" x="186" y="240" font-size="10" text-anchor="middle">3</text><text class="dim" x="226" y="240" font-size="10" text-anchor="middle">4</text><text class="dim" x="266" y="240" font-size="10" text-anchor="middle">5</text><text class="dim" x="306" y="240" font-size="10" text-anchor="middle">6</text><text class="dim" x="60" y="270" font-size="10" text-anchor="end">-1</text><text class="dim" x="60" y="190" font-size="10" text-anchor="end">1</text><text class="dim" x="60" y="150" font-size="10" text-anchor="end">2</text><text class="dim" x="60" y="110" font-size="10" text-anchor="end">3</text><text class="dim" x="60" y="70" font-size="10" text-anchor="end">4</text><text class="dim" x="60" y="30" font-size="10" text-anchor="end">5</text><line class="curve2" stroke-dasharray="5 4" x1="66" y1="226" x2="186" y2="226"/><line class="curve2" stroke-dasharray="5 4" x1="186" y1="226" x2="186" y2="66"/><line class="curve" x1="66" y1="226" x2="180.7" y2="73.0"/><polygon class="dot" points="186,66 183.6,76.7 176.4,71.3"/><text class="ink" x="126.0" y="220" font-size="13" text-anchor="middle">3</text><text class="ink" x="192" y="146" font-size="13" text-anchor="start">4</text><text class="ink" x="110.0" y="130.0" font-size="14" text-anchor="end">v = (3, 4)</text></svg>
  <figcaption>The purple arrow is $\mathbf{v} = (3, 4)$. The dashed orange lines are its components: first 3 right, then 4 up.</figcaption>
</figure>

The arrow has two properties:

- **Direction:** the way the arrow points.
- **Length (magnitude):** how long the arrow is. We will calculate it with Pythagoras below.

### Order matters

$(3, 4)$ and $(4, 3)$ are **different** vectors: one is "3 right, 4 up",
the other "4 right, 3 up". A vector is not a **set** but an **ordered**
list. In the house example $(120, 3, 10)$ means "120 square metres, 3
rooms, 10 years old"; mixing up the order creates a 3-square-metre house
with 120 rooms.

## Arrow or list?

You can look at a vector in two ways, and both are right:

1. **Geometric view:** a vector is an arrow; it has a direction and a length.
2. **Numerical view:** a vector is an ordered list of numbers.

In the plane (2 dimensions) and in space (3 dimensions) the two views
translate into each other: every arrow is a list, every list is an arrow.
But in machine learning vectors usually carry **far more** numbers:

- A house: $(120,\ 3,\ 10,\ 2,\ 1)$ — floor area, rooms, age, floor, parking. **5 dimensions.**
- A 28 × 28 black-and-white image: **784 dimensions.**
- A word in a language model: often **hundreds of dimensions.**

We cannot draw a 784-dimensional arrow. But here is the good news: **every
rule** in this chapter (addition, scaling, length) works in 784 dimensions
exactly as it does in 2. We understand it by drawing in 2 dimensions, then
apply the same calculation to as many numbers as we like.

The set of vectors made of $n$ real numbers is written $\mathbb{R}^n$.
$\mathbb{R}^2$ is the plane, $\mathbb{R}^3$ is space; the house vector is
an element of $\mathbb{R}^5$.

## A vector from two points

An arrow that does not start at the origin is also a vector. The arrow from
$A(1, 1)$ to $B(4, 5)$ goes "3 right, 4 up". This vector is written
$\overrightarrow{AB}$ and is found as **end minus start**:

$$
\overrightarrow{AB} = B - A = (4 - 1,\ 5 - 1) = (3,\ 4)
$$

<figure class="fig">
<svg viewBox="0 0 332 332" width="332"><line class="grid" x1="26" y1="306" x2="26" y2="26"/><line class="line" x1="66" y1="306" x2="66" y2="26"/><line class="grid" x1="106" y1="306" x2="106" y2="26"/><line class="grid" x1="146" y1="306" x2="146" y2="26"/><line class="grid" x1="186" y1="306" x2="186" y2="26"/><line class="grid" x1="226" y1="306" x2="226" y2="26"/><line class="grid" x1="266" y1="306" x2="266" y2="26"/><line class="grid" x1="306" y1="306" x2="306" y2="26"/><line class="grid" x1="26" y1="306" x2="306" y2="306"/><line class="line" x1="26" y1="266" x2="306" y2="266"/><line class="grid" x1="26" y1="226" x2="306" y2="226"/><line class="grid" x1="26" y1="186" x2="306" y2="186"/><line class="grid" x1="26" y1="146" x2="306" y2="146"/><line class="grid" x1="26" y1="106" x2="306" y2="106"/><line class="grid" x1="26" y1="66" x2="306" y2="66"/><line class="grid" x1="26" y1="26" x2="306" y2="26"/><text class="dim" x="26" y="280" font-size="10" text-anchor="middle">-1</text><text class="dim" x="106" y="280" font-size="10" text-anchor="middle">1</text><text class="dim" x="146" y="280" font-size="10" text-anchor="middle">2</text><text class="dim" x="186" y="280" font-size="10" text-anchor="middle">3</text><text class="dim" x="226" y="280" font-size="10" text-anchor="middle">4</text><text class="dim" x="266" y="280" font-size="10" text-anchor="middle">5</text><text class="dim" x="306" y="280" font-size="10" text-anchor="middle">6</text><text class="dim" x="60" y="310" font-size="10" text-anchor="end">-1</text><text class="dim" x="60" y="230" font-size="10" text-anchor="end">1</text><text class="dim" x="60" y="190" font-size="10" text-anchor="end">2</text><text class="dim" x="60" y="150" font-size="10" text-anchor="end">3</text><text class="dim" x="60" y="110" font-size="10" text-anchor="end">4</text><text class="dim" x="60" y="70" font-size="10" text-anchor="end">5</text><text class="dim" x="60" y="30" font-size="10" text-anchor="end">6</text><line class="curve3" stroke-dasharray="5 4" x1="66" y1="266" x2="186" y2="106"/><circle class="dot2" cx="106" cy="226" r="4"/><circle class="dot2" cx="226" cy="66" r="4"/><line class="curve" x1="106" y1="226" x2="220.7" y2="73.0"/><polygon class="dot" points="226,66 223.6,76.7 216.4,71.3"/><text class="ink" x="114" y="240" font-size="13" text-anchor="start">A(1, 1)</text><text class="ink" x="234" y="70" font-size="13" text-anchor="start">B(4, 5)</text><text class="dim" x="122.0" y="162.0" font-size="12" text-anchor="end">(3, 4)</text></svg>
  <figcaption>The purple arrow from $A$ to $B$ and the dashed arrow drawn from the origin are the same vector: both are $(3, 4)$.</figcaption>
</figure>

This gives an important fact: **where a vector sits does not matter.** Two
arrows pointing the same way with the same length are the same vector. If
you slide a vector across the plane it does not change; only its
**direction and length** define it.

Mind the order: $\overrightarrow{BA} = A - B = (-3, -4)$. The same length
but exactly the opposite direction. The answer to "from where to where"
flips the signs.

## Addition

Two vectors are added **component by component**:

$$
\mathbf{v} + \mathbf{w} = (v_1 + w_1,\ v_2 + w_2)
$$

**Example:** if $\mathbf{v} = (4, 1)$ and $\mathbf{w} = (1, 3)$ then
$\mathbf{v} + \mathbf{w} = (4 + 1,\ 1 + 3) = (5, 4)$.

The geometric meaning is very natural: first walk $\mathbf{v}$, then from
where you are walk $\mathbf{w}$. Where you end up is $\mathbf{v} + \mathbf{w}$.

<figure class="fig">
<svg viewBox="0 0 332 292" width="332"><line class="grid" x1="26" y1="266" x2="26" y2="26"/><line class="line" x1="66" y1="266" x2="66" y2="26"/><line class="grid" x1="106" y1="266" x2="106" y2="26"/><line class="grid" x1="146" y1="266" x2="146" y2="26"/><line class="grid" x1="186" y1="266" x2="186" y2="26"/><line class="grid" x1="226" y1="266" x2="226" y2="26"/><line class="grid" x1="266" y1="266" x2="266" y2="26"/><line class="grid" x1="306" y1="266" x2="306" y2="26"/><line class="grid" x1="26" y1="266" x2="306" y2="266"/><line class="line" x1="26" y1="226" x2="306" y2="226"/><line class="grid" x1="26" y1="186" x2="306" y2="186"/><line class="grid" x1="26" y1="146" x2="306" y2="146"/><line class="grid" x1="26" y1="106" x2="306" y2="106"/><line class="grid" x1="26" y1="66" x2="306" y2="66"/><line class="grid" x1="26" y1="26" x2="306" y2="26"/><text class="dim" x="26" y="240" font-size="10" text-anchor="middle">-1</text><text class="dim" x="106" y="240" font-size="10" text-anchor="middle">1</text><text class="dim" x="146" y="240" font-size="10" text-anchor="middle">2</text><text class="dim" x="186" y="240" font-size="10" text-anchor="middle">3</text><text class="dim" x="226" y="240" font-size="10" text-anchor="middle">4</text><text class="dim" x="266" y="240" font-size="10" text-anchor="middle">5</text><text class="dim" x="306" y="240" font-size="10" text-anchor="middle">6</text><text class="dim" x="60" y="270" font-size="10" text-anchor="end">-1</text><text class="dim" x="60" y="190" font-size="10" text-anchor="end">1</text><text class="dim" x="60" y="150" font-size="10" text-anchor="end">2</text><text class="dim" x="60" y="110" font-size="10" text-anchor="end">3</text><text class="dim" x="60" y="70" font-size="10" text-anchor="end">4</text><text class="dim" x="60" y="30" font-size="10" text-anchor="end">5</text><line class="curve3" stroke-dasharray="5 4" x1="66" y1="226" x2="106" y2="106"/><line class="curve3" stroke-dasharray="5 4" x1="106" y1="106" x2="266" y2="66"/><line class="curve" x1="66" y1="226" x2="217.5" y2="188.1"/><polygon class="dot" points="226,186 217.3,192.8 215.2,184.1"/><line class="curve2" x1="226" y1="186" x2="263.2" y2="74.3"/><polygon class="dot2" points="266,66 267.1,76.9 258.6,74.1"/><line class="curve4" x1="66" y1="226" x2="259.1" y2="71.5"/><polygon class="dot3" points="266,66 261.0,75.8 255.4,68.8"/><text class="ink" x="154.0" y="220.0" font-size="14" text-anchor="middle">v</text><text class="ink" x="254.0" y="126.0" font-size="14" text-anchor="start">w</text><text class="ink" x="152.0" y="138.0" font-size="14" text-anchor="end">v + w</text></svg>
  <figcaption>The orange $\mathbf{w}$ is drawn from the tip of the purple $\mathbf{v}$; the green arrow goes from the start to the final point: $\mathbf{v} + \mathbf{w} = (5, 4)$. The dashed lines show the other order (first $\mathbf{w}$, then $\mathbf{v}$): it reaches the same point.</figcaption>
</figure>

This is called **tip-to-tail addition** (or the triangle rule). The shape
completed by the dashed lines is a **parallelogram**; the sum vector is
its diagonal.

The properties of addition are the same as for numbers:

- **Commutative:** $\mathbf{v} + \mathbf{w} = \mathbf{w} + \mathbf{v}$ (the two paths in the figure reach the same place).
- **Associative:** $(\mathbf{u} + \mathbf{v}) + \mathbf{w} = \mathbf{u} + (\mathbf{v} + \mathbf{w})$.
- **Zero vector:** $\mathbf{0} = (0, 0)$; $\mathbf{v} + \mathbf{0} = \mathbf{v}$. Not walking at all.

**Only vectors of the same dimension can be added.** Adding $(1, 2)$ and
$(1, 2, 3)$ is undefined: the third component has no partner. If you write
one house as $(120, 3, 10)$ and another as $(100, 4)$ you cannot add them;
they describe different things.

## Subtraction

Subtraction is also component by component:

$$
\mathbf{v} - \mathbf{w} = (v_1 - w_1,\ v_2 - w_2)
$$

$(4, 1) - (1, 3) = (3, -2)$.

Its meaning: $\mathbf{v} - \mathbf{w}$ is the vector **from the tip of
$\mathbf{w}$ to the tip of $\mathbf{v}$**. It is the same rule as "the
vector between two points": end minus start.

Difference vectors are used all the time in machine learning: the
difference between two customers, two houses or two images is a vector.
The **length** of that difference says how far apart they are; we will
see it shortly.

## Multiplying by a scalar

Multiplying a vector by a number (a scalar) means multiplying every
component by that number:

$$
c \cdot \mathbf{v} = (c\, v_1,\ c\, v_2)
$$

<figure class="fig">
<svg viewBox="0 0 372 252" width="372"><line class="grid" x1="26" y1="226" x2="26" y2="26"/><line class="grid" x1="66" y1="226" x2="66" y2="26"/><line class="grid" x1="106" y1="226" x2="106" y2="26"/><line class="line" x1="146" y1="226" x2="146" y2="26"/><line class="grid" x1="186" y1="226" x2="186" y2="26"/><line class="grid" x1="226" y1="226" x2="226" y2="26"/><line class="grid" x1="266" y1="226" x2="266" y2="26"/><line class="grid" x1="306" y1="226" x2="306" y2="26"/><line class="grid" x1="346" y1="226" x2="346" y2="26"/><line class="grid" x1="26" y1="226" x2="346" y2="226"/><line class="grid" x1="26" y1="186" x2="346" y2="186"/><line class="line" x1="26" y1="146" x2="346" y2="146"/><line class="grid" x1="26" y1="106" x2="346" y2="106"/><line class="grid" x1="26" y1="66" x2="346" y2="66"/><line class="grid" x1="26" y1="26" x2="346" y2="26"/><text class="dim" x="26" y="160" font-size="10" text-anchor="middle">-3</text><text class="dim" x="66" y="160" font-size="10" text-anchor="middle">-2</text><text class="dim" x="106" y="160" font-size="10" text-anchor="middle">-1</text><text class="dim" x="186" y="160" font-size="10" text-anchor="middle">1</text><text class="dim" x="226" y="160" font-size="10" text-anchor="middle">2</text><text class="dim" x="266" y="160" font-size="10" text-anchor="middle">3</text><text class="dim" x="306" y="160" font-size="10" text-anchor="middle">4</text><text class="dim" x="346" y="160" font-size="10" text-anchor="middle">5</text><text class="dim" x="140" y="230" font-size="10" text-anchor="end">-2</text><text class="dim" x="140" y="190" font-size="10" text-anchor="end">-1</text><text class="dim" x="140" y="110" font-size="10" text-anchor="end">1</text><text class="dim" x="140" y="70" font-size="10" text-anchor="end">2</text><text class="dim" x="140" y="30" font-size="10" text-anchor="end">3</text><line class="curve2" x1="146" y1="146" x2="298.1" y2="69.9"/><polygon class="dot2" points="306,66 299.0,74.5 295.0,66.5"/><line class="curve" x1="146" y1="146" x2="218.1" y2="109.9"/><polygon class="dot" points="226,106 219.0,114.5 215.0,106.5"/><line class="curve4" x1="146" y1="146" x2="73.9" y2="182.1"/><polygon class="dot3" points="66,186 73.0,177.5 77.0,185.5"/><text class="ink" x="230" y="98" font-size="14" text-anchor="start">v</text><text class="ink" x="310" y="60" font-size="14" text-anchor="start">2v</text><text class="ink" x="60" y="190" font-size="14" text-anchor="end">−v</text></svg>
  <figcaption>Purple is $\mathbf{v} = (2, 1)$. Orange $2\mathbf{v} = (4, 2)$: same direction, twice as long. Green $-\mathbf{v} = (-2, -1)$: same length, opposite direction.</figcaption>
</figure>

There are four cases depending on the value of the scalar:

| Scalar | Effect | Example ($\mathbf{v} = (2, 1)$) |
|---|---|---|
| $c > 1$ | Same direction, longer | $2\mathbf{v} = (4, 2)$ |
| $0 < c < 1$ | Same direction, shorter | $0.5\,\mathbf{v} = (1, 0.5)$ |
| $c = 0$ | Zero vector | $0\,\mathbf{v} = (0, 0)$ |
| $c < 0$ | **Direction flips** | $-\mathbf{v} = (-2, -1)$ |

Multiplying by a scalar **does not turn** a vector; it either keeps its
direction or reverses it exactly. That is where the name comes from: to
"scale".

Subtraction is really addition combined with scaling:
$\mathbf{v} - \mathbf{w} = \mathbf{v} + (-1)\,\mathbf{w}$.

## Linear combinations

Combining addition and scaling gives the most important operation in
vector algebra:

$$
a\,\mathbf{v} + b\,\mathbf{w}
$$

This is called a **linear combination** of $\mathbf{v}$ and $\mathbf{w}$.
The numbers $a$ and $b$ are the **coefficients**.

**Example:** $\mathbf{v} = (1, 2)$, $\mathbf{w} = (3, 1)$ and $a = 2$, $b = -1$:

$$
2\,(1, 2) + (-1)\,(3, 1) = (2, 4) + (-3, -1) = (-1, 3)
$$

An everyday example: a café sells two blends. One pack of blend A contains
1 unit of coffee and 2 units of milk: $(1, 2)$. Blend B has 3 units of
coffee and 1 of milk: $(3, 1)$. Buying 2 packs of A and 1 pack of B gives a
total of $2(1, 2) + 1(3, 1) = (5, 5)$ in coffee and milk.

### Writing with unit vectors

There are two special vectors in the plane:

$$
\mathbf{i} = (1, 0) \qquad \mathbf{j} = (0, 1)
$$

One is one unit to the right, the other one unit up. **Every** vector can
be written as a linear combination of them:

$$
(3, 4) = 3\,(1, 0) + 4\,(0, 1) = 3\,\mathbf{i} + 4\,\mathbf{j}
$$

The components are really just how many steps are taken in these two basic
directions. Later in the Advanced Mathematics module (Linear Independence, Basis and Rank) this idea
will be generalised under the name "basis".

Linear combinations are everywhere in machine learning: a linear model makes
its prediction as a weighted sum of the features. House price
$= w_1 \cdot \text{area} + w_2 \cdot \text{rooms} + w_3 \cdot \text{age} + b$.
What the model learns is those $w$ coefficients.

## Length (magnitude)

The length of a vector is found with **Pythagoras' theorem**. Think of the
arrow $\mathbf{v} = (3, 4)$: it is the hypotenuse of a right triangle that
goes 3 across and 4 up.

$$
\|\mathbf{v}\| = \sqrt{v_1^2 + v_2^2} = \sqrt{3^2 + 4^2} = \sqrt{25} = 5
$$

$\|\mathbf{v}\|$ is read "the length (or **norm**) of v". A single bar
$|x|$ was the absolute value of a number; double bars are the length of a
vector. The idea is the same: "how big, regardless of sign".

In three dimensions one more component joins in:

$$
\|(2, -1, 2)\| = \sqrt{2^2 + (-1)^2 + 2^2} = \sqrt{9} = 3
$$

The general formula, for $n$ dimensions:

$$
\|\mathbf{v}\| = \sqrt{v_1^2 + v_2^2 + \cdots + v_n^2} = \sqrt{\sum_{i=1}^{n} v_i^2}
$$

Three properties of length:

- **It is never negative**; only the zero vector has length $0$.
- **A scalar comes out:** $\|c\,\mathbf{v}\| = |c|\,\|\mathbf{v}\|$. $\|{-2}\,(3, 4)\| = 2 \cdot 5 = 10$.
- **Triangle inequality:** $\|\mathbf{v} + \mathbf{w}\| \le \|\mathbf{v}\| + \|\mathbf{w}\|$. The length of a sum **cannot exceed** the sum of the lengths.

The triangle inequality can be read from the figure: the green arrow in the
addition figure is one side of a triangle, $\mathbf{v}$ and $\mathbf{w}$
are the other two. One side can never be longer than the other two
together. In numbers: $\|(4, 1)\| + \|(1, 3)\| \approx 4.12 + 3.16 = 7.28$,
but $\|(5, 4)\| \approx 6.40$.

## Unit vectors: direction only

A vector whose length is exactly $1$ is a **unit vector**. Divide any
vector by its own length and you get the unit vector pointing the same
way:

$$
\hat{\mathbf{v}} = \frac{\mathbf{v}}{\|\mathbf{v}\|}
$$

For $\mathbf{v} = (3, 4)$, $\|\mathbf{v}\| = 5$, so
$\hat{\mathbf{v}} = (3/5,\ 4/5) = (0.6,\ 0.8)$. Check:
$\sqrt{0.6^2 + 0.8^2} = \sqrt{0.36 + 0.64} = 1$.

This is called **normalisation**. A unit vector carries "direction only"
and throws away the length. This is very useful when comparing two
documents: if a long document and a short one are about the same topic,
you need to discard their lengths and look only at their directions (next
chapter).

The zero vector has **no** unit vector: its length is $0$ and you cannot
divide by zero. It has no direction anyway.

## Distance between two points

The distance between two points is the length of the difference vector
between them:

$$
d(\mathbf{a}, \mathbf{b}) = \|\mathbf{b} - \mathbf{a}\|
$$

Between $P(2, 3)$ and $Q(5, 7)$: $Q - P = (3, 4)$, whose length is $5$.

This is called the **Euclidean distance** and it is one of the most basic
tools in machine learning. The nearest-neighbour (KNN) algorithm finds the
examples closest to a new point using this distance.

### The scale trap

Take two houses: $\mathbf{a} = (120, 3, 10)$ and $\mathbf{b} = (100, 4, 12)$
(floor area, rooms, age).

$$
\mathbf{a} - \mathbf{b} = (20, -1, -2) \qquad
\|\mathbf{a} - \mathbf{b}\| = \sqrt{400 + 1 + 4} = \sqrt{405} \approx 20.12
$$

Almost all of the distance comes from the floor area ($1$ and $4$ are
negligible next to $400$). Because area is measured in hundreds and rooms
in ones, area **flattens** the distance. Had we written the area in units
of a hundred square metres ($1.20$ and $1.00$), the distance would be
$\approx 2.24$ and the room and age differences would become decisive.

This is a mathematical fact: **distance depends on the scale of the
components.** It is exactly why machine learning scales features
(standardisation).

## Common mistakes

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Wrong</h4>
      <p>$\|\mathbf{v} + \mathbf{w}\| = \|\mathbf{v}\| + \|\mathbf{w}\|$</p>
      <p>$\|(3, 4)\| = 3 + 4 = 7$</p>
      <p>$\overrightarrow{AB} = A - B$</p>
      <p>$(1, 2) + 5 = (6, 7)$</p>
    </div>
    <div class="ok">
      <h4>Right</h4>
      <p>$\|\mathbf{v} + \mathbf{w}\| \le \|\mathbf{v}\| + \|\mathbf{w}\|$</p>
      <p>$\|(3, 4)\| = \sqrt{9 + 16} = 5$</p>
      <p>$\overrightarrow{AB} = B - A$</p>
      <p>A vector and a number are not added; $5\,(1, 2) = (5, 10)$ is a product</p>
    </div>
  </div>
  <figcaption>Length is not the sum of the components but the square root of the sum of their squares.</figcaption>
</figure>

- **Finding length by adding components.** The length of $(3, 4)$ is $5$,
  not $7$: the straight-line distance is shorter than walking right and
  then up.
- **Squaring a negative component wrongly.** $(-3)^2 = 9$, not $-9$. That
  is why length is never negative.
- **Adding vectors of different dimensions.** Undefined.
- **Adding a number to a vector.** A vector and a number are not added;
  they can only be multiplied.

## Summary

- A vector is a list of numbers in which order matters; it is also an
  arrow with a direction and a length. $\mathbb{R}^n$ is the set of vectors
  with $n$ numbers.
- A vector from two points: **end minus start**. Sliding a vector does not change it.
- Addition and subtraction are component by component; geometrically tip to tail.
- Scaling multiplies every component; it keeps the direction or (if negative) reverses it.
- The linear combination $a\,\mathbf{v} + b\,\mathbf{w}$ is the basis of linear models.
- Length $\|\mathbf{v}\| = \sqrt{\sum v_i^2}$ (Pythagoras); unit vector $\mathbf{v}/\|\mathbf{v}\|$.
- The distance between two points is the length of the difference vector
  (Euclidean distance); it depends on the scale of the components.
