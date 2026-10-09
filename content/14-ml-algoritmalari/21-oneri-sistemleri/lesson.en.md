# Recommender Systems

A system that recommends films, music or products holds a **rating matrix**:
rows are users, columns are items, cells are ratings. Most of the matrix is
**empty**: nobody watched every film. The recommender's job is to predict the
empty cells and recommend to each person the items with the highest
predictions that they have not seen yet. In this section we start from simple
baselines and write **collaborative filtering** and **matrix factorisation**
from scratch.

## The rating matrix and baselines

We generate the data with a hidden structure: every user and every item has a
2-dimensional hidden "taste" vector; a rating depends on how well the two
match, on the item's general appeal and on the user's generosity. 200 users,
100 items; each user rated about a fifth of the items. 80% of the ratings are
for training, 20% for testing.

```python
import numpy as np

rng = np.random.default_rng(21)
n_users, n_items = 200, 100
U_true = rng.normal(0, 1, (n_users, 2))          # hidden tastes (2 dims)
V_true = rng.normal(0, 1, (n_items, 2))
item_bias = rng.normal(0, 0.7, n_items)
user_bias = rng.normal(0, 0.5, n_users)
signal = U_true @ V_true.T * 0.7 + item_bias + user_bias[:, None]
true = np.clip(3 + signal, 1, 5)
seen = rng.random((n_users, n_items)) < 0.2
noisy = np.clip(np.round(true + rng.normal(0, 0.4, true.shape)), 1, 5)
R = np.where(seen, noisy, 0)                     # 0 = no rating

obs = np.argwhere(R > 0)
rng.shuffle(obs)
cut = int(len(obs) * 0.8)
train, test = obs[:cut], obs[cut:]
Rtr = np.zeros_like(R)
Rtr[train[:, 0], train[:, 1]] = R[train[:, 0], train[:, 1]]
mask = Rtr > 0


def rmse(pred):
    errors = [(R[u, i] - pred(u, i)) ** 2 for u, i in test]
    return round(float(np.sqrt(np.mean(errors))), 3)


mu = Rtr[mask].mean()
item_mean = np.array([Rtr[mask[:, i], i].mean() for i in range(n_items)])
bu, bi = np.zeros(n_users), np.zeros(n_items)
for _ in range(20):                              # user and item biases
    bi = ((Rtr - mu - bu[:, None]) * mask).sum(axis=0) / (mask.sum(axis=0) + 5)
    bu = ((Rtr - mu - bi) * mask).sum(axis=1) / (mask.sum(axis=1) + 5)
print(len(obs), round(len(obs) / R.size, 3), len(train), len(test))
print(round(mu, 3), rmse(lambda u, i: mu), rmse(lambda u, i: item_mean[i]))
print(rmse(lambda u, i: mu + bu[u] + bi[i]))
```

```text
3928 0.196 3142 786
3.08 1.156 1.003
0.93
```

Only 3928 of the 20 000 cells are filled (19.6%). The measure is **RMSE**: the
square root of the mean squared prediction error on the test ratings. Telling
everyone the mean (3.08) gives an error of 1.156. The item's mean gives 1.003.
The baseline that learns user and item **biases** together gets 0.93: some
users give everything high ratings, some items everyone likes. To keep the
biases of users and items with few ratings from overfitting, 5 was added to
the denominator (regularisation).

## User-based collaborative filtering

The idea: what did users with tastes like mine rate this item? The similarity
of two users is the cosine similarity of their **deviations** from their own
means. The prediction: my own mean + the similarity-weighted average of the
deviations of my `k` most similar neighbours (who rated this item).

```python
means = np.array([Rtr[u, mask[u]].mean() for u in range(n_users)])
C = np.where(mask, Rtr - means[:, None], 0)      # deviations from the mean
norms = np.linalg.norm(C, axis=1)
norms[norms == 0] = 1
S = C @ C.T / np.outer(norms, norms)             # cosine similarity
np.fill_diagonal(S, 0)


def user_cf(u, i, k):
    raters = np.where(mask[:, i])[0]
    top = raters[np.argsort(-S[u, raters])[:k]]  # the k most similar
    w = S[u, top]
    if np.abs(w).sum() == 0:
        return means[u]
    return np.clip(means[u] + (w * C[top, i]).sum() / np.abs(w).sum(), 1, 5)


for k in (5, 10, 20):
    print(k, rmse(lambda u, i: user_cf(u, i, k)))
```

```text
5 0.816
10 0.803
20 0.817
```

With 10 neighbours the error is 0.803: clearly better than the bias
baseline. Few neighbours are noisy, many neighbours bring in dissimilar users
too; `k` is again chosen with cross-validation.

## Matrix factorisation

When generating the data we gave each user and item a hidden vector. **Matrix
factorisation** does this in reverse: it writes the rating matrix as the
product of two thin matrices, `R ≈ μ + b_u + b_i + P Qᵀ`. Each row of `P` is a
user's `k`-dimensional hidden vector, each row of `Q` an item's. Only over the
**filled** cells, at every rating a small step is taken in the direction that
reduces the error (stochastic gradient descent):

