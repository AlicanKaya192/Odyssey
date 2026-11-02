# Random Assignment

The power of an A/B test comes from one idea: **chance** decides who sees A
and who sees B. Then the two groups are the same on average in every
respect except the change, and the difference between them can be put down
to the change. This section shows what happens when assignment is not
random, and how random assignment is done in a real system.

## Groups that choose themselves: selection bias

Say the shop offers a new feature as "turn it on if you like". The feature
actually **does nothing**. But frequent users notice it more and turn it
on:

```python
import numpy as np
from ab_data import make_user_log

users = make_user_log()
rng = np.random.default_rng(81)
opted = rng.random(len(users)) < np.clip(0.05 * users["sessions"], 0, 0.9)
print(round(opted.mean(), 3))
print(round(users["bought"][opted].mean(), 4),
      round(users["bought"][~opted].mean(), 4))
print(round(users["sessions"][opted].mean(), 2),
      round(users["sessions"][~opted].mean(), 2))
```

```text
0.185
0.163 0.107
6.15 3.21
```

Those who turned the feature on bought 5.6 points more. It
is very easy to say "the feature raises sales", but it is wrong: the ones
who turned it on were already more frequent visitors (last line). The
difference comes not from the feature but from **who chose it**. This is
called **selection bias**; the number of visits is a **confounder** here:
it affects both the choice and the result.

## When chance decides

Let's split the same users with a coin flip:

```python
in_b = rng.random(len(users)) < 0.5
print(round(in_b.mean(), 3))
print(round(users["bought"][in_b].mean() - users["bought"][~in_b].mean(), 4))
print(round(users["sessions"][in_b].mean(), 2),
      round(users["sessions"][~in_b].mean(), 2))
```

```text
0.5
0.0005
3.75 3.75
```

The visit counts are almost equal and the buying difference is small. Let's
not trust a single split; do the same 500 times:

```python
diffs = []
for _ in range(500):
    in_b = rng.random(len(users)) < 0.5
    diffs.append(users["bought"][in_b].mean() - users["bought"][~in_b].mean())
print(round(float(np.mean(diffs)), 4), round(float(np.std(diffs)), 4))
```

```text
0.0002 0.0046
```

Over random splits the difference is zero on average and typically moves by
only 0.0046: that is exactly the standard error from the
Estimation and Standard Error section. The difference in the self-chosen
groups is 12 times that. With random assignment every
difference between the groups comes either from the change or from chance,
and we can compute how much chance moves things. Hypothesis tests rest on
exactly this.

## Assignment in a real system: a hash function

On a live site, using `rng.random()` causes problems: the same person may
see another group after reloading the page. Instead a **hash** of the
user's id is computed and turned into a **bucket** from 0 to 99:

<figure class="fig">
  <div class="flow">
    <span class="node">Salt<br><small>checkout-v2</small></span><span class="arrow">→</span>
    <span class="node">Id<br><small>U00001</small></span><span class="arrow">→</span>
    <span class="node">MD5 hash</span><span class="arrow">→</span>
    <span class="node">Bucket<br><small>0–99</small></span><span class="arrow">→</span>
    <span class="node acc">Group<br><small>B if &lt;50</small></span>
  </div>
  <figcaption>The same id and the same salt always land in the same bucket; buckets are spread evenly and independently of the id.</figcaption>
</figure>

```python
import hashlib


def bucket(user_id, salt):
    digest = hashlib.md5(f"{salt}:{user_id}".encode()).hexdigest()
    return int(digest, 16) % 100


print(bucket("U00001", "checkout-v2"), bucket("U00001", "checkout-v2"))
in_b = np.array([bucket(u, "checkout-v2") < 50 for u in users["user_id"]])
users["group"] = np.where(in_b, "B", "A")
users["mobile"] = (users["platform"] == "mobile").astype(int)
summary = users.groupby("group")[["sessions", "mobile", "bought"]].mean()
print(summary.round(3))
print(users["group"].value_counts().sort_index().to_dict())
```

```text
41 41
       sessions  mobile  bought
group                          
A         3.774   0.605   0.119
B         3.732   0.604   0.116
{'A': 10107, 'B': 9893}
```

- The same person lands in the same bucket every time: reloading the page
  does not change the group.
- The two groups' visit counts, mobile shares and buying rates are very
  close: the assignment is unrelated to the users' traits. This table is
  called a **balance table**; it is one of the first things to look at in
  every experiment.
- The group sizes are not exactly 50/50; a deviation that small is chance.
  How much deviation cannot be chance we will see in the A/A Tests and
  Sample Ratio Mismatch section.

`md5` is used here not for security but to turn the id into an evenly
spread number. Python's built-in `hash()` gives a different result for
strings on every run (designed that way for security), so it is not used
for assignment.

## The salt: keeping experiments apart

The **salt** is the experiment's name. If two experiments run at the same
time, each uses its own salt:

```python
other = np.array([bucket(u, "search-v3") < 50 for u in users["user_id"]])
print(round(float(np.mean(in_b == other)), 3))
```

```text
0.504
```

The share of users who see the same group in both experiments is about
half: the two assignments are independent. If the two experiments used the
same salt this share would be 1: everyone in the first experiment's B group
would also be in the second's B group, and the two changes' effects could
not be told apart.

## The unit of assignment

What gets randomised is also a decision:

- **User:** the most common. A person sees the same version on every visit.
- **Session or page view:** gives more observations, but the same person
  can see both versions; for changes that alter a person's behaviour the
  results get mixed.
- **Larger units** (city, store, class): needed when users affect one
  another; in the Network Effects and Interference section.

The analysis is done at the same level as the unit of assignment: assigning
by user and then counting each page view as a separate observation ignores
that the observations are not independent and makes p-values too small.

## Summary

- In self-chosen groups the difference can come from variables that affect
  the choice (selection bias).
- With random assignment the difference comes either from the change or
  from chance that can be computed.
- Live assignment uses `hash(salt + id) % 100`: stable and balanced.
- Each experiment has its own salt; the balance table is always checked.
- The analysis is done at the same level as the unit of assignment.
