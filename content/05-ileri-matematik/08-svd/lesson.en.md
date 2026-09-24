# Singular Value Decomposition (SVD)

In the previous section eigenvalues showed a matrix's "skeleton": in the
right basis the matrix is just a scaling. But that idea had two gaps: it
worked only for **square** matrices, and not even for every square one
(a rotation had no real eigenvectors).

The **singular value decomposition** (SVD) closes both gaps: it splits
**every** matrix, of any size, into three simple pieces. It is perhaps
the most useful result of linear algebra. Image compression,
recommendation systems, PCA, noise removal and extracting meaning from
text are all applications of the SVD.

Prerequisite: the Eigenvalues and Eigenvectors section.

## The main idea: rotate, stretch, rotate

Every $m \times n$ matrix $A$ can be written as:

$$
A = U \Sigma V^\mathsf{T}
$$

| Piece | Size | What it does |
|---|---|---|
| $V^\mathsf{T}$ | $n \times n$ | Rotates (or reflects); does not change lengths |
| $\Sigma$ | $m \times n$ | Stretches along the axes; its diagonal holds $\sigma_1 \ge \sigma_2 \ge \cdots \ge 0$ |
| $U$ | $m \times m$ | Rotates (or reflects); does not change lengths |

The columns of $U$ and $V$ are mutually perpendicular unit vectors (such
matrices are called **orthogonal**; $U^\mathsf{T}U = I$, so their inverse
is their transpose). The numbers on the diagonal of $\Sigma$ are the
**singular values**: always zero or positive, sorted from largest to
smallest.