```python
def factorize(k, epochs, lr=0.02, reg=0.05, seed=0):
    r = np.random.default_rng(seed)
    P = r.normal(0, 0.1, (n_users, k))
    Q = r.normal(0, 0.1, (n_items, k))
    bu, bi = np.zeros(n_users), np.zeros(n_items)
    for _ in range(epochs):
        for u, i in r.permutation(train):
            err = R[u, i] - (mu + bu[u] + bi[i] + P[u] @ Q[i])
            bu[u] += lr * (err - reg * bu[u])
            bi[i] += lr * (err - reg * bi[i])
            P[u], Q[i] = (P[u] + lr * (err * Q[i] - reg * P[u]),
                          Q[i] + lr * (err * P[u] - reg * Q[i]))
    return lambda u, i: mu + bu[u] + bi[i] + P[u] @ Q[i]


models = {}
for k in (1, 2, 5, 20):
    models[k] = factorize(k, 50)
    fit = np.sqrt(np.mean([(R[u, i] - models[k](u, i)) ** 2 for u, i in train]))
    print(k, round(float(fit), 3), rmse(models[k]))
```

```text
1 0.624 0.762
2 0.454 0.628
5 0.374 0.648
20 0.241 0.666
```

With `k = 2` the test error is 0.628: the best of all methods. This is no
coincidence; the data was generated with 2-dimensional hidden tastes and the
factorisation found that structure. `k = 1` is not enough to capture it
(0.762). As `k` grows the training error keeps falling (0.241 at 20) but the
test error rises again (0.666): too many dimensions memorise the noise.

<figure class="fig">
<svg viewBox="0 0 500 210" width="500" xmlns="http://www.w3.org/2000/svg"><text class="ink" x="180" y="36" font-size="12" text-anchor="end">global mean</text><rect class="dot2" x="190" y="24" width="265.9" height="18" rx="3" fill-opacity=".85"/><text class="dim" x="463.9" y="37" font-size="12">1.156</text><text class="ink" x="180" y="70" font-size="12" text-anchor="end">item mean</text><rect class="dot2" x="190" y="58" width="230.7" height="18" rx="3" fill-opacity=".85"/><text class="dim" x="428.7" y="71" font-size="12">1.003</text><text class="ink" x="180" y="104" font-size="12" text-anchor="end">biases</text><rect class="dot2" x="190" y="92" width="213.9" height="18" rx="3" fill-opacity=".85"/><text class="dim" x="411.9" y="105" font-size="12">0.93</text><text class="ink" x="180" y="138" font-size="12" text-anchor="end">user CF (k=10)</text><rect class="dot2" x="190" y="126" width="184.7" height="18" rx="3" fill-opacity=".85"/><text class="dim" x="382.7" y="139" font-size="12">0.803</text><text class="ink" x="180" y="172" font-size="12" text-anchor="end">matrix factorisation (k=2)</text><rect class="dot" x="190" y="160" width="144.4" height="18" rx="3" fill-opacity=".85"/><text class="dim" x="342.4" y="173" font-size="12">0.628</text></svg>
<figcaption>Test error of five methods (RMSE, smaller is better). Each step adds something to the previous idea: biases, similar users, hidden tastes.</figcaption>
</figure>

## The recommendation list

The real job is not predicting a rating but choosing **what to recommend**.
For each user we recommend the 5 items with the highest predictions among
those they have not rated, and check how many of them are really among the 5
items that user would like most (we know the true tastes, since we generated
the data):

```python
def precision_at_5(u, scores):
    unseen = np.where(~seen[u])[0]
    best = set(unseen[np.argsort(-true[u, unseen])[:5]])
    picked = unseen[np.argsort(-scores[unseen])[:5]]
    return len(best & set(picked)) / 5


best_model = models[2]
full = np.array([[best_model(u, i) for i in range(n_items)]
                 for u in range(n_users)])
for name, scores in (("mf", lambda u: full[u]), ("popular", lambda u: item_mean),
                     ("random", lambda u: rng.random(n_items))):
    hits = [precision_at_5(u, scores(u)) for u in range(n_users)]
    print(name, round(float(np.mean(hits)), 3))
```

```text
mf 0.593
popular 0.331
random 0.068
```

Close to 3 of matrix factorisation's 5 recommendations are, on average, among
the person's true top 5 (0.593). Recommending the most liked items to everyone
stays at 0.331, random recommendations at 0.068. Personalisation gives about
1.8 times the hits of popularity.

## Summary

- A recommender predicts the empty cells of a sparse rating matrix and
  recommends the highest ones.
- Baselines: the global mean, the item mean, user + item biases.
- User-based collaborative filtering: the weighted average of similar users'
  deviations.
- Matrix factorisation: `R ≈ μ + b_u + b_i + P Qᵀ`, SGD over the filled cells
  only; `k` and regularisation decide overfitting.
- Evaluation is not only RMSE; the hit rate of the recommended list
  (precision@k) is measured too.
