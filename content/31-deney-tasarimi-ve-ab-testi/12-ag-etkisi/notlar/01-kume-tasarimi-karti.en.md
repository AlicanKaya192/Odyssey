## The cost of cluster assignment: the design effect

Users in the same cluster resemble each other. This resemblance is
measured by the **intraclass correlation** (ICC): 0 means everyone in the
cluster is independent, 1 means everyone in the cluster is the same. The
variance of a test assigned by cluster grows, compared with a test where
the same number of users is assigned one by one, by the **design effect**:

$$\text{DEFF} = 1 + (m - 1)\,\text{ICC}$$

Here m is the number of users per cluster. The effective sample is
n / DEFF.

```python
def design_effect(cluster_size, icc):
    return 1 + (cluster_size - 1) * icc


for icc in [0.0, 0.01, 0.05]:
    deff = design_effect(300, icc)
    print(icc, round(deff, 2), round(30000 / deff))
```

```text
0.0 1.0 30000
0.01 3.99 7519
0.05 15.95 1881
```

With 300 users per city, even an ICC of only 0.01 means 30,000 users carry
about as much information as 7,500 independent users.

## Analysis in a cluster test

- The unit is the cluster: each cluster's mean is one observation.
- A Welch test between clusters or a cluster-level bootstrap.
- Testing users as if independent is the same mistake as in the Ratio
  Metrics and the Delta Method section: a small standard error, too many
  alarms.

## Number of clusters

What reduces the noise is not the size of the clusters but **the number of
clusters**. 10 huge cities carry less information than 100 small ones.
