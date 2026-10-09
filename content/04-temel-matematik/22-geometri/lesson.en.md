# Geometry Basics

Geometry is the mathematics of shapes, lengths, angles and areas. It shows
up in machine learning in surprisingly many places: the distance between
two data points is the Pythagorean relation itself, the similarity of two
vectors is measured by the angle between them, and an object detection
model measures how good its predicted box is by the overlapping area of two
rectangles. In this section we will see angles, triangles, the Pythagorean
theorem, similarity, the perimeter and area of basic shapes, the circle and
the volume of solids. The next section, Trigonometry, is built on the right
triangles here.

Prerequisites: Roots, Ratio, Proportion and Percentages, The Coordinate
Plane and Lines.

## Angles

When two rays share a starting point they form an **angle**. Angles are
measured in **degrees**; a full turn is $360°$.

| Name | Measure | Example |
|---|---|---|
| acute angle | between $0°$ and $90°$ | $45°$ |
| right angle | exactly $90°$ | the corner of a sheet of paper |
| obtuse angle | between $90°$ and $180°$ | $120°$ |
| straight angle | $180°$ | a straight line |
| full angle | $360°$ | a full turn |

**Complementary and supplementary.** Two angles adding up to $90°$ are
**complementary**; two adding up to $180°$ are **supplementary**. The
complement of $35°$ is $55°$, its supplement $145°$.

**Vertical angles.** The opposite angles of two crossing lines are equal.
If one is $70°$, the opposite one is $70°$ too and the ones beside it are
$110°$.

**Parallel lines and a transversal.** When a third line crosses two
parallel lines, the **alternate interior angles** are equal (like the two
corners of the letter Z). The angle sum of a triangle follows from this.

## Triangles

**The interior angles add up to $180°$.** Draw a line through the top of
the triangle parallel to the base. On the parallel line, copies of the base
angles appear on either side of the top angle (alternate interior angles).
The three angles at the top lie side by side and form a straight angle.

<figure class="fig">
<svg viewBox="0 0 440 264" width="440"><polygon class="curve" fill="none" points="60,210 380,210 170,50"/><line class="curve3" stroke-dasharray="5 4" x1="20" y1="50" x2="420" y2="50"/><path class="curve2" fill="none" stroke-width="2" d="M 86.0 210.0 A 26 26 0 0 0 74.7 188.6"/><text class="ink" x="97.2" y="195.4" font-size="14" text-anchor="middle">α</text><path class="curve4" fill="none" stroke-width="2" d="M 359.3 194.2 A 26 26 0 0 0 354.0 210.0"/><text class="ink" x="340.2" y="201.6" font-size="14" text-anchor="middle">β</text><path class="curve" fill="none" stroke-width="2" d="M 155.3 71.4 A 26 26 0 0 0 190.7 65.8"/><text class="ink" x="176.6" y="96.5" font-size="14" text-anchor="middle">γ</text><path class="curve2" fill="none" stroke-width="2" d="M 144.0 50.0 A 26 26 0 0 0 155.3 71.4"/><text class="ink" x="132.8" y="74.6" font-size="14" text-anchor="middle">α</text><path class="curve4" fill="none" stroke-width="2" d="M 196.0 50.0 A 26 26 0 0 1 190.7 65.8"/><text class="ink" x="209.8" y="68.4" font-size="14" text-anchor="middle">β</text><text class="ink" x="220" y="250" font-size="12" text-anchor="middle">the three angles at the top make a straight angle: α + γ + β = 180°</text></svg>
  <figcaption>α and β at the base repeat exactly on either side of the top, on the parallel line. At the top α, γ and β lie side by side and form a straight line; together they make 180°.</figcaption>
</figure>

A triangle with two angles of $50°$ and $60°$ has a third angle of
$180° - 110° = 70°$.

**Kinds.** By sides: **equilateral** (three equal sides, each angle $60°$),
**isosceles** (two equal sides, and the angles opposite them equal),
**scalene** (all different). By angles: **acute**, **right** (one angle
$90°$), **obtuse** (one angle greater than $90°$).

**Triangle inequality.** Each side is shorter than the sum of the other
two: $a + b > c$. Sticks of length $2$, $3$ and $6$ cannot make a triangle,
because $2 + 3 < 6$; the two short sticks cannot reach each other. It is
another way of saying "the shortest path between two points is a straight
line".