<figure class="fig">
<svg viewBox="0 0 440 144" width="440"><line class="grid" x1="8" y1="116" x2="8" y2="14"/><line class="grid" x1="25" y1="116" x2="25" y2="14"/><line class="grid" x1="42" y1="116" x2="42" y2="14"/><line class="line" x1="59" y1="116" x2="59" y2="14"/><line class="grid" x1="76" y1="116" x2="76" y2="14"/><line class="grid" x1="93" y1="116" x2="93" y2="14"/><line class="grid" x1="110" y1="116" x2="110" y2="14"/><line class="grid" x1="8" y1="116" x2="110" y2="116"/><line class="grid" x1="8" y1="99" x2="110" y2="99"/><line class="grid" x1="8" y1="82" x2="110" y2="82"/><line class="line" x1="8" y1="65" x2="110" y2="65"/><line class="grid" x1="8" y1="48" x2="110" y2="48"/><line class="grid" x1="8" y1="31" x2="110" y2="31"/><line class="grid" x1="8" y1="14" x2="110" y2="14"/><polygon class="dot" opacity="0.14" points="76.0,65.0 75.9,63.5 75.7,62.0 75.4,60.6 75.0,59.2 74.4,57.8 73.7,56.5 72.9,55.2 72.0,54.1 71.0,53.0 69.9,52.0 68.8,51.1 67.5,50.3 66.2,49.6 64.8,49.0 63.4,48.6 62.0,48.3 60.5,48.1 59.0,48.0 57.5,48.1 56.0,48.3 54.6,48.6 53.2,49.0 51.8,49.6 50.5,50.3 49.2,51.1 48.1,52.0 47.0,53.0 46.0,54.1 45.1,55.2 44.3,56.5 43.6,57.8 43.0,59.2 42.6,60.6 42.3,62.0 42.1,63.5 42.0,65.0 42.1,66.5 42.3,68.0 42.6,69.4 43.0,70.8 43.6,72.2 44.3,73.5 45.1,74.8 46.0,75.9 47.0,77.0 48.1,78.0 49.2,78.9 50.5,79.7 51.8,80.4 53.2,81.0 54.6,81.4 56.0,81.7 57.5,81.9 59.0,82.0 60.5,81.9 62.0,81.7 63.4,81.4 64.8,81.0 66.2,80.4 67.5,79.7 68.8,78.9 69.9,78.0 71.0,77.0 72.0,75.9 72.9,74.8 73.7,73.5 74.4,72.2 75.0,70.8 75.4,69.4 75.7,68.0 75.9,66.5"/><polygon class="curve3" points="76.0,65.0 75.9,63.5 75.7,62.0 75.4,60.6 75.0,59.2 74.4,57.8 73.7,56.5 72.9,55.2 72.0,54.1 71.0,53.0 69.9,52.0 68.8,51.1 67.5,50.3 66.2,49.6 64.8,49.0 63.4,48.6 62.0,48.3 60.5,48.1 59.0,48.0 57.5,48.1 56.0,48.3 54.6,48.6 53.2,49.0 51.8,49.6 50.5,50.3 49.2,51.1 48.1,52.0 47.0,53.0 46.0,54.1 45.1,55.2 44.3,56.5 43.6,57.8 43.0,59.2 42.6,60.6 42.3,62.0 42.1,63.5 42.0,65.0 42.1,66.5 42.3,68.0 42.6,69.4 43.0,70.8 43.6,72.2 44.3,73.5 45.1,74.8 46.0,75.9 47.0,77.0 48.1,78.0 49.2,78.9 50.5,79.7 51.8,80.4 53.2,81.0 54.6,81.4 56.0,81.7 57.5,81.9 59.0,82.0 60.5,81.9 62.0,81.7 63.4,81.4 64.8,81.0 66.2,80.4 67.5,79.7 68.8,78.9 69.9,78.0 71.0,77.0 72.0,75.9 72.9,74.8 73.7,73.5 74.4,72.2 75.0,70.8 75.4,69.4 75.7,68.0 75.9,66.5"/><line class="curve" x1="59" y1="65" x2="67.0" y2="57.0"/><polygon class="dot" points="71.0,53.0 68.5,59.5 64.5,55.5"/><line class="curve2" x1="59" y1="65" x2="51.0" y2="57.0"/><polygon class="dot2" points="47.0,53.0 53.5,55.5 49.5,59.5"/><text class="ink" x="59.0" y="134" font-size="11" text-anchor="middle">Start</text><text class="dim" x="113" y="69.0" font-size="12" text-anchor="middle">→</text><line class="grid" x1="116" y1="116" x2="116" y2="14"/><line class="grid" x1="133" y1="116" x2="133" y2="14"/><line class="grid" x1="150" y1="116" x2="150" y2="14"/><line class="line" x1="167" y1="116" x2="167" y2="14"/><line class="grid" x1="184" y1="116" x2="184" y2="14"/><line class="grid" x1="201" y1="116" x2="201" y2="14"/><line class="grid" x1="218" y1="116" x2="218" y2="14"/><line class="grid" x1="116" y1="116" x2="218" y2="116"/><line class="grid" x1="116" y1="99" x2="218" y2="99"/><line class="grid" x1="116" y1="82" x2="218" y2="82"/><line class="line" x1="116" y1="65" x2="218" y2="65"/><line class="grid" x1="116" y1="48" x2="218" y2="48"/><line class="grid" x1="116" y1="31" x2="218" y2="31"/><line class="grid" x1="116" y1="14" x2="218" y2="14"/><polygon class="dot" opacity="0.14" points="179.0,77.0 180.0,75.9 180.9,74.8 181.7,73.5 182.4,72.2 183.0,70.8 183.4,69.4 183.7,68.0 183.9,66.5 184.0,65.0 183.9,63.5 183.7,62.0 183.4,60.6 183.0,59.2 182.4,57.8 181.7,56.5 180.9,55.2 180.0,54.1 179.0,53.0 177.9,52.0 176.8,51.1 175.5,50.3 174.2,49.6 172.8,49.0 171.4,48.6 170.0,48.3 168.5,48.1 167.0,48.0 165.5,48.1 164.0,48.3 162.6,48.6 161.2,49.0 159.8,49.6 158.5,50.3 157.2,51.1 156.1,52.0 155.0,53.0 154.0,54.1 153.1,55.2 152.3,56.5 151.6,57.8 151.0,59.2 150.6,60.6 150.3,62.0 150.1,63.5 150.0,65.0 150.1,66.5 150.3,68.0 150.6,69.4 151.0,70.8 151.6,72.2 152.3,73.5 153.1,74.8 154.0,75.9 155.0,77.0 156.1,78.0 157.2,78.9 158.5,79.7 159.8,80.4 161.2,81.0 162.6,81.4 164.0,81.7 165.5,81.9 167.0,82.0 168.5,81.9 170.0,81.7 171.4,81.4 172.8,81.0 174.2,80.4 175.5,79.7 176.8,78.9 177.9,78.0"/><polygon class="curve3" points="179.0,77.0 180.0,75.9 180.9,74.8 181.7,73.5 182.4,72.2 183.0,70.8 183.4,69.4 183.7,68.0 183.9,66.5 184.0,65.0 183.9,63.5 183.7,62.0 183.4,60.6 183.0,59.2 182.4,57.8 181.7,56.5 180.9,55.2 180.0,54.1 179.0,53.0 177.9,52.0 176.8,51.1 175.5,50.3 174.2,49.6 172.8,49.0 171.4,48.6 170.0,48.3 168.5,48.1 167.0,48.0 165.5,48.1 164.0,48.3 162.6,48.6 161.2,49.0 159.8,49.6 158.5,50.3 157.2,51.1 156.1,52.0 155.0,53.0 154.0,54.1 153.1,55.2 152.3,56.5 151.6,57.8 151.0,59.2 150.6,60.6 150.3,62.0 150.1,63.5 150.0,65.0 150.1,66.5 150.3,68.0 150.6,69.4 151.0,70.8 151.6,72.2 152.3,73.5 153.1,74.8 154.0,75.9 155.0,77.0 156.1,78.0 157.2,78.9 158.5,79.7 159.8,80.4 161.2,81.0 162.6,81.4 164.0,81.7 165.5,81.9 167.0,82.0 168.5,81.9 170.0,81.7 171.4,81.4 172.8,81.0 174.2,80.4 175.5,79.7 176.8,78.9 177.9,78.0"/><line class="curve" x1="167" y1="65" x2="178.4" y2="65.0"/><polygon class="dot" points="184.0,65.0 177.6,67.9 177.6,62.1"/><line class="curve2" x1="167" y1="65" x2="167.0" y2="53.6"/><polygon class="dot2" points="167.0,48.0 169.9,54.4 164.1,54.4"/><text class="ink" x="167.0" y="134" font-size="11" text-anchor="middle">Vᵀ: rotate</text><text class="dim" x="221" y="69.0" font-size="12" text-anchor="middle">→</text><line class="grid" x1="224" y1="116" x2="224" y2="14"/><line class="grid" x1="241" y1="116" x2="241" y2="14"/><line class="grid" x1="258" y1="116" x2="258" y2="14"/><line class="line" x1="275" y1="116" x2="275" y2="14"/><line class="grid" x1="292" y1="116" x2="292" y2="14"/><line class="grid" x1="309" y1="116" x2="309" y2="14"/><line class="grid" x1="326" y1="116" x2="326" y2="14"/><line class="grid" x1="224" y1="116" x2="326" y2="116"/><line class="grid" x1="224" y1="99" x2="326" y2="99"/><line class="grid" x1="224" y1="82" x2="326" y2="82"/><line class="line" x1="224" y1="65" x2="326" y2="65"/><line class="grid" x1="224" y1="48" x2="326" y2="48"/><line class="grid" x1="224" y1="31" x2="326" y2="31"/><line class="grid" x1="224" y1="14" x2="326" y2="14"/><polygon class="dot" opacity="0.14" points="299.0,74.6 301.0,73.7 302.9,72.8 304.4,71.8 305.8,70.7 306.9,69.7 307.8,68.5 308.5,67.4 308.9,66.2 309.0,65.0 308.9,63.8 308.5,62.6 307.8,61.5 306.9,60.3 305.8,59.3 304.4,58.2 302.9,57.2 301.0,56.3 299.0,55.4 296.9,54.6 294.5,53.9 292.0,53.2 289.4,52.7 286.6,52.2 283.8,51.9 280.9,51.6 278.0,51.5 275.0,51.4 272.0,51.5 269.1,51.6 266.2,51.9 263.4,52.2 260.6,52.7 258.0,53.2 255.5,53.9 253.1,54.6 251.0,55.4 249.0,56.3 247.1,57.2 245.6,58.2 244.2,59.3 243.1,60.3 242.2,61.5 241.5,62.6 241.1,63.8 241.0,65.0 241.1,66.2 241.5,67.4 242.2,68.5 243.1,69.7 244.2,70.7 245.6,71.8 247.1,72.8 249.0,73.7 251.0,74.6 253.1,75.4 255.5,76.1 258.0,76.8 260.6,77.3 263.4,77.8 266.2,78.1 269.1,78.4 272.0,78.5 275.0,78.6 278.0,78.5 280.9,78.4 283.8,78.1 286.6,77.8 289.4,77.3 292.0,76.8 294.5,76.1 296.9,75.4"/><polygon class="curve3" points="299.0,74.6 301.0,73.7 302.9,72.8 304.4,71.8 305.8,70.7 306.9,69.7 307.8,68.5 308.5,67.4 308.9,66.2 309.0,65.0 308.9,63.8 308.5,62.6 307.8,61.5 306.9,60.3 305.8,59.3 304.4,58.2 302.9,57.2 301.0,56.3 299.0,55.4 296.9,54.6 294.5,53.9 292.0,53.2 289.4,52.7 286.6,52.2 283.8,51.9 280.9,51.6 278.0,51.5 275.0,51.4 272.0,51.5 269.1,51.6 266.2,51.9 263.4,52.2 260.6,52.7 258.0,53.2 255.5,53.9 253.1,54.6 251.0,55.4 249.0,56.3 247.1,57.2 245.6,58.2 244.2,59.3 243.1,60.3 242.2,61.5 241.5,62.6 241.1,63.8 241.0,65.0 241.1,66.2 241.5,67.4 242.2,68.5 243.1,69.7 244.2,70.7 245.6,71.8 247.1,72.8 249.0,73.7 251.0,74.6 253.1,75.4 255.5,76.1 258.0,76.8 260.6,77.3 263.4,77.8 266.2,78.1 269.1,78.4 272.0,78.5 275.0,78.6 278.0,78.5 280.9,78.4 283.8,78.1 286.6,77.8 289.4,77.3 292.0,76.8 294.5,76.1 296.9,75.4"/><line class="curve" x1="275" y1="65" x2="303.4" y2="65.0"/><polygon class="dot" points="309.0,65.0 302.6,67.9 302.6,62.1"/><line class="curve2" x1="275" y1="65" x2="275.0" y2="57.0"/><polygon class="dot2" points="275.0,51.4 277.9,57.8 272.1,57.8"/><text class="ink" x="275.0" y="134" font-size="11" text-anchor="middle">Σ: stretch</text><text class="dim" x="329" y="69.0" font-size="12" text-anchor="middle">→</text><line class="grid" x1="332" y1="116" x2="332" y2="14"/><line class="grid" x1="349" y1="116" x2="349" y2="14"/><line class="grid" x1="366" y1="116" x2="366" y2="14"/><line class="line" x1="383" y1="116" x2="383" y2="14"/><line class="grid" x1="400" y1="116" x2="400" y2="14"/><line class="grid" x1="417" y1="116" x2="417" y2="14"/><line class="grid" x1="434" y1="116" x2="434" y2="14"/><line class="grid" x1="332" y1="116" x2="434" y2="116"/><line class="grid" x1="332" y1="99" x2="434" y2="99"/><line class="grid" x1="332" y1="82" x2="434" y2="82"/><line class="line" x1="332" y1="65" x2="434" y2="65"/><line class="grid" x1="332" y1="48" x2="434" y2="48"/><line class="grid" x1="332" y1="31" x2="434" y2="31"/><line class="grid" x1="332" y1="14" x2="434" y2="14"/><polygon class="dot" opacity="0.14" points="408.6,61.3 409.9,59.5 411.0,57.8 411.9,56.2 412.6,54.6 413.0,53.1 413.2,51.6 413.2,50.3 412.9,49.1 412.4,48.0 411.7,47.0 410.8,46.2 409.7,45.5 408.3,45.0 406.8,44.6 405.1,44.4 403.2,44.3 401.2,44.4 399.0,44.7 396.7,45.1 394.3,45.6 391.8,46.3 389.3,47.1 386.7,48.1 384.1,49.2 381.4,50.4 378.8,51.8 376.2,53.2 373.7,54.7 371.2,56.4 368.8,58.0 366.5,59.7 364.4,61.5 362.4,63.3 360.5,65.1 358.9,66.9 357.4,68.7 356.1,70.5 355.0,72.2 354.1,73.8 353.4,75.4 353.0,76.9 352.8,78.4 352.8,79.7 353.1,80.9 353.6,82.0 354.3,83.0 355.2,83.8 356.3,84.5 357.7,85.0 359.2,85.4 360.9,85.6 362.8,85.7 364.8,85.6 367.0,85.3 369.3,84.9 371.7,84.4 374.2,83.7 376.7,82.9 379.3,81.9 381.9,80.8 384.6,79.6 387.2,78.2 389.8,76.8 392.3,75.3 394.8,73.6 397.2,72.0 399.5,70.3 401.6,68.5 403.6,66.7 405.5,64.9 407.1,63.1"/><polygon class="curve3" points="408.6,61.3 409.9,59.5 411.0,57.8 411.9,56.2 412.6,54.6 413.0,53.1 413.2,51.6 413.2,50.3 412.9,49.1 412.4,48.0 411.7,47.0 410.8,46.2 409.7,45.5 408.3,45.0 406.8,44.6 405.1,44.4 403.2,44.3 401.2,44.4 399.0,44.7 396.7,45.1 394.3,45.6 391.8,46.3 389.3,47.1 386.7,48.1 384.1,49.2 381.4,50.4 378.8,51.8 376.2,53.2 373.7,54.7 371.2,56.4 368.8,58.0 366.5,59.7 364.4,61.5 362.4,63.3 360.5,65.1 358.9,66.9 357.4,68.7 356.1,70.5 355.0,72.2 354.1,73.8 353.4,75.4 353.0,76.9 352.8,78.4 352.8,79.7 353.1,80.9 353.6,82.0 354.3,83.0 355.2,83.8 356.3,84.5 357.7,85.0 359.2,85.4 360.9,85.6 362.8,85.7 364.8,85.6 367.0,85.3 369.3,84.9 371.7,84.4 374.2,83.7 376.7,82.9 379.3,81.9 381.9,80.8 384.6,79.6 387.2,78.2 389.8,76.8 392.3,75.3 394.8,73.6 397.2,72.0 399.5,70.3 401.6,68.5 403.6,66.7 405.5,64.9 407.1,63.1"/><line class="curve" x1="383" y1="65" x2="407.6" y2="50.8"/><polygon class="dot" points="412.4,48.0 408.3,53.7 405.4,48.7"/><line class="curve2" x1="383" y1="65" x2="379.0" y2="58.1"/><polygon class="dot2" points="376.2,53.2 381.9,57.3 376.9,60.2"/><text class="ink" x="383.0" y="134" font-size="11" text-anchor="middle">U: rotate</text></svg>
  <figcaption>What a matrix does to a circle: first $V^\mathsf{T}$ rotates the circle so the purple and orange directions sit on the axes, then $\Sigma$ stretches along the axes (here by 2 and 0.8), and finally $U$ rotates the resulting ellipse into place.</figcaption>
