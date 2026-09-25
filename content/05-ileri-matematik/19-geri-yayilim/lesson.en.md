# Backpropagation: Derivatives in a Neural Network

Gradient descent needs, at every step, the derivative of the loss with
respect to **all** the weights. In a network with millions of weights,
taking a numerical derivative for each weight separately would mean
millions of forward passes per step; impossible. **Backpropagation**
computes all these derivatives in a single backward pass, at roughly the
cost of a forward pass. It is not new mathematics: it is the chain rule
applied cleverly, from the end back to the start.

In this section we will look at computational graphs, local derivatives,
backpropagation step by step in a small network, and the problems that
appear in deep networks.

Prerequisite: the Derivative Rules and the Chain Rule, Jacobian and
Hessian, and Gradient Descent sections.

## The computational graph

Every complicated expression is a sequence of simple operations. Drawing
these operations as nodes and the flow of data between them as arrows
gives a **computational graph**. For $f = (x + y) \cdot z$ the intermediate
value is $q = x + y$, then $f = q \cdot z$.

<figure class="fig">
<svg viewBox="0 0 420 330" width="420"><circle class="box" cx="50" cy="50" r="20"/><text class="ink" x="50" y="55" font-size="14" text-anchor="middle">x</text><circle class="box" cx="50" cy="150" r="20"/><text class="ink" x="50" y="155" font-size="14" text-anchor="middle">y</text><circle class="box" cx="50" cy="250" r="20"/><text class="ink" x="50" y="255" font-size="14" text-anchor="middle">z</text><circle class="dot3" opacity="0.35" cx="200" cy="100" r="20"/><text class="ink" x="200" y="105" font-size="14" text-anchor="middle">+</text><circle class="dot2" opacity="0.35" cx="340" cy="175" r="20"/><text class="ink" x="340" y="180" font-size="14" text-anchor="middle">×</text><line class="line" x1="69.0" y1="56.3" x2="177.2" y2="92.4"/><polygon class="dim" points="181.0,93.7 173.1,94.7 175.3,88.1"/><line class="line" x1="69.0" y1="143.7" x2="177.2" y2="107.6"/><polygon class="dim" points="181.0,106.3 175.3,111.9 173.1,105.3"/><line class="line" x1="217.6" y1="109.4" x2="318.8" y2="163.7"/><polygon class="dim" points="322.4,165.6 314.4,165.2 317.7,159.1"/><line class="line" x1="69.4" y1="245.0" x2="316.8" y2="181.0"/><polygon class="dim" points="320.6,180.0 314.5,185.2 312.8,178.4"/><text class="ink" x="400" y="180" font-size="15" text-anchor="middle">f</text><line class="line" x1="362" y1="175" x2="390" y2="175"/><text class="ink" x="110" y="50" font-size="12" text-anchor="middle">−2</text><text class="dot2" x="110" y="66" font-size="12" text-anchor="middle">−4</text><text class="ink" x="118" y="150" font-size="12" text-anchor="middle">5</text><text class="dot2" x="118" y="166" font-size="12" text-anchor="middle">−4</text><text class="ink" x="250" y="154" font-size="12" text-anchor="middle">q = 3</text><text class="dot2" x="250" y="170" font-size="12" text-anchor="middle">−4</text><text class="ink" x="190" y="226" font-size="12" text-anchor="middle">−4</text><text class="dot2" x="190" y="242" font-size="12" text-anchor="middle">3</text><text class="ink" x="400" y="153" font-size="12" text-anchor="middle">−12</text><text class="dot2" x="400" y="169" font-size="12" text-anchor="middle"></text><text class="dot2" x="400" y="205" font-size="12" text-anchor="middle">1</text><text class="ink" x="200" y="300" font-size="11" text-anchor="middle">forward pass: values (top)</text><text class="dot2" x="200" y="318" font-size="11" text-anchor="middle">backward pass: ∂f/∂(that node) (bottom, orange)</text></svg>
  <figcaption>x = −2, y = 5, z = −4. The forward pass computes the values from left to right: q = 3, f = −12. The backward pass carries derivatives from right to left: it starts with ∂f/∂f = 1, the multiplication node gives ∂f/∂q = z = −4 and ∂f/∂z = q = 3, and the addition node passes −4 unchanged to both x and y.</figcaption>
</figure>

**Two passes.**

1. **Forward:** from the inputs to the output, compute and store the value of every node.
2. **Backward:** start at the output with $\frac{\partial f}{\partial f} = 1$; at each node multiply the incoming derivative (the **upstream gradient**) by the node's **local derivative** and pass it on to its inputs.

The chain rule itself:

$$
\frac{\partial f}{\partial x} = \frac{\partial f}{\partial q} \cdot \frac{\partial q}{\partial x} = (-4) \cdot 1 = -4
$$

## How the gates behave

Each node only has to know its own local derivative. Commonly used nodes
work by surprisingly simple rules:

| Node | Forward | Backward (incoming gradient $g$) |
|---|---|---|
| addition $a + b$ | add | pass $g$ **unchanged** to both inputs |
| multiplication $a \cdot b$ | multiply | $g \cdot b$ to $a$, $g \cdot a$ to $b$: **swap** the inputs |
| $\max(a, b)$ | pick the larger | send $g$ **only to the larger**, $0$ to the other |
| ReLU | $\max(0, z)$ | $g$ if $z > 0$, otherwise $0$ |
| sigmoid | $\sigma(z)$ | $g \cdot \sigma(1 - \sigma)$ |
| **branching** (a value used in two places) | copy | **add up** the gradients from the two branches |

The last row matters: if $x$ affects both $a$ and $b$, the derivative of
$x$ is the sum of the two roads. In the multivariable chain rule we said
"roads add up".

## Backpropagation in a small network

One input, two hidden neurons (ReLU), one output:

$$
\begin{aligned}
\mathbf{z} &= W_1 x + \mathbf{b}_1, & \mathbf{a} &= \mathrm{ReLU}(\mathbf{z}) \\
\hat{y} &= \mathbf{w}_2 \cdot \mathbf{a} + b_2, & L &= \tfrac{1}{2}(\hat{y} - y)^2
\end{aligned}
$$

<figure class="fig">
<svg viewBox="0 0 440 290" width="440"><circle class="box" cx="70" cy="120" r="22"/><text class="ink" x="70" y="125" font-size="14" text-anchor="middle">x</text><circle class="box" cx="220" cy="60" r="22"/><text class="ink" x="220" y="65" font-size="14" text-anchor="middle">h₁</text><circle class="box" cx="220" cy="180" r="22"/><text class="ink" x="220" y="185" font-size="14" text-anchor="middle">h₂</text><circle class="box" cx="370" cy="120" r="22"/><text class="ink" x="370" y="125" font-size="14" text-anchor="middle">ŷ</text><line class="line" x1="90.4" y1="111.8" x2="195.9" y2="69.7"/><polygon class="dim" points="199.6,68.2 194.2,74.1 191.6,67.6"/><line class="line" x1="90.4" y1="128.2" x2="195.9" y2="170.3"/><polygon class="dim" points="199.6,171.8 191.6,172.4 194.2,165.9"/><line class="line" x1="240.4" y1="68.2" x2="345.9" y2="110.3"/><polygon class="dim" points="349.6,111.8 341.6,112.4 344.2,105.9"/><line class="line" x1="240.4" y1="171.8" x2="345.9" y2="129.7"/><polygon class="dim" points="349.6,128.2 344.2,134.1 341.6,127.6"/><text class="dim" x="138" y="78" font-size="11" text-anchor="middle">W₁₁ = 1</text><text class="dim" x="138" y="172" font-size="11" text-anchor="middle">W₁₂ = −1</text><text class="dim" x="300" y="78" font-size="11" text-anchor="middle">w₂₁ = 2</text><text class="dim" x="300" y="172" font-size="11" text-anchor="middle">w₂₂ = −1</text><text class="dim" x="220" y="222" font-size="10.5" text-anchor="middle">b₁₂ = 2</text><text class="ink" x="70" y="26" font-size="11" text-anchor="middle">input</text><text class="ink" x="220" y="20" font-size="11" text-anchor="middle">hidden layer (ReLU)</text><text class="ink" x="370" y="26" font-size="11" text-anchor="middle">output</text><text class="ink" x="220" y="256" font-size="11" text-anchor="middle">forward: z = (1, 1), a = (1, 1), ŷ = 1; target y = 3, L = 2</text><text class="dot2" x="220" y="276" font-size="11" text-anchor="middle">backward: ∂L/∂ŷ = −2, ∂L/∂a = (−4, 2), ∂L/∂w₂ = (−2, −2)</text></svg>
  <figcaption>x = 1, W₁ = (1, −1), b₁ = (0, 2), w₂ = (2, −1), b₂ = 0, target y = 3. The top line holds the values of the forward pass, the orange line the derivatives carried by the backward pass.</figcaption>
</figure>

**Forward.** $\mathbf{z} = (1, \ -1 + 2) = (1, 1)$, $\mathbf{a} = (1, 1)$,
$\hat{y} = 2 - 1 = 1$, $L = \frac{1}{2}(1 - 3)^2 = 2$.

