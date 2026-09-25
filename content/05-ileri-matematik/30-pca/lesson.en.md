# Dimensionality Reduction: The Mathematics of PCA

A data set may have hundreds of features; but they are often tied to each
other and really vary in far fewer "directions". **Principal component
analysis** (PCA) finds the directions in which the data spreads most and
reduces the dimension by projecting the data onto those few directions.
This section joins the two halves of MATH 2: the covariance matrix
(statistics), and eigenvalues and eigenvectors, the SVD and orthogonal
projection (linear algebra).

Prerequisites: Eigenvalues and Eigenvectors; Singular Value Decomposition
(SVD); Covariance and Correlation; The Mathematics of Linear Regression
(orthogonal projection).

## The idea: the direction of greatest spread

<figure class="fig">
<svg viewBox="0 0 420 322" width="420"><line class="grid" x1="40.0" y1="292.0" x2="40.0" y2="20.0"/><line class="grid" x1="74.0" y1="292.0" x2="74.0" y2="20.0"/><line class="grid" x1="108.0" y1="292.0" x2="108.0" y2="20.0"/><line class="grid" x1="142.0" y1="292.0" x2="142.0" y2="20.0"/><line class="grid" x1="176.0" y1="292.0" x2="176.0" y2="20.0"/><line class="grid" x1="210.0" y1="292.0" x2="210.0" y2="20.0"/><line class="grid" x1="244.0" y1="292.0" x2="244.0" y2="20.0"/><line class="grid" x1="278.0" y1="292.0" x2="278.0" y2="20.0"/><line class="grid" x1="312.0" y1="292.0" x2="312.0" y2="20.0"/><line class="grid" x1="346.0" y1="292.0" x2="346.0" y2="20.0"/><line class="grid" x1="380.0" y1="292.0" x2="380.0" y2="20.0"/><line class="grid" x1="40.0" y1="292.0" x2="380.0" y2="292.0"/><line class="grid" x1="40.0" y1="258.0" x2="380.0" y2="258.0"/><line class="grid" x1="40.0" y1="224.0" x2="380.0" y2="224.0"/><line class="grid" x1="40.0" y1="190.0" x2="380.0" y2="190.0"/><line class="grid" x1="40.0" y1="156.0" x2="380.0" y2="156.0"/><line class="grid" x1="40.0" y1="122.0" x2="380.0" y2="122.0"/><line class="grid" x1="40.0" y1="88.0" x2="380.0" y2="88.0"/><line class="grid" x1="40.0" y1="54.0" x2="380.0" y2="54.0"/><line class="grid" x1="40.0" y1="20.0" x2="380.0" y2="20.0"/><line class="line" x1="40.0" y1="292.0" x2="380.0" y2="292.0"/><line class="line" x1="40.0" y1="292.0" x2="40.0" y2="20.0"/><text class="dim" x="108.0" y="305.0" font-size="9" text-anchor="middle">2</text><text class="dim" x="176.0" y="305.0" font-size="9" text-anchor="middle">4</text><text class="dim" x="244.0" y="305.0" font-size="9" text-anchor="middle">6</text><text class="dim" x="312.0" y="305.0" font-size="9" text-anchor="middle">8</text><text class="dim" x="35.0" y="227.0" font-size="9" text-anchor="end">2</text><text class="dim" x="35.0" y="159.0" font-size="9" text-anchor="end">4</text><text class="dim" x="35.0" y="91.0" font-size="9" text-anchor="end">6</text><circle class="dot" cx="166.8" cy="170.4" r="3.2"/><circle class="dot" cx="143.6" cy="186.8" r="3.2"/><circle class="dot" cx="204.3" cy="171.4" r="3.2"/><circle class="dot" cx="229.4" cy="143.8" r="3.2"/><circle class="dot" cx="248.8" cy="103.6" r="3.2"/><circle class="dot" cx="218.4" cy="157.5" r="3.2"/><circle class="dot" cx="183.7" cy="170.9" r="3.2"/><circle class="dot" cx="175.2" cy="180.8" r="3.2"/><circle class="dot" cx="238.0" cy="125.0" r="3.2"/><circle class="dot" cx="286.1" cy="109.6" r="3.2"/><circle class="dot" cx="223.5" cy="149.4" r="3.2"/><circle class="dot" cx="152.9" cy="191.4" r="3.2"/><circle class="dot" cx="166.4" cy="184.6" r="3.2"/><circle class="dot" cx="288.9" cy="116.9" r="3.2"/><circle class="dot" cx="211.2" cy="138.4" r="3.2"/><circle class="dot" cx="144.2" cy="226.3" r="3.2"/><circle class="dot" cx="216.8" cy="173.7" r="3.2"/><circle class="dot" cx="169.4" cy="208.4" r="3.2"/><circle class="dot" cx="173.5" cy="163.5" r="3.2"/><circle class="dot" cx="191.4" cy="175.7" r="3.2"/><circle class="dot" cx="186.7" cy="190.4" r="3.2"/><circle class="dot" cx="244.6" cy="153.0" r="3.2"/><circle class="dot" cx="203.5" cy="152.7" r="3.2"/><circle class="dot" cx="193.0" cy="187.6" r="3.2"/><circle class="dot" cx="239.4" cy="159.2" r="3.2"/><circle class="dot" cx="241.6" cy="122.4" r="3.2"/><circle class="dot" cx="147.3" cy="222.3" r="3.2"/><circle class="dot" cx="201.4" cy="168.1" r="3.2"/><circle class="dot" cx="166.4" cy="186.7" r="3.2"/><circle class="dot" cx="206.2" cy="167.0" r="3.2"/><circle class="dot" cx="153.0" cy="196.9" r="3.2"/><circle class="dot" cx="199.2" cy="138.6" r="3.2"/><circle class="dot" cx="212.8" cy="163.7" r="3.2"/><circle class="dot" cx="207.5" cy="181.3" r="3.2"/><circle class="dot" cx="179.4" cy="211.7" r="3.2"/><circle class="dot" cx="194.1" cy="170.9" r="3.2"/><circle class="dot" cx="164.5" cy="194.5" r="3.2"/><circle class="dot" cx="147.3" cy="195.0" r="3.2"/><circle class="dot" cx="224.1" cy="154.8" r="3.2"/><circle class="dot" cx="164.8" cy="196.6" r="3.2"/><circle class="dot" cx="268.5" cy="128.5" r="3.2"/><circle class="dot" cx="246.5" cy="140.2" r="3.2"/><circle class="dot" cx="119.6" cy="216.3" r="3.2"/><circle class="dot" cx="225.5" cy="152.3" r="3.2"/><circle class="dot" cx="160.0" cy="189.1" r="3.2"/><circle class="dot" cx="194.8" cy="131.1" r="3.2"/><circle class="dot" cx="207.7" cy="148.6" r="3.2"/><circle class="dot" cx="135.2" cy="237.8" r="3.2"/><circle class="dot" cx="184.4" cy="141.6" r="3.2"/><circle class="dot" cx="195.5" cy="159.6" r="3.2"/><circle class="dot" cx="261.1" cy="137.8" r="3.2"/><circle class="dot" cx="149.4" cy="181.5" r="3.2"/><circle class="dot" cx="242.7" cy="132.7" r="3.2"/><circle class="dot" cx="166.4" cy="198.0" r="3.2"/><circle class="dot" cx="200.8" cy="174.3" r="3.2"/><circle class="dot" cx="181.3" cy="194.7" r="3.2"/><circle class="dot" cx="274.1" cy="110.2" r="3.2"/><circle class="dot" cx="225.9" cy="124.9" r="3.2"/><circle class="dot" cx="321.2" cy="84.2" r="3.2"/><circle class="dot" cx="234.9" cy="130.7" r="3.2"/><line class="curve2" x1="201.7" y1="164.6" x2="277.5" y2="107.6"/><polygon class="dot2" points="284.5,102.3 279.2,111.9 273.8,104.8"/><line class="curve2" x1="60" y1="34" x2="86" y2="34"/><text class="ink" x="92" y="38" font-size="11" text-anchor="start">1st component</text><line class="curve4" x1="201.7" y1="164.6" x2="191.9" y2="151.5"/><polygon class="dot3" points="186.6,144.5 196.2,149.8 189.0,155.2"/><line class="curve4" x1="60" y1="54" x2="86" y2="54"/><text class="ink" x="92" y="58" font-size="11" text-anchor="start">2nd component</text><circle class="dot3" cx="201.7" cy="164.6" r="4.5"/><text class="dim" x="380.0" y="320.0" font-size="10" text-anchor="end">x₁</text><text class="dim" x="32.0" y="24.0" font-size="10" text-anchor="end">x₂</text></svg>
  <figcaption>60 points with two related features. The orange arrow is the direction of greatest spread (1st component), the green arrow the 2nd component perpendicular to it; the arrow lengths are proportional to the standard deviation in that direction. In this data the 1st component carries about 94 percent of the total variance.</figcaption>