</figure>

The meaning is powerful: **even the most complicated-looking linear
transformation is a rotation, a stretch along the axes, and another
rotation.** All the "real work" is in the middle $\Sigma$; the other two
matrices only change directions.

## Geometry: the circle becomes an ellipse

A matrix always takes the unit circle to an **ellipse** (or, if it
squashes, to a line segment). The SVD describes this ellipse exactly:

- The lengths of the ellipse's semi-axes are the singular values:
  $\sigma_1$ (longest), $\sigma_2$, …
- The directions of the axes are the columns of $U$: $\mathbf{u}_1,
  \mathbf{u}_2, \dots$ (the **left singular vectors**)
- The points on the circle that go to these axes are the columns of $V$:
  $\mathbf{v}_1, \mathbf{v}_2, \dots$ (the **right singular vectors**)

In short:

$$
A\mathbf{v}_i = \sigma_i \mathbf{u}_i
$$

It looks like the eigenvalue equation ($A\mathbf{v} = \lambda\mathbf{v}$),
with one difference: the input direction ($\mathbf{v}_i$) and the output
direction ($\mathbf{u}_i$) may differ. That flexibility is what lets the
SVD work for every matrix.

<figure class="fig">
<svg viewBox="0 0 360 270" width="360"><line class="grid" x1="20" y1="214" x2="20" y2="70"/><line class="grid" x1="56" y1="214" x2="56" y2="70"/><line class="line" x1="92" y1="214" x2="92" y2="70"/><line class="grid" x1="128" y1="214" x2="128" y2="70"/><line class="grid" x1="164" y1="214" x2="164" y2="70"/><line class="grid" x1="20" y1="214" x2="164" y2="214"/><line class="grid" x1="20" y1="178" x2="164" y2="178"/><line class="line" x1="20" y1="142" x2="164" y2="142"/><line class="grid" x1="20" y1="106" x2="164" y2="106"/><line class="grid" x1="20" y1="70" x2="164" y2="70"/><polygon class="dot" opacity="0.14" points="128.0,142.0 127.9,138.9 127.5,135.7 126.8,132.7 125.8,129.7 124.6,126.8 123.2,124.0 121.5,121.4 119.6,118.9 117.5,116.5 115.1,114.4 112.6,112.5 110.0,110.8 107.2,109.4 104.3,108.2 101.3,107.2 98.3,106.5 95.1,106.1 92.0,106.0 88.9,106.1 85.7,106.5 82.7,107.2 79.7,108.2 76.8,109.4 74.0,110.8 71.4,112.5 68.9,114.4 66.5,116.5 64.4,118.9 62.5,121.4 60.8,124.0 59.4,126.8 58.2,129.7 57.2,132.7 56.5,135.7 56.1,138.9 56.0,142.0 56.1,145.1 56.5,148.3 57.2,151.3 58.2,154.3 59.4,157.2 60.8,160.0 62.5,162.6 64.4,165.1 66.5,167.5 68.9,169.6 71.4,171.5 74.0,173.2 76.8,174.6 79.7,175.8 82.7,176.8 85.7,177.5 88.9,177.9 92.0,178.0 95.1,177.9 98.3,177.5 101.3,176.8 104.3,175.8 107.2,174.6 110.0,173.2 112.6,171.5 115.1,169.6 117.5,167.5 119.6,165.1 121.5,162.6 123.2,160.0 124.6,157.2 125.8,154.3 126.8,151.3 127.5,148.3 127.9,145.1"/><polygon class="curve3" points="128.0,142.0 127.9,138.9 127.5,135.7 126.8,132.7 125.8,129.7 124.6,126.8 123.2,124.0 121.5,121.4 119.6,118.9 117.5,116.5 115.1,114.4 112.6,112.5 110.0,110.8 107.2,109.4 104.3,108.2 101.3,107.2 98.3,106.5 95.1,106.1 92.0,106.0 88.9,106.1 85.7,106.5 82.7,107.2 79.7,108.2 76.8,109.4 74.0,110.8 71.4,112.5 68.9,114.4 66.5,116.5 64.4,118.9 62.5,121.4 60.8,124.0 59.4,126.8 58.2,129.7 57.2,132.7 56.5,135.7 56.1,138.9 56.0,142.0 56.1,145.1 56.5,148.3 57.2,151.3 58.2,154.3 59.4,157.2 60.8,160.0 62.5,162.6 64.4,165.1 66.5,167.5 68.9,169.6 71.4,171.5 74.0,173.2 76.8,174.6 79.7,175.8 82.7,176.8 85.7,177.5 88.9,177.9 92.0,178.0 95.1,177.9 98.3,177.5 101.3,176.8 104.3,175.8 107.2,174.6 110.0,173.2 112.6,171.5 115.1,169.6 117.5,167.5 119.6,165.1 121.5,162.6 123.2,160.0 124.6,157.2 125.8,154.3 126.8,151.3 127.5,148.3 127.9,145.1"/><line class="curve" x1="92" y1="142" x2="112.4" y2="121.6"/><polygon class="dot" points="117.5,116.5 114.3,124.9 109.1,119.7"/><line class="curve2" x1="92" y1="142" x2="112.4" y2="162.4"/><polygon class="dot2" points="117.5,167.5 109.1,164.3 114.3,159.1"/><text class="ink" x="121.5" y="114.5" font-size="12" text-anchor="start">v₁</text><text class="ink" x="121.5" y="179.5" font-size="12" text-anchor="start">v₂</text><text class="ink" x="92.0" y="234" font-size="12" text-anchor="middle">Unit circle</text><line class="grid" x1="214" y1="238" x2="214" y2="14"/><line class="grid" x1="230" y1="238" x2="230" y2="14"/><line class="grid" x1="246" y1="238" x2="246" y2="14"/><line class="grid" x1="262" y1="238" x2="262" y2="14"/><line class="line" x1="278" y1="238" x2="278" y2="14"/><line class="grid" x1="294" y1="238" x2="294" y2="14"/><line class="grid" x1="310" y1="238" x2="310" y2="14"/><line class="grid" x1="326" y1="238" x2="326" y2="14"/><line class="grid" x1="342" y1="238" x2="342" y2="14"/><line class="grid" x1="214" y1="238" x2="342" y2="238"/><line class="grid" x1="214" y1="222" x2="342" y2="222"/><line class="grid" x1="214" y1="206" x2="342" y2="206"/><line class="grid" x1="214" y1="190" x2="342" y2="190"/><line class="grid" x1="214" y1="174" x2="342" y2="174"/><line class="grid" x1="214" y1="158" x2="342" y2="158"/><line class="grid" x1="214" y1="142" x2="342" y2="142"/><line class="line" x1="214" y1="126" x2="342" y2="126"/><line class="grid" x1="214" y1="110" x2="342" y2="110"/><line class="grid" x1="214" y1="94" x2="342" y2="94"/><line class="grid" x1="214" y1="78" x2="342" y2="78"/><line class="grid" x1="214" y1="62" x2="342" y2="62"/><line class="grid" x1="214" y1="46" x2="342" y2="46"/><line class="grid" x1="214" y1="30" x2="342" y2="30"/><line class="grid" x1="214" y1="14" x2="342" y2="14"/><polygon class="dot" opacity="0.14" points="326.0,62.0 325.8,55.3 325.3,49.1 324.4,43.5 323.1,38.5 321.5,34.2 319.6,30.6 317.3,27.7 314.8,25.6 311.9,24.2 308.9,23.6 305.5,23.8 302.0,24.7 298.3,26.4 294.4,28.9 290.4,32.2 286.3,36.1 282.2,40.7 278.0,46.0 273.8,51.9 269.7,58.3 265.6,65.3 261.6,72.7 257.7,80.5 254.0,88.7 250.5,97.2 247.1,105.9 244.1,114.7 241.2,123.6 238.7,132.5 236.4,141.4 234.5,150.2 232.9,158.8 231.6,167.1 230.7,175.1 230.2,182.8 230.0,190.0 230.2,196.7 230.7,202.9 231.6,208.5 232.9,213.5 234.5,217.8 236.4,221.4 238.7,224.3 241.2,226.4 244.1,227.8 247.1,228.4 250.5,228.2 254.0,227.3 257.7,225.6 261.6,223.1 265.6,219.8 269.7,215.9 273.8,211.3 278.0,206.0 282.2,200.1 286.3,193.7 290.4,186.7 294.4,179.3 298.3,171.5 302.0,163.3 305.5,154.8 308.9,146.1 311.9,137.3 314.8,128.4 317.3,119.5 319.6,110.6 321.5,101.8 323.1,93.2 324.4,84.9 325.3,76.9 325.8,69.2"/><polygon class="curve3" points="326.0,62.0 325.8,55.3 325.3,49.1 324.4,43.5 323.1,38.5 321.5,34.2 319.6,30.6 317.3,27.7 314.8,25.6 311.9,24.2 308.9,23.6 305.5,23.8 302.0,24.7 298.3,26.4 294.4,28.9 290.4,32.2 286.3,36.1 282.2,40.7 278.0,46.0 273.8,51.9 269.7,58.3 265.6,65.3 261.6,72.7 257.7,80.5 254.0,88.7 250.5,97.2 247.1,105.9 244.1,114.7 241.2,123.6 238.7,132.5 236.4,141.4 234.5,150.2 232.9,158.8 231.6,167.1 230.7,175.1 230.2,182.8 230.0,190.0 230.2,196.7 230.7,202.9 231.6,208.5 232.9,213.5 234.5,217.8 236.4,221.4 238.7,224.3 241.2,226.4 244.1,227.8 247.1,228.4 250.5,228.2 254.0,227.3 257.7,225.6 261.6,223.1 265.6,219.8 269.7,215.9 273.8,211.3 278.0,206.0 282.2,200.1 286.3,193.7 290.4,186.7 294.4,179.3 298.3,171.5 302.0,163.3 305.5,154.8 308.9,146.1 311.9,137.3 314.8,128.4 317.3,119.5 319.6,110.6 321.5,101.8 323.1,93.2 324.4,84.9 325.3,76.9 325.8,69.2"/><line class="curve" x1="278" y1="126" x2="309.6" y2="31.0"/><polygon class="dot" points="311.9,24.2 312.8,33.2 305.8,30.8"/><line class="curve2" x1="278" y1="126" x2="305.1" y2="135.0"/><polygon class="dot2" points="311.9,137.3 302.9,138.2 305.3,131.2"/><text class="ink" x="317.9" y="30.2" font-size="12" text-anchor="start">σ₁u₁</text><text class="ink" x="317.9" y="147.3" font-size="12" text-anchor="start">σ₂u₂</text><text class="ink" x="278.0" y="258" font-size="12" text-anchor="middle">Under A: an ellipse</text></svg>
  <figcaption>$A = \begin{bmatrix} 3 & 0 \\ 4 & 5 \end{bmatrix}$ takes the unit circle to an ellipse. $\mathbf{v}_1$ (purple) on the circle goes to the longest axis of the ellipse, $\sigma_1\mathbf{u}_1$; $\mathbf{v}_2$ (orange) to the shortest. The two axes are perpendicular; the singular values are $\sigma_1 \approx 6.71$ and $\sigma_2 \approx 2.24$.</figcaption>
