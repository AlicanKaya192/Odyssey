New data: 800 patient records. `age`, `bmi`, `visits` (numeric, with
missing values), `sex`, `region`, `smoker` (text) and the target
`readmitted` — whether the patient was admitted again after discharge.

The data also holds a `followup_calls` column. **You will not use it in
this exercise**; you will see why in the third one.

**What you need to do:**

1. Read the data. Print the missing-value counts and the positive rate.
2. Take the six columns other than `followup_calls` and `readmitted` as
   `X`. Split (`test_size=0.25`, `random_state=42`, `stratify=y`).
3. Print the number of test records and positives side by side.
4. Set the baseline (0 for everything) and print its accuracy.
5. Train a `LogisticRegression(max_iter=1000)` in a pipeline. Print the
   accuracy, precision, recall and F1 on one line.
6. Print the confusion matrix.
7. Retrain the same model with `class_weight="balanced"` and print the same
   four numbers.

**Expected output:**

```
{'age': 0, 'sex': 0, 'region': 40, 'bmi': 56, 'visits': 32, 'smoker': 0, 'followup_calls': 0, 'readmitted': 0}
0.194
200 39
0.805
0.815 0.571 0.205 0.302
[[155   6]
 [ 31   8]]
0.65 0.293 0.564 0.386
```

**The baseline is 0.805 and the model 0.815.** A one-point gap. Section 09's
table is in front of you again: the positive class is 19.4% and accuracy
says almost nothing about this problem.

**The confusion matrix does say something:** of 39 real readmissions,
**8** were caught and **31** escaped. Recall is 0.205.

A hospital using this model would miss four fifths of its readmissions.

**The last line is what weighting achieves:**

| | Accuracy | Precision | Recall | F1 |
|---|---|---|---|---|
| Default | 0.815 | 0.571 | 0.205 | 0.302 |
| `balanced` | 0.650 | 0.293 | **0.564** | 0.386 |

Recall went from 0.205 to 0.564 — 22 patients caught instead of 8. The cost
is precision falling from 0.571 to 0.293 and accuracy from 0.815 to 0.650.

**Which is right?** That is not a model question but a clinical decision: is
a missed readmission more expensive, or a patient followed up for nothing?
The model cannot answer it. Whoever knows the answer reads the table and
chooses.

**Do not be troubled by accuracy falling.** 0.650 is below the baseline
(0.805), yet the model now genuinely works. This is accuracy's misleading
nature at its clearest.
