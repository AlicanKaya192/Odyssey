The model says "negative unless you are sure" because it is trying to
reduce total error. There is a way to tell it that **missing a positive
costs more**.

```python
LogisticRegression(max_iter=1000, class_weight="balanced")
```

`"balanced"` gives each class a weight in inverse proportion to its
frequency.

**What you need to do:**

1. Prepare, split (`stratify=y`) and scale the data.
2. Take four models in turn:
   - `logreg` — `LogisticRegression(max_iter=1000)`, on the scaled data
   - `logreg-bal` — the same with `class_weight="balanced"`
   - `forest` — `RandomForestClassifier(n_estimators=200, random_state=42)`,
     on the **unscaled** data
   - `forest-bal` — the same with `class_weight="balanced"`
3. Print one line each: **the name, accuracy, precision, recall, F1** (three
   decimals).
4. On the last line print the weighted logistic regression's recall minus
   the default one's.

**Expected output:**

```
logreg 0.955 0.75 0.286 0.414
logreg-bal 0.88 0.269 0.667 0.384
forest 0.955 0.75 0.286 0.414
forest-bal 0.952 0.615 0.381 0.471
0.381
```

**Weighting raised recall from 0.286 to 0.667.** Fourteen frauds are caught
instead of six. The last line writes that difference: **0.381**.

**But the cost sits on the same line:** precision fell from 0.75 to 0.269.
The model now calls 52 transactions fraud and 38 of them are false alarms.
Accuracy dropped from 0.955 to 0.880 too.

**This is a trade, not an improvement.** Which side is right depends on the
problem itself: is a missed fraud more expensive, or a customer called for
nothing? The model cannot answer that question.

**The effect is more measured in the forest:** recall from 0.286 to 0.381,
precision from 0.75 to 0.615. F1 rises (0.414 → 0.471) — the most balanced
result on this data.

The reason is how a tree decides: logistic regression shifts the whole
boundary, while a tree only changes the vote inside its leaves.
