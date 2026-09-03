For the first time in this module you have no `y`. There are four columns
for 350 customers and nobody labelled "this customer is of that type".

The question: **how many groups do these people fall into, and what
separates the groups?**

**What you need to do:**

1. Read the data, take the four columns (`spend`, `visits`, `items`,
   `returns`) and **scale** them. K-means rests on distance — just like
   KNN.
2. Cluster with `KMeans(n_clusters=4, random_state=42, n_init=10)`.
3. Print the cluster sizes as a list.
4. Make the labels a column called `cluster` and print the **profile
   table**: the mean of the four columns per cluster (one decimal).
5. On the last line print the silhouette score (three decimals).

**Expected output:**

```
[79, 102, 70, 99]
         spend  visits  items  returns
cluster
0        428.2    15.2   23.4      3.3
1         45.8     3.2    4.2      0.3
2         63.9    19.3    6.4      2.6
3        180.2     8.4   11.3      1.1
0.517
```

**This table is the exercise's real output.** The cluster numbers say
nothing; the means say everything:

- **Cluster 1** — comes rarely, spends little. 102 people.
- **Cluster 3** — mid-level, regular. 99 people.
- **Cluster 0** — spends a lot, buys a lot. 79 people.
- **Cluster 2 is the interesting one.** Its spend is as low as cluster 1's
  (63.9) yet it visits **19 times** a month and makes 2.6 returns. Someone
  who comes often, browses a lot, buys little and sends back what they buy.
  70 people.

**You could not have found cluster 2 by eye.** Look at `spend` and it looks
like cluster 1; look at `visits` and it looks like cluster 0. It only
separates when all four are read at once. That is exactly what clustering
is for.

**The silhouette is 0.517.** For now you have no idea whether that is good
or bad — good against what? You will measure the reference in the fourth
exercise.

**Note:** `n_clusters` is not a hyperparameter but an **input**. You told
the model "find four groups" and it found four. Had you said three it would
have found three; it has no notion of how many groups the data holds.