</figure>

The points lie almost along a single line. If we described each point by
its "position along the line", a single number instead of two, we would
lose very little information. PCA finds this line (and in general the best
$k$-dimensional subspace).

## Step 0: centring

First each feature's mean is subtracted: $x \leftarrow x - \bar{x}$. If the
features are in different units (metres and money, say) they are also
divided by their standard deviations; otherwise the large-scale feature
dominates the variance and PCA sees only it.

## The variance in a direction

The projection $u^\mathsf{T}x$ onto a unit vector $u$ is a number. By the
rule from the Covariance section, its variance is:

$$
\operatorname{Var}(u^\mathsf{T}x) = u^\mathsf{T}\Sigma u
$$

The problem: maximise $u^\mathsf{T}\Sigma u$ subject to
$\lVert u \rVert = 1$. With a Lagrange multiplier, setting the derivative to
zero gives:

$$
\Sigma u = \lambda u
$$

So $u$ is an **eigenvector** of the covariance matrix; the variance in that
direction is $u^\mathsf{T}\Sigma u = \lambda$, the **eigenvalue**. The
direction of greatest spread is the eigenvector of the largest eigenvalue.

- **1st principal component:** the eigenvector of the largest eigenvalue.
- **2nd principal component:** among directions perpendicular to the first,
  the one with the largest variance; the eigenvector of the second largest
  eigenvalue. Since $\Sigma$ is symmetric, its eigenvectors are already
  perpendicular.
