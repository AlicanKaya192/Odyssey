# Partial Derivatives and the Gradient

So far we have worked with functions of a single input: one weight, one
loss. A real model has thousands, even billions, of weights, and the loss
depends on all of them at once. The answer to "which weight should I push
which way to reduce the loss?" is not a single derivative but a vector
made of one derivative per weight: the **gradient**.

In this section we will look at functions of several variables, the
partial derivative, the gradient, and why the gradient points in the
"direction of steepest ascent".

Prerequisite: the Derivative Rules section, and the Vectors and Dot
Product sections of linear algebra.

## Functions of several variables

$f(x, y) = x^2 + 2y^2$ takes two inputs and gives one number. Its graph is
a surface: above each point $(x, y)$ there is a point at height
$f(x, y)$. The most practical way to show this surface on paper is the
**level curves** of maps: curves joining the points where $f$ takes the
same value.

<figure class="fig">
<svg viewBox="0 0 420 322" width="420"><line class="grid" x1="60.0" y1="270.0" x2="60.0" y2="20.0"/><line class="grid" x1="110.0" y1="270.0" x2="110.0" y2="20.0"/><line class="grid" x1="160.0" y1="270.0" x2="160.0" y2="20.0"/><line class="grid" x1="210.0" y1="270.0" x2="210.0" y2="20.0"/><line class="grid" x1="260.0" y1="270.0" x2="260.0" y2="20.0"/><line class="grid" x1="310.0" y1="270.0" x2="310.0" y2="20.0"/><line class="grid" x1="360.0" y1="270.0" x2="360.0" y2="20.0"/><line class="grid" x1="40.0" y1="245.0" x2="380.0" y2="245.0"/><line class="grid" x1="40.0" y1="195.0" x2="380.0" y2="195.0"/><line class="grid" x1="40.0" y1="145.0" x2="380.0" y2="145.0"/><line class="grid" x1="40.0" y1="95.0" x2="380.0" y2="95.0"/><line class="grid" x1="40.0" y1="45.0" x2="380.0" y2="45.0"/><line class="line" x1="40.0" y1="145.0" x2="380.0" y2="145.0"/><line class="line" x1="210.0" y1="270.0" x2="210.0" y2="20.0"/><text class="dim" x="60.0" y="158.0" font-size="9" text-anchor="middle">−3</text><text class="dim" x="110.0" y="158.0" font-size="9" text-anchor="middle">−2</text><text class="dim" x="160.0" y="158.0" font-size="9" text-anchor="middle">−1</text><text class="dim" x="260.0" y="158.0" font-size="9" text-anchor="middle">1</text><text class="dim" x="310.0" y="158.0" font-size="9" text-anchor="middle">2</text><text class="dim" x="360.0" y="158.0" font-size="9" text-anchor="middle">3</text><text class="dim" x="205.0" y="248.0" font-size="9" text-anchor="end">−2</text><text class="dim" x="205.0" y="198.0" font-size="9" text-anchor="end">−1</text><text class="dim" x="205.0" y="98.0" font-size="9" text-anchor="end">1</text><text class="dim" x="205.0" y="48.0" font-size="9" text-anchor="end">2</text><polyline class="curve" fill="none" points="260.0,145.0 259.7,141.3 258.9,137.6 257.6,134.1 255.7,130.6 253.3,127.3 250.5,124.2 247.2,121.3 243.5,118.7 239.4,116.4 235.0,114.4 230.3,112.7 225.5,111.4 220.4,110.4 215.2,109.8 210.0,109.6 204.8,109.8 199.6,110.4 194.5,111.4 189.7,112.7 185.0,114.4 180.6,116.4 176.5,118.7 172.8,121.3 169.5,124.2 166.7,127.3 164.3,130.6 162.4,134.1 161.1,137.6 160.3,141.3 160.0,145.0 160.3,148.7 161.1,152.4 162.4,155.9 164.3,159.4 166.7,162.7 169.5,165.8 172.8,168.7 176.5,171.3 180.6,173.6 185.0,175.6 189.7,177.3 194.5,178.6 199.6,179.6 204.8,180.2 210.0,180.4 215.2,180.2 220.4,179.6 225.5,178.6 230.3,177.3 235.0,175.6 239.4,173.6 243.5,171.3 247.2,168.7 250.5,165.8 253.3,162.7 255.7,159.4 257.6,155.9 258.9,152.4 259.7,148.7 260.0,145.0"/><polyline class="curve" fill="none" points="280.7,145.0 280.3,139.8 279.2,134.6 277.2,129.5 274.6,124.7 271.2,120.0 267.2,115.6 262.5,111.5 257.3,107.8 251.6,104.5 245.4,101.7 238.8,99.3 231.9,97.4 224.7,96.1 217.4,95.3 210.0,95.0 202.6,95.3 195.3,96.1 188.1,97.4 181.2,99.3 174.6,101.7 168.4,104.5 162.7,107.8 157.5,111.5 152.8,115.6 148.8,120.0 145.4,124.7 142.8,129.5 140.8,134.6 139.7,139.8 139.3,145.0 139.7,150.2 140.8,155.4 142.8,160.5 145.4,165.3 148.8,170.0 152.8,174.4 157.5,178.5 162.7,182.2 168.4,185.5 174.6,188.3 181.2,190.7 188.1,192.6 195.3,193.9 202.6,194.7 210.0,195.0 217.4,194.7 224.7,193.9 231.9,192.6 238.8,190.7 245.4,188.3 251.6,185.5 257.3,182.2 262.5,178.5 267.2,174.4 271.2,170.0 274.6,165.3 277.2,160.5 279.2,155.4 280.3,150.2 280.7,145.0"/><polyline class="curve" fill="none" points="310.0,145.0 309.5,137.6 307.8,130.3 305.1,123.1 301.4,116.2 296.6,109.6 290.9,103.4 284.3,97.7 276.9,92.5 268.8,87.8 260.0,83.8 250.7,80.4 240.9,77.8 230.8,75.8 220.5,74.7 210.0,74.3 199.5,74.7 189.2,75.8 179.1,77.8 169.3,80.4 160.0,83.8 151.2,87.8 143.1,92.5 135.7,97.7 129.1,103.4 123.4,109.6 118.6,116.2 114.9,123.1 112.2,130.3 110.5,137.6 110.0,145.0 110.5,152.4 112.2,159.7 114.9,166.9 118.6,173.8 123.4,180.4 129.1,186.6 135.7,192.3 143.1,197.5 151.2,202.2 160.0,206.2 169.3,209.6 179.1,212.2 189.2,214.2 199.5,215.3 210.0,215.7 220.5,215.3 230.8,214.2 240.9,212.2 250.7,209.6 260.0,206.2 268.8,202.2 276.9,197.5 284.3,192.3 290.9,186.6 296.6,180.4 301.4,173.8 305.1,166.9 307.8,159.7 309.5,152.4 310.0,145.0"/><polyline class="curve" fill="none" points="332.5,145.0 331.8,135.9 329.8,127.0 326.5,118.2 321.9,109.8 316.1,101.7 309.1,94.1 301.0,87.1 292.0,80.6 282.0,74.9 271.2,70.0 259.8,65.9 247.8,62.6 235.5,60.3 222.8,58.9 210.0,58.4 197.2,58.9 184.5,60.3 172.2,62.6 160.2,65.9 148.8,70.0 138.0,74.9 128.0,80.6 119.0,87.1 110.9,94.1 103.9,101.7 98.1,109.8 93.5,118.2 90.2,127.0 88.2,135.9 87.5,145.0 88.2,154.1 90.2,163.0 93.5,171.8 98.1,180.2 103.9,188.3 110.9,195.9 119.0,202.9 128.0,209.4 138.0,215.1 148.8,220.0 160.2,224.1 172.2,227.4 184.5,229.7 197.2,231.1 210.0,231.6 222.8,231.1 235.5,229.7 247.8,227.4 259.8,224.1 271.2,220.0 282.0,215.1 292.0,209.4 301.0,202.9 309.1,195.9 316.1,188.3 321.9,180.2 326.5,171.8 329.8,163.0 331.8,154.1 332.5,145.0"/><line class="curve2" x1="310.0" y1="145.0" x2="338.6" y2="145.0"/><polygon class="dot2" points="345.0,145.0 337.7,148.3 337.7,141.7"/><circle class="dot2" cx="310.0" cy="145.0" r="3.5"/><line class="curve2" x1="310.0" y1="95.0" x2="330.2" y2="74.8"/><polygon class="dot2" points="334.7,70.3 331.8,77.8 327.2,73.2"/><circle class="dot2" cx="310.0" cy="95.0" r="3.5"/><line class="curve2" x1="139.3" y1="95.0" x2="122.8" y2="71.6"/><polygon class="dot2" points="119.1,66.4 126.0,70.5 120.6,74.2"/><circle class="dot2" cx="139.3" cy="95.0" r="3.5"/><line class="curve2" x1="210.0" y1="215.7" x2="210.0" y2="244.3"/><polygon class="dot2" points="210.0,250.7 206.7,243.4 213.3,243.4"/><circle class="dot2" cx="210.0" cy="215.7" r="3.5"/><line class="curve2" x1="110.0" y1="195.0" x2="89.8" y2="215.2"/><polygon class="dot2" points="85.3,219.7 88.2,212.2 92.8,216.8"/><circle class="dot2" cx="110.0" cy="195.0" r="3.5"/><text class="ink" x="45.0" y="35.0" font-size="12" text-anchor="start">f(x, y) = x² + 2y²</text><text class="dim" x="210" y="294" font-size="11" text-anchor="middle">level curves f = 1, 2, 4, 6</text><text class="dim" x="210" y="312" font-size="11" text-anchor="middle">gradient: steepest ascent, perpendicular to the curve</text></svg>
  <figcaption>The level curves of the surface f(x, y) = x² + 2y²: nested ellipses, with the smallest value at the centre. The orange arrows are the gradient at a few points; each is perpendicular to the curve through its point and faces outwards, uphill.</figcaption>