**Exterior angle.** The exterior angle formed by extending a side equals
the sum of the other two interior angles: if the interior angle is
$\gamma$, the exterior angle is $180° - \gamma = \alpha + \beta$.

## The Pythagorean theorem

In a right triangle the longest side, opposite the right angle, is called
the **hypotenuse**. If the legs are $a$ and $b$ and the hypotenuse is $c$:

$$
a^2 + b^2 = c^2
$$

<figure class="fig">
<svg viewBox="0 0 440 278" width="440"><polygon class="dot" opacity="0.35" points="110,176 198,176 198,264 110,264"/><polygon class="dot2" opacity="0.35" points="110,176 110,110 44,110 44,176"/><polygon class="dot3" opacity="0.35" points="198,176 110,110 176,22 264,88"/><polygon class="curve" fill="none" points="110,176 198,176 110,110"/><polyline class="curve3" fill="none" points="110,165.0 121.0,165.0 121.0,176"/><text class="ink" x="154" y="225" font-size="16" text-anchor="middle">16</text><text class="ink" x="77.0" y="148.0" font-size="16" text-anchor="middle">9</text><text class="ink" x="187.0" y="104.0" font-size="16" text-anchor="middle">25</text><text class="dim" x="154" y="170" font-size="12" text-anchor="middle">4</text><text class="dim" x="118" y="147.0" font-size="12" text-anchor="start">3</text><text class="dim" x="162" y="141.0" font-size="12" text-anchor="start">5</text><text class="ink" x="330" y="240" font-size="14" text-anchor="middle">9 + 16 = 25</text></svg>
  <figcaption>A square drawn on each side of the right triangle with sides 3, 4 and 5. The squares on the legs have areas 9 and 16; the square on the hypotenuse has area 25. The two small squares together equal the large one.</figcaption>
</figure>

**Example.** A $10$ metre ladder leans against a wall with its foot $6$
metres away. How high up the wall does it reach? $6^2 + h^2 = 10^2$, so
$h^2 = 64$ and $h = 8$ metres.

**Familiar triples.** $3$-$4$-$5$, $5$-$12$-$13$, $8$-$15$-$17$ and their
multiples (such as $6$-$8$-$10$). Recognising them saves time.

**The converse holds too.** If the sides satisfy $a^2 + b^2 = c^2$, the
triangle is right. $7$, $24$, $25$: $49 + 576 = 625$ ✓, a right triangle.
If not: when $c^2$ is larger the triangle is obtuse, when smaller acute.

**The distance formula comes from here.** The
$d = \sqrt{\Delta x^2 + \Delta y^2}$ of The Coordinate Plane and Lines is
the hypotenuse of the right triangle formed by the horizontal and vertical
differences. In three dimensions one term is added: the distance between
$(1, 2, 3)$ and $(4, 6, 3)$ is $\sqrt{9 + 16 + 0} = 5$.

## Similarity

Two shapes with the same angles and **proportional** sides are called
**similar**. If the ratio is $k$, every side is $k$ times as long.

**The shadow problem.** A $2$ metre stick casts a $3$ metre shadow; at the
same moment a tree casts a $15$ metre shadow. The sun's rays make the two
triangles similar: $\frac{h}{15} = \frac{2}{3}$, so the tree is $10$
metres.

**Special right triangles.** Two triangles that Trigonometry will use all
the time:

| Angles | Side ratios | From |
|---|---|---|
| $45°$, $45°$, $90°$ | $1 : 1 : \sqrt{2}$ | the diagonal of a square |
| $30°$, $60°$, $90°$ | $1 : \sqrt{3} : 2$ | half of an equilateral triangle |

The diagonal of a square with side $1$ is $\sqrt{1 + 1} = \sqrt{2}$ by
Pythagoras. Cutting an equilateral triangle with side $2$ in half gives a
right triangle with sides $1$, $2$ and $\sqrt{4 - 1} = \sqrt{3}$.

## Perimeter and area

The **perimeter** is the sum of the sides, the **area** the space the
shape covers; area is measured in unit squares ($\text{cm}^2$,
$\text{m}^2$).

| Shape | Perimeter | Area |
|---|---|---|
| square, side $a$ | $4a$ | $a^2$ |
| rectangle, $a \times b$ | $2(a + b)$ | $a \cdot b$ |
| triangle, base $t$, height $h$ | sum of the sides | $\frac{1}{2} t h$ |
| parallelogram | sum of the sides | $t \cdot h$ |
| trapezoid, bases $a$ and $c$ | sum of the sides | $\frac{(a + c)}{2} h$ |