</figure>

$\sigma_1$ is the **largest** factor by which $A$ can stretch a unit
vector; $\sigma_n$ the smallest. That is why $\sigma_1$ is also called the
**norm** of the matrix: $\|A\| = \sigma_1$.

## Finding the singular values

The way to find the SVD by hand goes through $A^\mathsf{T}A$. If $A =
U\Sigma V^\mathsf{T}$, then:

$$
A^\mathsf{T}A = V\Sigma^\mathsf{T}U^\mathsf{T}U\Sigma V^\mathsf{T} = V (\Sigma^\mathsf{T}\Sigma) V^\mathsf{T}
$$

($U^\mathsf{T}U = I$.) This is the diagonalisation of the symmetric matrix
$A^\mathsf{T}A$! So:

- The **eigenvalues** of $A^\mathsf{T}A$ are the **squares** of the singular values: $\sigma_i^2$.
- The **eigenvectors** of $A^\mathsf{T}A$ are the right singular vectors $\mathbf{v}_i$.
- The left singular vectors are $\mathbf{u}_i = \dfrac{A\mathbf{v}_i}{\sigma_i}$.

$A^\mathsf{T}A$ is always symmetric and its eigenvalues are never negative
($\mathbf{v}^\mathsf{T}A^\mathsf{T}A\mathbf{v} = \|A\mathbf{v}\|^2 \ge 0$);
that is why their square roots can be taken.