</figure>

Where the curves are close together the surface is steep; where they are
far apart it is gentle.

## The partial derivative

With more than one variable we take the derivative **with respect to one
variable**, holding the others as fixed numbers. This is called the
**partial derivative** and is written with $\partial$ ("partial d"):

$$
\frac{\partial f}{\partial x} = \lim_{h \to 0} \frac{f(x + h, y) - f(x, y)}{h}
$$

Example: $f(x, y) = x^2 y + 3y$.

- With respect to $x$ ($y$ fixed): $\dfrac{\partial f}{\partial x} = 2xy$. ($3y$ is a constant, derivative $0$.)
- With respect to $y$ ($x$ fixed): $\dfrac{\partial f}{\partial y} = x^2 + 3$.

**Its geometric meaning.** Holding $y$ fixed means cutting the surface
with a plane on which $y$ is constant; the cut is a curve in one
variable. $\frac{\partial f}{\partial x}$ is the slope of that curve: how
much does the height change for one step east?

Short forms: $f_x$, $f_y$ or $\partial_x f$.

## The gradient

Collect all the partial derivatives in a vector:

$$
\nabla f = \left( \frac{\partial f}{\partial x}, \ \frac{\partial f}{\partial y} \right)
$$

$\nabla$ is read "nabla". With $n$ variables the gradient is a vector
with $n$ components. Example: for $f = x^2 + 2y^2$, $\nabla f = (2x, 4y)$;
at the point $(1, 1)$ it is $(2, 4)$.