- The sum of the eigenvalues (the trace of $\Sigma$) is the total variance.

**Example.**

$$
\Sigma = \begin{pmatrix} 5 & 4 \\ 4 & 5 \end{pmatrix}
$$

The characteristic equation $(5 - \lambda)^2 - 16 = 0$ gives
$\lambda_1 = 9$, $\lambda_2 = 1$. The eigenvectors are
$\frac{1}{\sqrt{2}}(1, 1)$ and $\frac{1}{\sqrt{2}}(1, -1)$. The first
component explains $\frac{9}{10}$ of the total variance, that is $90$
percent.

## Projection and reconstruction

Put the first $k$ eigenvectors side by side as columns: $U_k$
($d \times k$).

$$
z = U_k^\mathsf{T}(x - \bar{x}) \qquad \hat{x} = \bar{x} + U_k z
$$

- $z$: the point's new, $k$-dimensional coordinates (the **component
  scores**).
- $\hat{x}$: the point rebuilt from these $k$ numbers; the orthogonal
  projection onto the subspace.

<figure class="fig">
<svg viewBox="0 0 420 312" width="420"><line class="grid" x1="40.0" y1="292.0" x2="40.0" y2="20.0"/><line class="grid" x1="74.0" y1="292.0" x2="74.0" y2="20.0"/><line class="grid" x1="108.0" y1="292.0" x2="108.0" y2="20.0"/><line class="grid" x1="142.0" y1="292.0" x2="142.0" y2="20.0"/><line class="grid" x1="176.0" y1="292.0" x2="176.0" y2="20.0"/><line class="grid" x1="210.0" y1="292.0" x2="210.0" y2="20.0"/><line class="grid" x1="244.0" y1="292.0" x2="244.0" y2="20.0"/><line class="grid" x1="278.0" y1="292.0" x2="278.0" y2="20.0"/><line class="grid" x1="312.0" y1="292.0" x2="312.0" y2="20.0"/><line class="grid" x1="346.0" y1="292.0" x2="346.0" y2="20.0"/><line class="grid" x1="380.0" y1="292.0" x2="380.0" y2="20.0"/><line class="grid" x1="40.0" y1="292.0" x2="380.0" y2="292.0"/><line class="grid" x1="40.0" y1="258.0" x2="380.0" y2="258.0"/><line class="grid" x1="40.0" y1="224.0" x2="380.0" y2="224.0"/><line class="grid" x1="40.0" y1="190.0" x2="380.0" y2="190.0"/><line class="grid" x1="40.0" y1="156.0" x2="380.0" y2="156.0"/><line class="grid" x1="40.0" y1="122.0" x2="380.0" y2="122.0"/><line class="grid" x1="40.0" y1="88.0" x2="380.0" y2="88.0"/><line class="grid" x1="40.0" y1="54.0" x2="380.0" y2="54.0"/><line class="grid" x1="40.0" y1="20.0" x2="380.0" y2="20.0"/><line class="curve" x1="38.7" y1="287.2" x2="364.8" y2="42.0"/><line class="curve2" stroke-width="1.6" x1="166.8" y1="170.4" x2="176.6" y2="183.5"/><line class="curve2" stroke-width="1.6" x1="143.6" y1="186.8" x2="153.9" y2="200.5"/><line class="curve2" stroke-width="1.6" x1="204.3" y1="171.4" x2="200.1" y2="165.8"/><line class="curve2" stroke-width="1.6" x1="229.4" y1="143.8" x2="229.4" y2="143.8"/><line class="curve2" stroke-width="1.6" x1="248.8" y1="103.6" x2="261.1" y2="120.0"/><line class="curve2" stroke-width="1.6" x1="218.4" y1="157.5" x2="215.7" y2="154.1"/><line class="curve2" stroke-width="1.6" x1="183.7" y1="170.9" x2="187.2" y2="175.5"/><line class="curve2" stroke-width="1.6" x1="175.2" y1="180.8" x2="177.0" y2="183.2"/><line class="curve2" stroke-width="1.6" x1="238.0" y1="125.0" x2="243.9" y2="132.9"/><line class="curve2" stroke-width="1.6" x1="286.1" y1="109.6" x2="282.0" y2="104.2"/><line class="curve2" stroke-width="1.6" x1="223.5" y1="149.4" x2="222.9" y2="148.7"/><line class="curve2" stroke-width="1.6" x1="152.9" y1="191.4" x2="157.6" y2="197.7"/><line class="curve2" stroke-width="1.6" x1="166.4" y1="184.6" x2="169.5" y2="188.8"/><line class="curve2" stroke-width="1.6" x1="288.9" y1="116.9" x2="280.3" y2="105.5"/><circle class="dot" cx="166.8" cy="170.4" r="4"/><circle class="dot3" cx="176.6" cy="183.5" r="3.4"/><circle class="dot" cx="143.6" cy="186.8" r="4"/><circle class="dot3" cx="153.9" cy="200.5" r="3.4"/><circle class="dot" cx="204.3" cy="171.4" r="4"/><circle class="dot3" cx="200.1" cy="165.8" r="3.4"/><circle class="dot" cx="229.4" cy="143.8" r="4"/><circle class="dot3" cx="229.4" cy="143.8" r="3.4"/><circle class="dot" cx="248.8" cy="103.6" r="4"/><circle class="dot3" cx="261.1" cy="120.0" r="3.4"/><circle class="dot" cx="218.4" cy="157.5" r="4"/><circle class="dot3" cx="215.7" cy="154.1" r="3.4"/><circle class="dot" cx="183.7" cy="170.9" r="4"/><circle class="dot3" cx="187.2" cy="175.5" r="3.4"/><circle class="dot" cx="175.2" cy="180.8" r="4"/><circle class="dot3" cx="177.0" cy="183.2" r="3.4"/><circle class="dot" cx="238.0" cy="125.0" r="4"/><circle class="dot3" cx="243.9" cy="132.9" r="3.4"/><circle class="dot" cx="286.1" cy="109.6" r="4"/><circle class="dot3" cx="282.0" cy="104.2" r="3.4"/><circle class="dot" cx="223.5" cy="149.4" r="4"/><circle class="dot3" cx="222.9" cy="148.7" r="3.4"/><circle class="dot" cx="152.9" cy="191.4" r="4"/><circle class="dot3" cx="157.6" cy="197.7" r="3.4"/><circle class="dot" cx="166.4" cy="184.6" r="4"/><circle class="dot3" cx="169.5" cy="188.8" r="3.4"/><circle class="dot" cx="288.9" cy="116.9" r="4"/><circle class="dot3" cx="280.3" cy="105.5" r="3.4"/><text class="ink" x="60" y="36" font-size="11" text-anchor="start">1st component line</text><line class="curve" x1="60" y1="46" x2="86" y2="46"/><circle class="dot3" cx="66" cy="62" r="3.4"/><text class="ink" x="76" y="66" font-size="11" text-anchor="start">projection</text><line class="curve2" x1="60" y1="80" x2="86" y2="80"/><text class="ink" x="92" y="84" font-size="11" text-anchor="start">error (discarded information)</text></svg>
  <figcaption>The points (purple) are projected perpendicularly onto the 1st component line; the projections are green. The orange segments are what is lost in the projection. The line PCA chooses is the one that makes the sum of the squares of these segments smallest.</figcaption>