### An example

$$
A = \begin{bmatrix} 3 & 0 \\ 4 & 5 \end{bmatrix}
$$

**Step 1 — $A^\mathsf{T}A$.**

$$
A^\mathsf{T}A = \begin{bmatrix} 3 & 4 \\ 0 & 5 \end{bmatrix} \begin{bmatrix} 3 & 0 \\ 4 & 5 \end{bmatrix} = \begin{bmatrix} 25 & 20 \\ 20 & 25 \end{bmatrix}
$$

**Step 2 — Its eigenvalues.** Trace $50$, determinant $625 - 400 = 225$:
$\lambda^2 - 50\lambda + 225 = (\lambda - 45)(\lambda - 5) = 0$.

$$
\sigma_1 = \sqrt{45} = 3\sqrt{5} \approx 6.71
\qquad
\sigma_2 = \sqrt{5} \approx 2.24
$$

**Step 3 — The right singular vectors.** $A^\mathsf{T}A - 45I = \begin{bmatrix} -20 & 20 \\ 20 & -20 \end{bmatrix}$:
$y = x$. $A^\mathsf{T}A - 5I = \begin{bmatrix} 20 & 20 \\ 20 & 20 \end{bmatrix}$: $y = -x$.
Scaled to unit length:

$$
\mathbf{v}_1 = \tfrac{1}{\sqrt{2}}(1, 1)
\qquad
\mathbf{v}_2 = \tfrac{1}{\sqrt{2}}(1, -1)
$$