The **height** is the distance measured at right angles to the base; not
the slanted side.

<figure class="fig">
<svg viewBox="0 0 440 220" width="440"><rect class="box" x="100" y="30" width="240" height="160"/><polygon class="dot" opacity="0.4" points="100,190 340,190 180,30"/><polygon class="curve" fill="none" points="100,190 340,190 180,30"/><line class="curve2" stroke-dasharray="5 4" x1="180" y1="190" x2="180" y2="30"/><text class="ink" x="220" y="208" font-size="12" text-anchor="middle">base 6</text><text class="ink" x="186" y="114" font-size="12" text-anchor="start">height 4</text><text class="ink" x="220" y="20" font-size="13" text-anchor="middle">area = ½ · 6 · 4 = 12</text></svg>
  <figcaption>The triangle with base 6 and height 4 fits inside a 6 × 4 rectangle. The height line splits the rectangle in two, and the triangle covers exactly half of each piece; that is why its area is half of the rectangle.</figcaption>
</figure>

**Example.** A trapezoid with bases $4$ and $10$ and height $5$ has area
$\frac{4 + 10}{2} \cdot 5 = 35$. A trapezoid behaves like a rectangle as
wide as the average of its bases.

## Circles

A **circle** is the set of points at equal distance from a centre; the
**disc** is its inside. The distance from the centre to the circle is the
**radius** $r$; a segment across the circle through the centre is the
**diameter** $2r$.

In every circle the ratio of the circumference to the diameter is the same
number: $\pi \approx 3.14159$.

$$
\text{circumference} = 2 \pi r \qquad \text{area} = \pi r^2
$$

For $r = 5$ the circumference is $10\pi \approx 31.42$ and the area
$25\pi \approx 78.54$.

<figure class="fig">
<svg viewBox="0 0 440 236" width="440"><circle class="box" cx="150" cy="120" r="95"/><path class="dot" opacity="0.4" d="M 150 120 L 245 120 A 95 95 0 0 0 197.5 37.7 Z"/><line class="curve" x1="150" y1="120" x2="245" y2="120"/><line class="curve" x1="150" y1="120" x2="197.5" y2="37.7"/><line class="curve2" stroke-dasharray="5 4" x1="133.5" y1="213.6" x2="166.5" y2="26.4"/><circle class="dot3" cx="150" cy="120" r="4"/><text class="ink" x="197.5" y="136" font-size="12" text-anchor="middle">radius r</text><text class="ink" x="128" y="178" font-size="12" text-anchor="end">diameter 2r</text><text class="ink" x="180" y="108" font-size="12" text-anchor="start">60°</text><text class="ink" x="265" y="60" font-size="12" text-anchor="start">60° sector: 1/6 of the area</text></svg>
  <figcaption>The radius runs from the centre to the circle, the diameter from one side to the other through the centre. A 60° sector is 60 / 360 = 1/6 of a full turn; its area and its arc length are both 1/6 of the circle's.</figcaption>
</figure>

**Arcs and sectors.** A sector with a central angle of $\theta$ degrees is
$\frac{\theta}{360}$ of a full turn:

$$
\text{arc} = \frac{\theta}{360} \cdot 2\pi r \qquad \text{sector area} = \frac{\theta}{360} \cdot \pi r^2
$$

For $r = 6$ and $\theta = 60°$ the arc is $2\pi$ and the sector area $6\pi$.
In Trigonometry we will measure angles by arc length instead of degrees
(radians).

## Solids

| Solid | Volume | Surface area |
|---|---|---|
| cube, side $a$ | $a^3$ | $6a^2$ |
| rectangular box $a \times b \times c$ | $abc$ | $2(ab + bc + ca)$ |
| cylinder, radius $r$, height $h$ | $\pi r^2 h$ | $2\pi r^2 + 2\pi r h$ |
| sphere, radius $r$ | $\frac{4}{3} \pi r^3$ | $4 \pi r^2$ |
| cone | $\frac{1}{3} \pi r^2 h$ | |

The volume of a prism or a cylinder is **base area times height**; a cone
is one third of the cylinder with the same base. A $2 \times 3 \times 4$
box has volume $24$ and surface $2(6 + 12 + 8) = 52$. A cylinder with
radius $3$ and height $10$ has volume $90\pi \approx 282.7$.