</figure>

**Example.** The $\Sigma$ above, $\bar{x} = (2, 3)$, $x = (5, 4)$ and
$k = 1$. The centred point is $(3, 1)$; $z = \frac{3 + 1}{\sqrt{2}} \approx
2.83$. Reconstruction $\hat{x} = (2, 3) + 2.83 \cdot \frac{1}{\sqrt{2}}(1,
1) = (4, 5)$. The error is $(1, -1)$, squared $2$.

**Two views, one answer.** Maximising the variance and minimising the
reconstruction error give the same direction. Pythagoras:
$\lVert x - \bar{x} \rVert^2 = \lVert\text{projection}\rVert^2 +
\lVert\text{error}\rVert^2$; the left side is fixed, so as one grows the
other shrinks. The mean squared reconstruction error is the sum of the
eigenvalues of the discarded components (with the $n - 1$ convention of the
sample covariance).

Note: this differs from regression. Regression shrinks the **vertical**
errors in the $y$ direction; PCA shrinks the distances **perpendicular** to
the line, and there is no such thing as a target variable.

## How many components?

Each component's **share of explained variance** is
$\frac{\lambda_j}{\sum_i \lambda_i}$. Components are added until the
cumulative share reaches the desired level (for example $95$ percent).

<figure class="fig">
<svg viewBox="0 0 420 262" width="420"><line class="grid" x1="91.5" y1="216.0" x2="91.5" y2="26.0"/><line class="grid" x1="150.7" y1="216.0" x2="150.7" y2="26.0"/><line class="grid" x1="210.0" y1="216.0" x2="210.0" y2="26.0"/><line class="grid" x1="269.3" y1="216.0" x2="269.3" y2="26.0"/><line class="grid" x1="328.5" y1="216.0" x2="328.5" y2="26.0"/><line class="grid" x1="50.0" y1="216.0" x2="370.0" y2="216.0"/><line class="grid" x1="50.0" y1="179.8" x2="370.0" y2="179.8"/><line class="grid" x1="50.0" y1="143.6" x2="370.0" y2="143.6"/><line class="grid" x1="50.0" y1="107.4" x2="370.0" y2="107.4"/><line class="grid" x1="50.0" y1="71.2" x2="370.0" y2="71.2"/><line class="grid" x1="50.0" y1="35.0" x2="370.0" y2="35.0"/><line class="line" x1="50.0" y1="216.0" x2="370.0" y2="216.0"/><line class="curve3" stroke-dasharray="5 4" x1="50.0" y1="44.1" x2="370.0" y2="44.1"/><text class="dim" x="115.2" y="40.1" font-size="9" text-anchor="start">95 percent</text><rect class="dot" opacity="0.8" x="73.7" y="107.4" width="35.6" height="108.6"/><text class="ink" x="91.5" y="101.4" font-size="10" text-anchor="middle">0.60</text><text class="dim" x="91.5" y="230.0" font-size="10" text-anchor="middle">1</text><rect class="dot" opacity="0.8" x="133.0" y="170.8" width="35.5" height="45.2"/><text class="ink" x="150.7" y="164.8" font-size="10" text-anchor="middle">0.25</text><text class="dim" x="150.7" y="230.0" font-size="10" text-anchor="middle">2</text><rect class="dot" opacity="0.8" x="192.2" y="201.5" width="35.6" height="14.5"/><text class="ink" x="210.0" y="195.5" font-size="10" text-anchor="middle">0.08</text><text class="dim" x="210.0" y="230.0" font-size="10" text-anchor="middle">3</text><rect class="dot" opacity="0.8" x="251.5" y="208.8" width="35.5" height="7.2"/><text class="ink" x="269.3" y="202.8" font-size="10" text-anchor="middle">0.04</text><text class="dim" x="269.3" y="230.0" font-size="10" text-anchor="middle">4</text><rect class="dot" opacity="0.8" x="310.7" y="210.6" width="35.6" height="5.4"/><text class="ink" x="328.5" y="204.6" font-size="10" text-anchor="middle">0.03</text><text class="dim" x="328.5" y="230.0" font-size="10" text-anchor="middle">5</text><line class="curve2" x1="91.5" y1="107.4" x2="150.7" y2="62.2"/><line class="curve2" x1="150.7" y1="62.2" x2="210.0" y2="47.7"/><line class="curve2" x1="210.0" y1="47.7" x2="269.3" y2="40.5"/><line class="curve2" x1="269.3" y1="40.5" x2="328.5" y2="35.0"/><circle class="dot2" cx="91.5" cy="107.4" r="4"/><circle class="dot2" cx="150.7" cy="62.2" r="4"/><circle class="dot2" cx="210.0" cy="47.7" r="4"/><circle class="dot2" cx="269.3" cy="40.5" r="4"/><circle class="dot2" cx="328.5" cy="35.0" r="4"/><text class="ink" x="158.7" y="76.2" font-size="10" text-anchor="start">cumulative 0.85</text><text class="dim" x="46.0" y="182.8" font-size="9" text-anchor="end">0.2</text><text class="dim" x="46.0" y="146.6" font-size="9" text-anchor="end">0.4</text><text class="dim" x="46.0" y="110.4" font-size="9" text-anchor="end">0.6</text><text class="dim" x="46.0" y="74.2" font-size="9" text-anchor="end">0.8</text><text class="dim" x="46.0" y="38.0" font-size="9" text-anchor="end">1.0</text><text class="dim" x="370.0" y="244.0" font-size="10" text-anchor="end">component</text><text class="dim" x="54.0" y="20.0" font-size="10" text-anchor="start">share of explained variance</text></svg>
  <figcaption>Five-feature data with eigenvalues 6, 2.5, 0.8, 0.4, 0.3. The first two components explain 85 percent of the variance; passing 95 percent takes four components. The "elbow" where the bars drop sharply is another criterion.</figcaption>
