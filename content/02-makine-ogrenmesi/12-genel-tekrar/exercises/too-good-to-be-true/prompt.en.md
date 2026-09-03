A colleague hands you a model and says it scores **100% accuracy**. Before
celebrating, what should you do?

In this exercise you will model the same data twice: once with every
column, once without `followup_calls`.

**What you need to do:**

1. Read the data and split it (`stratify=y`).
2. **The first model:** numeric columns `age`, `bmi`, `visits`,
   `followup_calls`. Train a `LogisticRegression(max_iter=1000)` in a
   pipeline. Print the accuracy, precision and recall on one line.
3. Print the confusion matrix.
4. Print how many mistakes the model made in total (the sum of the
   off-diagonal cells).
5. Print `followup_calls`' **mean by target** (two decimals) — the source of
   the leak shows here.
6. **The second model:** print the same three numbers with `followup_calls`
   removed.
7. On the last line print the difference between the two accuracies.

**Expected output:**

```
1.0 1.0 1.0
[[161   0]
 [  0  39]]
0
{0: 0.48, 1: 3.43}
0.815 0.571 0.205
0.185
```

**The first line: accuracy, precision and recall are all 1.0.** The
confusion matrix holds not one error. The model got all 200 patients right.

**That is not a success but an alarm.** On real data a perfect score almost
always means one thing: **leakage.**

**The fifth line shows the reason:** among patients not readmitted the mean
`followup_calls` is 0.48, among those readmitted **3.43**. The column
copies the target almost exactly.

Why? Because **follow-up calls are made after the patient is discharged.**
That column is the **outcome** of the event we are trying to predict — not
its cause.

**At prediction time you will not have this information.** As the patient is
being discharged, you do not know how many follow-up calls will be made.
The model runs on information you will never actually hold.

**No tool can catch this.** `train_test_split` does not — the column is on
both sides. A pipeline does not — the leak is not in the preprocessing but
in the column itself. Cross validation does not — the same thing happens in
every fold.

**The only thing that catches it is this question:** *will this information
really be in my hands at the moment I make the prediction?*

Putting every column through that question is the one step of this module
that cannot be automated.

**The last line: 0.185.** Removing the column drops accuracy from 1.000 to
0.815 — and 0.815 is barely above the baseline (0.805). So what you really
have is a very weak model; the leak was making it look perfect.

**Had this model gone to production**, the `followup_calls` column would
arrive empty from day one and the model would be useless.
