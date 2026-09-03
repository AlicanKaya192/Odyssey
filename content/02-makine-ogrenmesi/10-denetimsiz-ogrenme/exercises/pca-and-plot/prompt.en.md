You cannot put four-column data on paper. **Principal component
analysis** (PCA) exists for exactly this: turning four columns into two
while losing as little information as possible.

**What you need to do:**

1. Prepare and scale the data. (Since PCA works on variance, scaling is
   mandatory here too.)
2. Compute **every** component and print the cumulative explained variance
   as a list of three-decimal values.
3. Refit with two components and transform. Print the two components'
   weights on separate lines (three decimals, in column order `spend`,
   `visits`, `items`, `returns`).
4. Run `KMeans(n_clusters=4, random_state=42, n_init=10)` **separately** in
   the full space and in the PCA space. Print the two silhouettes side by
   side (three decimals).
5. Print the `adjusted_rand_score` between the two clusterings.
6. Draw the PCA-space points as a scatter, **coloured by the full-space
   cluster label**. Label the axes `pc1` and `pc2`, add a title, and save
   as `chart.png`.

**Expected output:**

```
[0.662, 0.885, 0.973, 1.0]
[0.531, 0.426, 0.54, 0.495]
[-0.471, 0.659, -0.425, 0.403]
0.517 0.652
1.0
```

**The first line: two components carry 88.5% of the variance.** We turned
four columns into two and lost 11.5% of the information.

**The second line — the first component:** all four positive and close to
each other (0.531, 0.426, 0.540, 0.495). That axis is "overall activity":
the further right, the more a customer does of everything.

**The third line — the second component:** `visits` (0.659) and `returns`
(0.403) positive, `spend` (−0.471) and `items` (−0.425) negative. That axis
is precisely **"comes often but buys little"**. What separates cluster 2
from the first exercise is written right here.

**PCA found that axis without seeing a single label.** Nobody told it to
separate the browsers; it merely looked for the directions carrying the
most variance, and the second came out as this.

**The fourth line: 0.517 and 0.652.** The silhouette rises after PCA — **but
do not be fooled.** A higher silhouette does not show the clusters are
better, only that they were **measured in fewer dimensions**. The two
discarded dimensions were the noise that blurred the clusters together;
drop them and the same groups merely *look* tidier. Silhouettes from spaces
of different dimension are not comparable.

**The fifth line proves it: ARI 1.0.** The grouping is identical. Two
columns were thrown away and **not one customer moved.**

In the chart you will see the four clusters separate. That is PCA's real
benefit here: you cannot put four-dimensional data on paper, but you can
put two.

**The cost is interpretability.** The new columns are called `pc1` and
`pc2`; they are mixtures of the four original ones. A sentence like "as
spend rises, this happens" can no longer be written.