</figure>

## Computing with the SVD

For a centred data matrix $X$ ($n \times d$), the decomposition
$X = U S V^\mathsf{T}$ from the SVD section gives PCA directly:

- The columns of $V$ are the principal directions.
- The eigenvalues are $\lambda_j = \frac{s_j^2}{n - 1}$ ($s_j$ the singular
  values).
- The component scores are $XV = US$.

Libraries use the SVD without ever building the covariance matrix; it is
both more stable and cheaper when $d$ is very large.

## In machine learning

- **Visualisation:** projecting high-dimensional data onto the first two
  components and plotting it.
- **Pre-processing:** reducing many related features to a few unrelated
  components; it removes multicollinearity and speeds up training.
- **Compression and noise:** components with small eigenvalues are often
  noise; dropping them cleans the data. Describing face images with
  "eigenfaces" is a famous example.
- **Whitening:** dividing the scores by $\sqrt{\lambda_j}$ produces
  unrelated features with unit variance.

**Limits.** PCA is linear: if the data lies on a curved surface, linear
directions cannot describe it well (which is why non-linear methods like
t-SNE, UMAP and autoencoders exist). PCA does not see the target: the
direction carrying the most variance may not be the most useful for
prediction. Outliers distort the covariance and hence the components.

## Common mistakes

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Wrong</h4>
      <p>PCA without subtracting the mean</p>
      <p>metres and money in one table, unscaled</p>
      <p>PCA finds the regression line</p>
      <p>largest variance = most important feature</p>
    </div>
    <div class="ok">
      <h4>Right</h4>
      <p>centre first; standardise if needed</p>
      <p>with different units, work with the correlation matrix</p>
      <p>PCA shrinks perpendicular distances; there is no target</p>
      <p>variance does not mean importance for the target</p>
    </div>
  </div>
  <figcaption>PCA summarises the data's own shape; it does not know what we want to predict.</figcaption>
</figure>

- **Reading components as features.** Each component is a mixture of all
  the features; saying "component 1 = height" is usually wrong. Look at
  the entries of the eigenvector (the loadings).

## Summary

- Centre the data (standardise if needed); covariance matrix $\Sigma$.
- The variance in direction $u$ is $u^\mathsf{T}\Sigma u$; the $u$ that
  maximises it is the eigenvector of the largest eigenvalue.
- The principal components are the perpendicular eigenvectors of $\Sigma$;
  their variances are the eigenvalues.
- $z = U_k^\mathsf{T}(x - \bar{x})$, $\hat{x} = \bar{x} + U_k z$; maximising
  variance = minimising reconstruction error.
- The share of explained variance is $\frac{\lambda_j}{\sum\lambda_i}$;
  choose $k$ by the cumulative share.
- SVD: the directions are the columns of $V$, $\lambda_j = \frac{s_j^2}{n -
  1}$.
