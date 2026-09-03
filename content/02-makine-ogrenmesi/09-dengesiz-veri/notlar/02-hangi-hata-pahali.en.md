On imbalanced data every setting hangs on one question: **which of the two
error types costs more?** Every threshold and weight chosen without
answering it is arbitrary.

## The two errors

| | Name | What happened |
|---|---|---|
| **FN** | A miss (false negative) | You said "negative" to a real positive |
| **FP** | A false alarm (false positive) | You said "positive" to a real negative |

In the confusion matrix they are the two cells off the diagonal. Their sum
is the whole error — but they are **not the same thing.**

## When recall is expensive

If a miss costs more than a false alarm, **recall** comes first.

| Problem | If you miss | If you raise a false alarm |
|---|---|---|
| Cancer screening | The patient goes untreated | One more test is run |
| Fraud | Money is gone | The customer gets a call to confirm |
| Aircraft maintenance | The fault appears in flight | An extra inspection |
| Earthquake warning | You are caught unprepared | A drill for nothing |

What they share: the consequence of a miss is **irreversible**, while a
false alarm is **annoying but fixable**.

Here `class_weight="balanced"` and a low threshold make sense.

## When precision is expensive

If a false alarm costs more, **precision** comes first.

| Problem | If you raise a false alarm | If you miss |
|---|---|---|
| Spam filter | An important email is binned | One spam in the inbox |
| Content removal | An innocent user is silenced | One bad post stays up |
| Loan refusal | A paying customer is lost | One bad loan |
| Hiring screen | A good candidate is cut without ever knowing | One bad interview |

What they share: a false alarm **harms a person**, and that person usually
cannot appeal.

Here a high threshold and no `class_weight` make sense.

## Putting numbers on it

If the costs are known, the threshold can be chosen by **expected cost**
rather than F1:

```
cost = FN_count * FN_price + FP_count * FP_price
```

An example: a miss costs 400, a false alarm 5 (the cost of a phone call).

| Threshold | FN | FP | Cost |
|---|---|---|---|
| 0.50 | 15 | 2 | 15*400 + 2*5 = **6010** |
| 0.20 | 14 | 7 | 14*400 + 7*5 = **5635** |
| 0.10 | 8 | 25 | 8*400 + 25*5 = **3325** |
| 0.05 | 5 | 45 | 5*400 + 45*5 = **2225** |

With these costs **0.05 wins** — not the 0.10 that F1 chose. Because F1
treats precision and recall as equally important; the business does not.

Had a false alarm cost 100 rather than 5 (say every alarm loses a
customer), the table would point somewhere else:

| Threshold | Cost (FP = 100) |
|---|---|
| 0.50 | 6200 |
| 0.20 | 6300 |
| 0.10 | **5700** |
| 0.05 | 6500 |

**The same model, the same probabilities, a different decision.** One number
changed: the price of a false alarm.

## When the cost is unknown

Most of the time nobody can answer "what does one miss cost". Then:

1. **Present the table, do not decide.** Take the threshold sweep's output
   to the business side. "At 0.10 we catch 13 frauds and call 25 customers
   for nothing" is far more discussable than "our F1 score is 0.441".
2. **Set a constraint.** If there is a limit like "we can handle at most 30
   false alarms a day", the threshold follows from it.
3. **Use F1 as a temporary anchor.** With no information at all, F1 is a
   reasonable start — but it should be written down that this is an
   assumption.

## Look at the decision, not the model

In this section's measurements the model **never changed**. The same
logistic regression, the same coefficients, the same probabilities. All that
changed was:

- The weights (`class_weight`)
- Where the decision is made (the threshold)
- The number being read (the metric)

Recall went from 0.286 to 0.762 and precision from 0.75 to 0.262. None of it
was a new model.

**The conclusion:** on imbalanced data the gain usually comes not from a
better model but from a better decision.
