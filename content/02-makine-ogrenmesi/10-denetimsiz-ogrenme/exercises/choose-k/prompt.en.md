`n_clusters` is an input. So what number do you write? There are two
tools, and in this exercise you will build both.

**What you need to do:**

1. Prepare and scale the data.
2. Try `k` from **2 to 8** (inclusive). Print one line each: **k, the
   inertia (one decimal), the silhouette (three decimals)**.
3. Draw the two curves **side by side**: inertia on the left, silhouette on
   the right. Label the axes `k` and `inertia` / `silhouette`, add titles,
   and save as `chart.png`.
4. On the last line print **the `k` giving the highest silhouette** and
   that silhouette, side by side.

**Expected output:**

```
2 695.9 0.514
3 388.8 0.525
4 265.6 0.517
5 212.7 0.489
6 189.6 0.457
7 167.3 0.442
8 155.4 0.415
3 0.525
```

**The inertia column always falls.** It would be zero if `k` equalled the
record count — so "the lowest inertia" is not a target. What you look for
is **where it slows down**: 695.9 → 388.8 → 265.6 are large drops, then
212.7 → 189.6 → 167.3 slows. This is the **elbow method**, and the elbow
here sits between 3 and 4.

**The silhouette says `k=3`.** But this data was generated from **four
groups**.

The silhouette is not wrong; it answers its own question correctly. Its
question is "how tidy are the clusters", not "how many real groups are
there". Cluster 1 (the rare visitors) and cluster 2 (the frequent
browsers) from the first exercise sit close together in space; merging into
three raises the silhouette by 0.008 and **loses a distinction that matters
to the business.**

The gap between 0.525 and 0.517 is no larger than the measurement noise
anyway.

**The conclusion: `k` is not a measurement result but a decision.** The two
tools narrow the range — 3 to 4, not 2 to 8. A person reading the profile
table picks the rest.
