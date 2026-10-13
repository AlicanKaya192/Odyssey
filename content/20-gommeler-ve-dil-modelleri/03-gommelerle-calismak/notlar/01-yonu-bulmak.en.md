In the lesson we built the gender direction from the average of the
differences of ten word pairs. Why not just "she − he"? Let us compare the
two with the lesson's `E`, `pairs`, `jobs` and `skew`:

```python
for name, chosen in [("she - he", [("he", "she")]), ("all pairs", pairs)]:
    g = np.mean([E[index[f]] - E[index[m]] for m, f in chosen], axis=0)
    g = g / np.linalg.norm(g)
    proj = np.array([E[index[j]] @ g for j in jobs])
    print(name, round(float(np.corrcoef(proj, skew)[0, 1]), 3))
```

```text
she - he -0.708
all pairs 0.997
```

- The direction built from one pair shows the bias **reversed** (−0.708). The
  vectors of "she" and "he" carry not only gender but also the particular use
  of these two words ("she cooked", "he is a man"...). The difference vector
  contains that noise too.
- In the average of ten pairs the particular noise of each pair cancels out
  and what they share, gender, remains: the correlation is 0.997.
- Bolukbasi and colleagues (2016) also extracted the direction from the
  differences of many pairs (with PCA). Check that the direction you measure
  really is what you want to measure; here we did it by comparing with the
  shares in the data.