**Step 4 — The left singular vectors.** $A\mathbf{v}_1 = \tfrac{1}{\sqrt{2}}(3, 9)$;
dividing by $\sigma_1 = 3\sqrt{5}$ gives $\mathbf{u}_1 = \tfrac{1}{\sqrt{10}}(1, 3)$.
$A\mathbf{v}_2 = \tfrac{1}{\sqrt{2}}(3, -1)$; dividing by $\sqrt{5}$ gives
$\mathbf{u}_2 = \tfrac{1}{\sqrt{10}}(3, -1)$.

Check: $\mathbf{u}_1 \cdot \mathbf{u}_2 = \tfrac{1}{10}(3 - 3) = 0$ (perpendicular) ✓;
$\sigma_1\sigma_2 = \sqrt{45 \cdot 5} = 15 = |\det A|$ ✓.

## What the singular values tell you

| Property | In terms of singular values |
|---|---|
| Rank | The number of non-zero singular values |
| Norm (largest stretch) | $\sigma_1$ |
| $\lvert\det A\rvert$ for a square matrix | $\sigma_1 \sigma_2 \cdots \sigma_n$ |
| Sum of the squares of all entries | $\sigma_1^2 + \sigma_2^2 + \cdots$ |
| Invertibility (square) | all non-zero |
| Condition number | $\sigma_1 / \sigma_n$ |

