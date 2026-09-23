Search systems often turn every vector into a unit vector once, then compute only dot products.

**1. Unit vectors:**

$$
\hat{\mathbf{q}} = \frac{(1,\ 1,\ 0)}{\sqrt{2}} \approx (0.707,\ 0.707,\ 0)
$$

$$
\hat{D}_1 = \frac{(2,\ 2,\ 1)}{3} \approx (0.667,\ 0.667,\ 0.333)
$$

$$
\hat{D}_2 = \frac{(0,\ 6,\ 8)}{10} = (0,\ 0.6,\ 0.8)
$$

**2. Between unit vectors, cosine = dot product:**

$$
\hat{\mathbf{q}} \cdot \hat{D}_1 \approx 0.707 \cdot 0.667 + 0.707 \cdot 0.667 \approx 0.94
$$

$$
\hat{\mathbf{q}} \cdot \hat{D}_2 \approx 0.707 \cdot 0.6 \approx 0.42
$$

With millions of documents this arrangement pays off: the documents are normalised once and every search is just multiply and add.

**Answer: $0.94$ and $0.42$**
