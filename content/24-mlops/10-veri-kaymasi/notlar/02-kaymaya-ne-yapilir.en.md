The drift has been measured. Now what?

<figure class="fig">
  <div class="flow">
    <span class="node">Drift alert</span>
    <span class="arrow">→</span>
    <span class="node">Is it noise?</span>
    <span class="arrow">→</span>
    <span class="node">An important column?</span>
    <span class="arrow">→</span>
    <span class="node acc">Did quality drop?</span>
  </div>
  <figcaption>The decision to retrain is made by the last question.</figcaption>
</figure>

## The questions in order

1. **Is it noise?** What is the PSI of another sample from the same
   period? Is the measured drift clearly above it?
2. **Is it a data error?** Did the drift start suddenly and in a single
   column? It may be a change of unit or a broken source (Data
   Validation).
3. **Is it an important column?** How much does the model rely on this
   column?
4. **Did quality drop?** Accuracy is measured when the labels arrive. If
   it didn't drop, the drift is harmless; keep monitoring.
5. If it dropped: retrain with new data, pass it through the gate, put it
   in the registry (Concept Drift and Retraining).

## Checklist

- Is the reference data known and in the registry (which training data)?
- Was the noise level measured for every column?
- Was the threshold put on a measure of size (PSI, KS statistic)?
- Are the shares of the categorical columns watched too?

## Don't

- Don't tie the alert to the p-value.
- Don't retrain automatically at every drift; you may teach the model a
  data error.
- Don't take the PSI thresholds as law; tune them to your own data's
  noise.