The **condition number** matters especially: a matrix that stretches one
direction a lot and another very little ($\sigma_1 / \sigma_n$ large) makes
the ellipse needle-thin. Solving equations with such a matrix turns a
small error in the input into a large error in the output. This is what
we called "nearly singular" in earlier sections.

**The link to eigenvalues.** For a symmetric matrix with non-negative
eigenvalues (covariance matrices are like this), the SVD and the
eigendecomposition are the same thing: the singular values are the
eigenvalues and $U = V$. For general matrices the two differ.

## The SVD as a sum: layers

Expanding the product $U\Sigma V^\mathsf{T}$ writes $A$ as a sum of simple
matrices **of rank 1**:

$$
A = \sigma_1 \mathbf{u}_1 \mathbf{v}_1^\mathsf{T} + \sigma_2 \mathbf{u}_2 \mathbf{v}_2^\mathsf{T} + \cdots + \sigma_r \mathbf{u}_r \mathbf{v}_r^\mathsf{T}
$$

Each $\mathbf{u}_i\mathbf{v}_i^\mathsf{T}$ is a column times a row: a
matrix whose rows are all multiples of the same vector (a "layer"). The
singular value says how important that layer is. The layers are in order
of importance: the first carries the matrix's biggest structure, the later
ones ever smaller details.

## Low-rank approximation

Keep the first $k$ layers and drop the rest:

$$
A_k = \sigma_1 \mathbf{u}_1 \mathbf{v}_1^\mathsf{T} + \cdots + \sigma_k \mathbf{u}_k \mathbf{v}_k^\mathsf{T}
$$

**The Eckart–Young theorem:** among all matrices of rank $k$, $A_k$ is the
**closest** to $A$. The error is measured by the dropped singular values
(the sum of the squared differences of the entries):

$$
\|A - A_k\|^2 = \sigma_{k+1}^2 + \sigma_{k+2}^2 + \cdots
$$

That is why the **squares** of the singular values are called "energy".
The share carried by the first $k$ layers:

$$
\frac{\sigma_1^2 + \cdots + \sigma_k^2}{\sigma_1^2 + \cdots + \sigma_r^2}
$$

