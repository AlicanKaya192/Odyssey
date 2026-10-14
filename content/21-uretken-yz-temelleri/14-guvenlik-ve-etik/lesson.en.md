# Safety, Bias and Responsibility

Generative models learn from data; they also learn the unfairness, the
personal information and the errors in the data. This section deals with three
risks by measuring them: **bias** (does the model systematically disadvantage
a group?), **personal data** (does identifying information leak in the text?)
and **responsibility** (who checks the system, and how?). Attacks made through
the prompt (prompt injection) are Module 2's topic.

## Bias comes from the data

A company wants to train a model that screens candidates using its past hiring
decisions. Let us build synthetic data: the candidates' real ability
(`skill`), their experience measured noisily from it, a group label (A or B)
and a feature strongly related to the group: membership of a club (80% in
group B, 20% in A). A candidate is **truly suitable** if their skill passes a
certain threshold. But past decisions were biased against group B:

```python
import numpy as np
from sklearn.linear_model import LogisticRegression


def make_applicants(n, seed):
    rng = np.random.default_rng(seed)
    group = rng.integers(0, 2, n)
    skill = rng.normal(0, 1, n)
    club = (rng.random(n) < np.where(group == 1, 0.8, 0.2)).astype(int)
    experience = skill + rng.normal(0, 0.8, n)
    suitable = (skill > 0.3).astype(int)
    noise = rng.normal(0, 0.5, n)
    hired = (skill - 0.8 * group + noise > 0.3).astype(int)
    X = np.column_stack([experience, club, group])
    return X, group, suitable, hired


X, group, suitable, hired = make_applicants(4000, 0)
X_test, g_test, s_test, _ = make_applicants(4000, 1)
for k, name in [(0, "A"), (1, "B")]:
    print(name, "suitable", suitable[group == k].mean().round(2),
          "hired in the past", hired[group == k].mean().round(2))
```

```text
A suitable 0.37 hired in the past 0.37
B suitable 0.4 hired in the past 0.17
```

The share of suitable candidates is close in the two groups (37% and 40%);
the past hiring rate in B is less than half of A's. If we train the model on
these past decisions, what does it learn?

## Removing the group is not enough

We train three models: with all features, with the group column removed, and
with experience only. For each we look at two things: each group's
**selection rate** and the selection rate of the **truly suitable**
candidates (equal opportunity).

```python
def report(name, chosen):
    rates = []
    for k in (0, 1):
        sel = chosen[g_test == k].mean()
        fair = chosen[(g_test == k) & (s_test == 1)].mean()
        rates.append(f"{sel:.2f}/{fair:.2f}")
    print(f"{name:16} A {rates[0]}  B {rates[1]}")


for name, cols in [("all features", [0, 1, 2]),
                   ("without group", [0, 1]),
                   ("experience only", [0])]:
    model = LogisticRegression().fit(X[:, cols], hired)
    report(name, model.predict(X_test[:, cols]))
```

```text
all features     A 0.33/0.67  B 0.10/0.24
without group    A 0.24/0.52  B 0.15/0.35
experience only  A 0.17/0.40  B 0.18/0.41
```

The model trained with all features learns the history's bias: 67% of the
suitable candidates are selected in A, 24% in B. Removing the group column
narrows the gap but does not close it (52% against 35%): club membership gives
the group away, and the model carries the bias on through it. Such a feature
is called a **proxy variable**. With experience only the gap closes (40%
against 41%); but in group A the selection rate of suitable candidates falls
from 52% to 40%: the model has less information and the labels still come from
the biased history. In real data proxies are not always this visible (address,
school, gap years).

## A correction and its price

One way is to lower the threshold for group B until the selection rate of
suitable candidates is equal in both groups. The group label does not go into
the model, but it is used at the decision step:

```python
model = LogisticRegression().fit(X[:, [0, 1]], hired)
p = model.predict_proba(X_test[:, [0, 1]])[:, 1]
target = (p >= 0.5)[(g_test == 0) & (s_test == 1)].mean()
best = min(np.arange(0.20, 0.51, 0.01), key=lambda t: abs(
    (p >= t)[(g_test == 1) & (s_test == 1)].mean() - target))
print("threshold for B", round(best, 2))
report("adjusted", (p >= np.where(g_test == 1, best, 0.5)).astype(int))
```

```text
threshold for B 0.35
adjusted         A 0.24/0.52  B 0.24/0.53
```

With B's threshold lowered to 0.35, the selection rate of suitable candidates
becomes equal in the two groups (52% and 53%). The price: group B's overall
selection rate rises from 15% to 24%, and the two groups are now judged with
different thresholds. Although it looks like a technical setting, this is a
**policy decision**: which fairness measure to choose (equal selection rate,
equal opportunity…) is an institutional and legal decision, not a technical
one; a different decision rule per group is debated or forbidden in some legal
systems. The real fix is often in the data: correcting the biased labels and
collecting the groups that are missing.

## Masking personal data

Support requests, documents and chat histories carry **personal data** like
email addresses and phone numbers. This data can be masked before it goes to
the model (or into the logs). Let us write a simple masker with regular
expressions and try it on example sentences:

```python
import re

PATTERNS = {
    "EMAIL": r"[\w.+-]+@[\w-]+\.[\w.]+",
    "PHONE": r"\+?\d[\d\s()-]{8,}\d",
    "ORDER": r"ORD-\d{5}",
}


def mask(text):
    for label, pattern in PATTERNS.items():
        text = re.sub(pattern, f"[{label}]", text)
    return text


SAMPLES = [
    "Please email me at ana.k@example.com about ORD-48213.",
    "Call me on +90 532 123 45 67 tomorrow.",
    "My number is (555) 123-4567.",
    "Write to ana dot k at example dot com.",
    "Order ORD-48213 arrived but the box was empty.",
]
for text in SAMPLES:
    print(mask(text))
```

```text
Please email me at [EMAIL] about [ORDER].
Call me on [PHONE] tomorrow.
My number is ([PHONE].
Write to ana dot k at example dot com.
Order [ORDER] arrived but the box was empty.
```

The email, the order number and the phone number in international form were
masked. But there are two gaps: in the number with brackets the first bracket
stayed outside ("([PHONE]."), and the email written out in words ("ana dot k
at example dot com") was not caught at all. Regular expressions catch common
forms cheaply and miss unusual spellings. The masker, like a checker, is
measured on example sentences (08) and the forms it misses are listed.

## Responsibility: a checklist

Technical measures alone are not enough; who checks a system, and how, is part
of the design too:

- **Measure and write it down:** measure success per group, document the
  results and the known limits.
- **Keep a human in the loop:** in decisions that affect people, like hiring,
  credit or health, the last word is a person's; the model makes a suggestion.
- **Be transparent:** tell users that they are talking to a model and that the
  model can make mistakes.
- **Little data:** do not collect personal data the task does not need; mask
  what is needed and limit how long it is kept.
- **Keep logs and take feedback:** wrong or harmful outputs should be
  reportable and reviewed.

## Summary

- A model learns the bias in past decisions; in the section the selection rate
  of suitable candidates in group B was about a third of A's.
- Removing the group column was not enough: a feature related to the group
  (the club) carried the bias.
- Corrections have a price: a per-group threshold equalised opportunity but
  changed the selection rates; this is an institutional and legal decision,
  not a technical one.
- Masking personal data with regular expressions is cheap but misses unusual
  spellings; it is used measured.
- Responsibility is part of the design: measure, document, keep a human in the
  loop.
