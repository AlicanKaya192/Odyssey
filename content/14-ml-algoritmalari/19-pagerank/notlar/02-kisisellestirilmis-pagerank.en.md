In the lesson the bored surfer jumped to **any** page (`(1 − d) / n`). If the
jump goes only to certain pages, we get **personalised PageRank**: the result
no longer shows pages that are "important in general" but those "close to
this page and important". It is used in recommender systems and "more like
this" searches.

With the lesson's `M`, let the bored surfer always return to D:

```python
v = np.zeros(n)
v[idx["D"]] = 1                          # jumps go only to D
rp = np.full(n, 1 / n)
for _ in range(200):
    rp = 0.85 * M @ rp + 0.15 * v
print(show(rp))
print(show(pagerank(M)[0]))
```

```text
A=0.292 B=0.124 C=0.343 D=0.150 E=0.064 F=0.027
A=0.347 B=0.173 C=0.379 D=0.025 E=0.036 F=0.040
```

In general PageRank D's value is 0.025, in the personalised one 0.15: the
surfer keeps returning there. E rises from 0.036 to 0.064 because it is D's
direct neighbour. F falls from 0.040 to 0.027: it is two steps away from D and
no longer gets the random-jump share it had in general PageRank. The order of
A, B and C does not change; D's links eventually flow to them too.

In a recommender system `v` is spread over the items a person liked; nodes
with high values that the person has not seen yet are recommended.
