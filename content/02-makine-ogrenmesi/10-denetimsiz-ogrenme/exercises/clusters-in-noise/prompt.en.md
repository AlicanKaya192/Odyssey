In the third exercise the silhouette came out as 0.525. **Is that good?**

You cannot answer that — good against what? In this exercise you will build
the reference.

**The method:** generate random data of the same shape with the same number
of columns and **no structure at all**, then apply the same clustering to
it.

**What you need to do:**

1. Prepare and scale the data.
2. With `numpy.random.default_rng(0)`, generate a standard normal noise
   array of **the same shape** as `X_scaled`.
3. Try `k` from **2 to 5**. Print one line per `k`: **k, the real data's
   silhouette, the noise's silhouette** (three decimals).
4. Print the cluster sizes found in the noise at `k=4`, as a sorted list.
5. On the last line print the ratio of the two silhouettes at `k=4` (one
   decimal).

**Expected output:**

```
2 0.514 0.169
3 0.525 0.176
4 0.517 0.181
5 0.489 0.185
[80, 82, 94, 94]
2.9
```

**Look at the fourth line: there are four clusters in the noise.** Their
sizes even look reasonable — 80, 82, 94, 94. There are no groups there at
all, and the model returned four anyway.

**The first lesson: returning clusters is not proof that clusters exist.**
The algorithm partitions whatever you give it. "I ran KMeans and found four
clusters" says nothing.

**The second lesson: watch the noise column.** 0.169 → 0.176 → 0.181 →
0.185: the silhouette **rises** as `k` grows. So "pick the `k` that
maximises the silhouette" is not a method; it gives a peak even on noise.

**The last line: 2.9.** The real data's silhouette is about **three times**
the noise's. That ratio is the actual information, not the number 0.517.

Had the two come out close — say 0.22 against 0.18 — you would have to
conclude the clusters are arbitrary partitions the algorithm handed you.

**But a number alone is still not enough.** The real test of whether the
clusters exist is in the first exercise's table: **can you give every row a
name?** If you can say "the group that visits often and buys little", the
cluster is saying something.
