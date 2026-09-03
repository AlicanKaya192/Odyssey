In section 06 you measured that scaling is mandatory for KNN, and in
section 07 that it is pointless for a tree. Which side is k-means on?

**What you need to do:**

1. Read the data and take the four columns. Prepare a scaled copy too.
2. With the same settings (`n_clusters=4`, `random_state=42`, `n_init=10`)
   run **two clusterings**: one on the **raw** data and one on the scaled
   data.
3. Print one line each: **the name, the cluster sizes (sorted list), the
   silhouette**. Compute both silhouettes in the **scaled** space —
   otherwise they are not comparable.
4. Print the raw clustering's profile table (the `spend` and `visits`
   means, one decimal).
5. On the last line print the `adjusted_rand_score` between the two
   clusterings (three decimals).

**Expected output:**

```
raw [33, 47, 95, 175] 0.202
scaled [70, 79, 99, 102] 0.517
         spend  visits
cluster
0         52.4     9.8
1        481.5    15.2
2        184.5     8.4
3        348.4    14.9
0.602
```

**The silhouette falls from 0.517 to 0.202.** But the sizes tell the real
story.

**Scaled:** 70, 79, 99, 102 — four balanced groups.

**Raw:** 33, 47, 95, **175**. One cluster swallowed half the data.

The profile table says what happened: the raw clustering **merged two real
groups into a heap of 175** (cluster 0: spend 52.4, visits 9.8 — the mean
of the "rare visitor" and "frequent browser" groups from the first
exercise). In exchange it **split the high spenders in two**: 481.5 and
348.4. Their visit counts are nearly identical (15.2 and 14.9) — so the
split rests entirely on the `spend` column.

**The reason fits in one line:** `spend` has a spread of 155 and `returns`
of 1.5. In the distance computation `spend` weighs a hundred times more.
Instead of four real groups the model finds **four slices of one column**.

**The last line: ARI 0.602.** Because cluster numbers change with the seed,
you cannot compare two clusterings by their labels.
`adjusted_rand_score` asks "are these two records in the same cluster in
both". 1.0 means exactly the same grouping; 0.602 means **two genuinely
different groupings** — not merely shifted numbers.