**Backward**, from the end to the start:

| Step | Formula | Value |
|---|---|---|
| output | $\frac{\partial L}{\partial \hat{y}} = \hat{y} - y$ | $-2$ |
| output weights | $\frac{\partial L}{\partial \mathbf{w}_2} = \frac{\partial L}{\partial \hat{y}} \, \mathbf{a}$ | $(-2, -2)$ |
| hidden outputs | $\frac{\partial L}{\partial \mathbf{a}} = \frac{\partial L}{\partial \hat{y}} \, \mathbf{w}_2$ | $(-4, 2)$ |
| through ReLU | $\frac{\partial L}{\partial \mathbf{z}} = \frac{\partial L}{\partial \mathbf{a}} \odot \mathrm{ReLU}'(\mathbf{z})$ | $(-4, 2)$ |
| first layer weights | $\frac{\partial L}{\partial W_1} = \frac{\partial L}{\partial \mathbf{z}} \, x$ | $(-4, 2)$ |

($\odot$ is element-wise multiplication; both $z$'s are positive, so ReLU
let the gradient through unchanged.) Every layer has the same two moves:
**carry the gradient back through the transpose of the weights** and
**multiply by the input to get the weights' derivative**. The recipe does
not change however many layers there are.

## Why is it so efficient?

**Reverse mode.** Because we carry derivatives from the output towards
the input, a single backward pass gives the derivative of a single
output (the loss) with respect to **all** inputs and weights. Its cost is
roughly a few times that of a forward pass. Taking numerical derivatives
by wiggling the weights one by one would need as many forward passes as
there are weights.

**The memory cost.** The backward pass needs the intermediate values of
the forward pass ($\mathbf{z}$, $\mathbf{a}$) for the local derivatives;
they are all stored. That is why large models need far more memory for
training than for inference.

**Automatic differentiation.** Deep learning libraries record the
computational graph themselves while the forward pass is written, and
perform the backward pass automatically with these rules. The user only
writes the model and the loss; the `backward` call fills in the table of
this section for millions of nodes.

**Verification.** A hand-written backward pass is tested with gradient
checking: wiggle a few weights by $\pm h$ and compare the central
difference with the derivative from backpropagation.

## Problems in deep networks

A gradient passing through $n$ layers is multiplied by $n$ local
derivatives. If the factors are usually below $1$ the gradient
**vanishes**; if above, it **explodes**:

- With sigmoids each factor is at most $0.25$: over $10$ layers $0.25^{10} \approx 10^{-6}$.
- If the weights are a little large, even a factor of $1.1$ per layer gives $1.1^{50} \approx 117$ over $50$ layers.

**Remedies.**

- Activations such as **ReLU** whose derivative is $1$ in the active region.
- **Careful initialisation** (Xavier, He): starting the weights at a scale where the factors stay around $1$ on average.
- **Residual connections:** $\mathbf{a}_{k+1} = \mathbf{a}_k + F(\mathbf{a}_k)$. The derivative is $I + J_F$; thanks to the identity matrix there is a "highway" the gradient can pass through.
- **Normalisation layers** and **gradient clipping**.

## Common mistakes

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Wrong</h4>
      <p>Multiplying by the weight itself in the backward pass</p>
      <p>Taking only one gradient at a branch</p>
      <p>$\max$ sends the gradient to both inputs</p>
      <p>Backpropagation is a new derivative rule</p>
    </div>
    <div class="ok">
      <h4>Right</h4>
      <p>By its transpose: $W^\mathsf{T} \frac{\partial L}{\partial \mathbf{z}}$</p>
      <p>Add up what comes from the branches</p>
      <p>Only to the chosen input</p>
      <p>The chain rule applied from the end back</p>
    </div>
  </div>
  <figcaption>Each node only knows its own local derivative; backpropagation combines them with the chain rule.</figcaption>
</figure>

## Summary

- Computational graph: nodes made of simple operations; the forward pass computes and stores the values.
- The backward pass starts with $\frac{\partial L}{\partial L} = 1$; at each node, upstream gradient × local derivative.
- Addition distributes, multiplication swaps, max routes, branching adds up.
- Per layer: $\frac{\partial L}{\partial \mathbf{x}} = W^\mathsf{T}\frac{\partial L}{\partial \mathbf{z}}$, $\frac{\partial L}{\partial W} = \frac{\partial L}{\partial \mathbf{z}}\mathbf{x}^\mathsf{T}$.
- One backward pass gives all derivatives (reverse mode); the cost is storing the intermediate values.
- Vanishing and exploding gradients: factors far from $1$; remedies are ReLU, good initialisation, residual connections, normalisation and clipping.