<figure class="fig">
<svg viewBox="0 0 380 226" width="380"><rect class="dot" opacity="0.85" x="60" y="20.0" width="44" height="150.0" rx="3"/><text class="ink" x="82" y="14.0" font-size="12" text-anchor="middle">12</text><text class="ink" x="82" y="188" font-size="13" text-anchor="middle">σ₁</text><rect class="dot" opacity="0.85" x="130" y="107.5" width="44" height="62.5" rx="3"/><text class="ink" x="152" y="101.5" font-size="12" text-anchor="middle">5</text><text class="ink" x="152" y="188" font-size="13" text-anchor="middle">σ₂</text><rect class="dim" opacity="0.45" x="200" y="132.5" width="44" height="37.5" rx="3"/><text class="ink" x="222" y="126.5" font-size="12" text-anchor="middle">3</text><text class="ink" x="222" y="188" font-size="13" text-anchor="middle">σ₃</text><rect class="dim" opacity="0.45" x="270" y="157.5" width="44" height="12.5" rx="3"/><text class="ink" x="292" y="151.5" font-size="12" text-anchor="middle">1</text><text class="ink" x="292" y="188" font-size="13" text-anchor="middle">σ₄</text><line class="line" x1="40" y1="170" x2="340" y2="170"/><text class="ink" x="190" y="214" font-size="12" text-anchor="middle">The first two hold 94% of the energy: (144 + 25) / 179</text></svg>
  <figcaption>In a matrix with singular values 12, 5, 3 and 1, the first two layers carry 169 of the sum of squares (179): the rank-2 approximation keeps 94% of the matrix, and the error of the dropped part is $\sqrt{9 + 1} \approx 3.16$.</figcaption>
</figure>

### Image compression

A greyscale photo is an $m \times n$ matrix. Storing all of it takes $m
\cdot n$ numbers. To store the first $k$ layers, each layer needs one
$\mathbf{u}_i$ ($m$ numbers), one $\mathbf{v}_i$ ($n$ numbers) and one
$\sigma_i$:

$$
k\,(m + n + 1) \text{ numbers}
$$

For a $1000 \times 1000$ photo with $k = 50$ that is $50 \cdot 2001 = 100\,050$
numbers; about a tenth of the original. In real photos the singular
values shrink fast ($\sigma_{50}$ is tiny next to $\sigma_1$), so the eye
can hardly tell the difference.

## SVD in machine learning

**PCA.** The SVD of the mean-centred data matrix $X$ gives PCA directly:
the $\mathbf{v}_i$ are the principal directions (components) of the data,
and $\sigma_i^2 / (n - 1)$ is the variance in that direction. Libraries
compute PCA with the SVD rather than with the eigenvalues of the covariance
matrix; it is numerically more stable.

**Recommendation systems.** A low-rank approximation of the user × film
rating matrix: every user and every film is described by a few "hidden
features" (amount of action, romance, …). The $\mathbf{u}_i$ hold the
users' weights on these features, the $\mathbf{v}_i$ the films'. Empty
cells (films not watched) are predicted with this approximation.

**Meaning in text.** The SVD of a document × word count matrix (latent
semantic analysis): words that occur together in the same layer, such as
"car" and "automobile", end up with nearby vectors.

**Noise removal.** In data, the real structure sits in the large singular
values, while random noise is spread over many small ones. Dropping the
small layers removes most of the noise.

**Numerical rank.** In real data singular values never come out exactly
zero; very small values like $10^{-12}$ count as "really zero". The
`matrix_rank` functions of libraries find the rank this way, by looking
at the singular values.

## Common mistakes

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Wrong</h4>
      <p>Singular values = the eigenvalues of $A$</p>
      <p>The SVD exists only for square matrices</p>
      <p>A singular value can be negative</p>
      <p>$\sigma_i$ = the eigenvalues of $A^\mathsf{T}A$</p>
    </div>
    <div class="ok">
      <h4>Right</h4>
      <p>Singular values = square roots of the eigenvalues of $A^\mathsf{T}A$</p>
      <p>Every $m \times n$ matrix has an SVD</p>
      <p>$\sigma_i \ge 0$, sorted from largest to smallest</p>
      <p>$\sigma_i^2$ = the eigenvalues of $A^\mathsf{T}A$</p>
    </div>
  </div>
  <figcaption>Singular values and eigenvalues coincide only for symmetric matrices with non-negative eigenvalues.</figcaption>
</figure>

- **Forgetting the square root.** The eigenvalues of $A^\mathsf{T}A$ are
  the squares of the singular values; take the square root for $\sigma$.
- **Leaving $\mathbf{u}_i$ undivided.** $A\mathbf{v}_i$ has length
  $\sigma_i$; $\mathbf{u}_i$ must be a unit vector.
- **Keeping the smallest singular values in a low-rank approximation.** The
  large ones matter; the small ones are dropped.

## Summary

- For every matrix, $A = U\Sigma V^\mathsf{T}$: rotate ($V^\mathsf{T}$), stretch along the axes ($\Sigma$), rotate ($U$).
- $A\mathbf{v}_i = \sigma_i\mathbf{u}_i$; the unit circle goes to an ellipse with semi-axes $\sigma_i$.
- Computation: the eigenvalues of $A^\mathsf{T}A$ are $\sigma_i^2$, its eigenvectors $\mathbf{v}_i$; $\mathbf{u}_i = A\mathbf{v}_i / \sigma_i$.
- Rank = number of non-zero $\sigma$; $\|A\| = \sigma_1$; for square matrices $|\det A| = \prod \sigma_i$; condition number $\sigma_1 / \sigma_n$.
- $A = \sum \sigma_i \mathbf{u}_i\mathbf{v}_i^\mathsf{T}$: rank-1 layers in order of importance.
- The first $k$ layers are the best rank-$k$ approximation (Eckart–Young); error $\sqrt{\sigma_{k+1}^2 + \cdots}$; energy share $\sum_{i \le k} \sigma_i^2 / \sum \sigma_i^2$.
- Storage: $k(m + n + 1)$ numbers.
- ML: PCA, recommendation systems, meaning in text, noise removal, numerical rank.