**The gradient is a vector that depends on the point:** it is different
at every point. The arrows in the figure are exactly this: at each point
the gradient of that point is drawn.

## Why does the gradient point the steepest way?

Take a small step from $(x, y)$ in the direction of a unit vector
$\mathbf{u}$. The rate of change of the height is the **directional
derivative**:

$$
D_{\mathbf{u}} f = \nabla f \cdot \mathbf{u} = \lVert \nabla f \rVert \cos \theta
$$

($\theta$ is the angle between $\nabla f$ and $\mathbf{u}$; the formula
from the dot product section.)

<figure class="fig">
<svg viewBox="0 0 400 299" width="400"><line class="grid" x1="40.0" y1="245.0" x2="40.0" y2="20.0"/><line class="grid" x1="77.5" y1="245.0" x2="77.5" y2="20.0"/><line class="grid" x1="115.0" y1="245.0" x2="115.0" y2="20.0"/><line class="grid" x1="152.5" y1="245.0" x2="152.5" y2="20.0"/><line class="grid" x1="190.0" y1="245.0" x2="190.0" y2="20.0"/><line class="grid" x1="227.5" y1="245.0" x2="227.5" y2="20.0"/><line class="grid" x1="265.0" y1="245.0" x2="265.0" y2="20.0"/><line class="grid" x1="302.5" y1="245.0" x2="302.5" y2="20.0"/><line class="grid" x1="340.0" y1="245.0" x2="340.0" y2="20.0"/><line class="grid" x1="40.0" y1="245.0" x2="340.0" y2="245.0"/><line class="grid" x1="40.0" y1="207.5" x2="340.0" y2="207.5"/><line class="grid" x1="40.0" y1="170.0" x2="340.0" y2="170.0"/><line class="grid" x1="40.0" y1="132.5" x2="340.0" y2="132.5"/><line class="grid" x1="40.0" y1="95.0" x2="340.0" y2="95.0"/><line class="grid" x1="40.0" y1="57.5" x2="340.0" y2="57.5"/><line class="grid" x1="40.0" y1="20.0" x2="340.0" y2="20.0"/><line class="curve" x1="77.5" y1="207.5" x2="294.6" y2="98.9"/><polygon class="dot" points="302.5,95.0 295.5,103.5 291.5,95.5"/><line class="curve2" x1="77.5" y1="207.5" x2="119.3" y2="95.5"/><polygon class="dot2" points="122.1,88.0 122.7,98.0 115.1,95.1"/><polyline class="curve3" fill="none" points="117.7,187.4 117.0,185.9 116.1,184.4 115.2,183.0 114.3,181.6 113.3,180.2 112.2,178.9 111.1,177.6 110.0,176.4 108.8,175.2 107.6,174.0 106.3,172.9 105.0,171.9 103.6,170.9 102.2,169.9 100.8,169.0 99.4,168.2 97.9,167.4 96.3,166.6 94.8,166.0 93.2,165.3"/><text class="ink" x="117.6" y="166.9" font-size="13" text-anchor="middle">θ</text><line class="curve3" stroke-dasharray="5 4" x1="122.1" y1="88.0" x2="160.9" y2="165.8"/><text class="ink" x="310.5" y="99.0" font-size="14" text-anchor="start">∇f</text><text class="ink" x="116.1" y="82.0" font-size="12" text-anchor="end">u (unit direction)</text><text class="ink" x="190" y="269" font-size="12" text-anchor="middle">rate of change along u = ‖∇f‖ cos θ</text><text class="dim" x="190" y="289" font-size="10.5" text-anchor="middle">θ = 0: fastest increase; θ = 90°: no change; θ = 180°: fastest decrease</text></svg>
  <figcaption>The directional derivative is the length of the projection of u onto the gradient. It grows as the angle shrinks; when u faces the same way as the gradient it reaches its largest value, ‖∇f‖.</figcaption>