**Scale.** If all lengths are multiplied by $k$, area is multiplied by
$k^2$ and volume by $k^3$. A cube whose side doubles has $4$ times the
surface and $8$ times the volume. That is why large animals have
disproportionately thick legs: weight grows with $k^3$, bone cross-section
with $k^2$.

## Geometry in machine learning

**Distance everywhere.** $k$-nearest neighbours, clustering (k-means) and
recommender systems look at distances between examples. The distance
between two examples with a hundred features is a Pythagoras with a hundred
terms: $\sqrt{\Delta_1^2 + \dots + \Delta_{100}^2}$.

**Angle and similarity.** How similar two documents or two words are is
often measured by the angle between them: a small angle means similar. The
calculation comes with Trigonometry and the dot product in the Advanced Mathematics module.

**IoU.** An object detection model predicts a box in an image. How good the
prediction is gets measured by the **ratio of the intersection area to the
union area** of the true box and the predicted box:

$$
\text{IoU} = \frac{\text{intersection area}}{\text{union area}}
$$

<figure class="fig">
<svg viewBox="0 0 440 244" width="440"><rect class="curve" fill="none" stroke-width="2" x="90" y="68" width="176" height="132"/><rect class="curve2" fill="none" stroke-width="2" stroke-dasharray="6 4" x="134" y="24" width="176" height="132"/><rect class="dot3" opacity="0.4" x="134" y="68" width="132" height="88"/><text class="ink" x="94" y="192" font-size="12" text-anchor="start">true box</text><text class="ink" x="306" y="16" font-size="12" text-anchor="end">prediction</text><text class="ink" x="200.0" y="117" font-size="12" text-anchor="middle">intersection 6</text><text class="ink" x="220" y="230" font-size="14" text-anchor="middle">IoU = 6 / 18 = 1/3</text></svg>
  <figcaption>The true box is 4 × 3 and the prediction 4 × 3, both 12 square units. The overlap is 3 × 2 = 6. The union is 12 + 12 − 6 = 18; the shared region is subtracted once so it is not counted twice. IoU = 6 / 18 = 1/3.</figcaption>
</figure>

An IoU of $1$ means the boxes coincide, $0$ that they do not overlap at
all. In practice anything above $0.5$ is usually counted as a "correct
detection".

**An image is a grid.** A picture is a rectangle of pixels; a
$224 \times 224$ image has $50{,}176$ pixels. Convolutional networks move
across this grid with small squares.

## Common mistakes

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Wrong</h4>
      <p>$a + b = c$ (in a right triangle)</p>
      <p>triangle area $t \cdot h$</p>
      <p>disc area $2\pi r$</p>
      <p>length $\times 2$ ⇒ volume $\times 2$</p>
    </div>
    <div class="ok">
      <h4>Right</h4>
      <p>$a^2 + b^2 = c^2$</p>
      <p>$\dfrac{1}{2} t h$</p>
      <p>area $\pi r^2$, circumference $2\pi r$</p>
      <p>volume $\times 2^3 = 8$</p>
    </div>
  </div>
  <figcaption>Pythagoras works with squares; area grows with the square of length, volume with its cube.</figcaption>
</figure>

- **Taking the slanted side as the height.** The height is measured at
  right angles to the base.
- **Picking the wrong hypotenuse.** The hypotenuse is the longest side,
  opposite the right angle; it is the $c$ in $a^2 + b^2 = c^2$.

## Summary

- Angles in degrees; complementary $90°$, supplementary $180°$; vertical
  angles are equal.
- A triangle's interior angles add up to $180°$; each side is shorter than
  the sum of the other two.
- In a right triangle $a^2 + b^2 = c^2$; the converse holds; the distance
  formula comes from here.
- Similar shapes have proportional sides; the $45$-$45$-$90$ and
  $30$-$60$-$90$ triangles are $1 : 1 : \sqrt{2}$ and $1 : \sqrt{3} : 2$.
- Areas: rectangle $ab$, triangle $\frac{1}{2} t h$, trapezoid
  $\frac{a + c}{2} h$, disc $\pi r^2$; circumference $2\pi r$.
- Volume: prism and cylinder base times height, sphere
  $\frac{4}{3}\pi r^3$; under scaling area goes with $k^2$, volume with
  $k^3$.
- Distance, angle and IoU are the geometric tools of machine learning.
