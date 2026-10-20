Retraining is a pipeline, not a single `fit` call.

<figure class="fig">
  <div class="flow">
    <span class="node">Trigger</span>
    <span class="arrow">→</span>
    <span class="node">Data window</span>
    <span class="arrow">→</span>
    <span class="node">Train</span>
    <span class="arrow">→</span>
    <span class="node acc">Current gate</span>
    <span class="arrow">→</span>
    <span class="node">Registry</span>
  </div>
  <figcaption>The gate works with a current, labelled set.</figcaption>
</figure>

## The lesson's choices (months 6 and 7)

| Choice | Month 6 | Month 7 |
|---|---|---|
| Never retrain | 0.685 | 0.658 |
| All history (0–5) | 0.759 | 0.742 |
| Last window (4–5) | 0.821 | 0.798 |

## The gate trap

| Model | Month 0 set | Month 5 set |
|---|---|---|
| First model | 0.813 | 0.681 |
| Last window | 0.718 | 0.837 |

A gate built on the old set would have turned the new model away.

## Checklist

- Is the trigger clear (a schedule, a quality alert or both)?
- Was the window size chosen by measuring on a later period?
- Was the training data pulled as of a date and validated?
- Is the gate's evaluation set current and labelled?
- Did the new model enter the registry with its version, data and
  measurements?

## Don't

- Don't say "the more data the better" when the concept has drifted.
- Don't run the gate with a set left over from training time.
- Don't retrain automatically at every drift alert; first make sure the
  data isn't faulty.