</figure>

Since $\cos \theta$ is at most $1$:

- **$\theta = 0$**: $\mathbf{u}$ along the gradient; the increase is fastest, at rate $\lVert \nabla f \rVert$.
- **$\theta = 180°$**: against the gradient; the **fastest decrease**. The direction gradient descent takes.
- **$\theta = 90°$**: no change; this direction runs along the level curve. That is why the gradient is **perpendicular** to the level curves.

## Where the gradient is zero

In one variable $f' = 0$ meant a horizontal tangent; with several
variables $\nabla f = \mathbf{0}$ means a **horizontal tangent plane**.
Such a point can be one of three kinds:

| Point | Example | Looks like |
|---|---|---|
| local minimum | $x^2 + y^2$ at $(0, 0)$ | a bowl |
| local maximum | $-x^2 - y^2$ at $(0, 0)$ | a peak |
| **saddle point** | $x^2 - y^2$ at $(0, 0)$ | a bowl one way, a cap the other |

A saddle point is something that does not exist in one variable: like a
horse's saddle, a bottom in the $x$ direction and a top in the $y$
direction. The second partial derivatives tell which it is.

**Second partial derivatives.** $f_{xx} = \frac{\partial^2 f}{\partial x^2}$,
$f_{yy}$ and the mixed derivative $f_{xy} = \frac{\partial^2 f}{\partial x \, \partial y}$.
For well-behaved functions the order does not matter: $f_{xy} = f_{yx}$.
The matrix they form (the Hessian) is the subject of the next section.

## The gradient in machine learning

**The gradient of a linear model.** $\hat{y} = w_1 x_1 + w_2 x_2 + b$,
with loss $L = (\hat{y} - y)^2$ on one example. By the chain rule, with
respect to each weight:

$$
\frac{\partial L}{\partial w_j} = 2(\hat{y} - y) \, x_j, \qquad \frac{\partial L}{\partial b} = 2(\hat{y} - y)
$$

As a vector: $\nabla_{\mathbf{w}} L = 2(\hat{y} - y) \, \mathbf{x}$. If
the error is large and the feature is large, that weight's gradient is
large too.

**Gradient descent.** To reduce the loss, take a step in the direction of
fastest decrease, against the gradient:

$$
\mathbf{w} \leftarrow \mathbf{w} - \eta \, \nabla L(\mathbf{w})
$$

The same idea as $w \leftarrow w - \eta L'(w)$ in one variable; now every
weight is updated at the same time with its own partial derivative. We
will see it in detail in the Gradient Descent section.

**Feature scaling.** The ellipses in the figure were long because the
function is steeper in the $y$ direction ($2y^2$). If the features have
very different scales, the level curves of the loss become very flat
ellipses; the gradient points at the side wall instead of the centre,
and the descent zigzags. Bringing the features to the same scale makes
the curves closer to circles.

## Common mistakes

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Wrong</h4>
      <p>$\dfrac{\partial}{\partial x}(x^2 y) = 2x$</p>
      <p>$\dfrac{\partial}{\partial x}(3y) = 3$</p>
      <p>The gradient is a number</p>
      <p>The gradient points to the minimum</p>
    </div>
    <div class="ok">
      <h4>Right</h4>
      <p>$2xy$: $y$ stays as a constant factor</p>
      <p>$0$: if $y$ is fixed, so is $3y$</p>
      <p>A vector with one component per variable</p>
      <p>It points to the fastest increase; descent goes the other way</p>
    </div>
  </div>
  <figcaption>In a partial derivative the other variables behave like numbers: they stay as factors, and on their own their derivative is zero.</figcaption>
</figure>

## Summary

- The graph of a function of several variables is a surface; level curves are its map.
- Partial derivative: the derivative taken with the other variables held fixed, $\frac{\partial f}{\partial x}$.
- The gradient $\nabla f = (f_x, f_y, \ldots)$: the vector of partial derivatives.
- Directional derivative $D_{\mathbf{u}} f = \nabla f \cdot \mathbf{u}$; largest along the gradient, with value $\lVert \nabla f \rVert$.
- The gradient is the direction of steepest ascent and perpendicular to the level curves; its opposite is steepest descent.
- $\nabla f = \mathbf{0}$: a minimum, a maximum or a saddle point.
- Linear model: $\nabla_{\mathbf{w}} L = 2(\hat{y} - y)\mathbf{x}$; gradient descent $\mathbf{w} \leftarrow \mathbf{w} - \eta \nabla L$.
