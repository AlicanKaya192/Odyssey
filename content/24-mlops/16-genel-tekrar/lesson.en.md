# Overall Review

You have reached the end of the MLOps and ML System Design module. We
started with why a model that measures well in a notebook is only the
beginning; we made training reproducible, checked the data, and versioned
the data and the model. Then we built experiments, the registry and the
gate; we served the model and monitored it live. We measured the change
that comes with time (data and concept drift) and released new models
carefully. At the end we saw scaling, design and the whole pipeline. This
section walks the path once more.

<figure class="fig">
  <div class="flow">
    <span class="node">Foundations</span>
    <span class="arrow">→</span>
    <span class="node">Experiment to registry</span>
    <span class="arrow">→</span>
    <span class="node">Live</span>
    <span class="arrow">→</span>
    <span class="node">Over time</span>
    <span class="arrow">→</span>
    <span class="node acc">The system</span>
  </div>
  <figcaption>The module's path: repeat, record, serve, monitor, design.</figcaption>
</figure>

## 1. Foundations (Sections 0–3)

- **MLOps** applies the ideas of DevOps to ML systems; behavior comes from
  the code **and** the data. The lifecycle: data → train → evaluate →
  serve → monitor (0).
- **Reproducibility:** randomness comes from a seed; a separate seed for
  every random step, the settings in one configuration, the data's
  fingerprint and the library versions in the training record (1).
- **Data validation:** a data error doesn't stop the code, it breaks the
  model. Schema, quarantine or rejection, comparing profiles (2).
- **Versioning:** large files go not into Git but into a content-addressed
  store; a pointer file goes into Git; lineage ties the model to its data
  (3).

## 2. Experiment to registry (Sections 4–6)

- **Experiment tracking:** every experiment recorded automatically; a
  baseline; choose on validation, report once on test; the winner's curse
  (4).
- **Model registry:** version numbers that never change, a label pointing
  at the live one, the gate (`min_gain`), rolling back by moving the label,
  the model card (5).
- **CI for ML:** feature tests, the quality gate (a floor, a margin over
  the baseline, slices), behavior tests; measurements kept in every case
  (6).

## 3. Live (Sections 7–9)

- **Serving:** the model is loaded once; batch or online; the model
  version in the response; speed with p50 and p95 (7).
- **Training-serving skew:** no error appears, the predictions break.
  Feature code in one place; every feature as of the prediction time; a
  feature store (8).
- **Monitoring:** three layers (system, data and predictions, model
  quality); every prediction is logged; an alert after repeated breaches
  (9).

## 4. Over time (Sections 10–12)

- **Data drift:** PSI (0.1 / 0.25), KS; noise first; the p-value misleads
  with large samples; not every drift does harm (10).
- **Concept drift:** the relationship changes, invisible without labels;
  calibration breaks; the last window; the gate with a current set (11).
- **Shadow, canary, A/B:** shadow has no risk; a canary by a bucket from
  the id, a minimum number of customers per stage; the A/A noise before
  an A/B test (12).

## 5. The system (Sections 13–15)

- **Scaling:** as utilization approaches 100% the wait explodes;
  horizontal scaling needs a stateless server; the cache key is customer +
  model version; model size is weighed against latency (13).
- **Design:** the goal and the business measure first; the threshold by
  the measure; a fallback written in advance and tested (14).
- **Capstone:** monitor → trigger → validate → train → gate, every month;
  drift alone doesn't change the model, the gate alone isn't enough (15).

## All together: auditing a release

Using the module's rules, let's write a small auditor that reads the
record of a model release and lists its problems. The record below has
eight problems we saw in this module:

```python
release = {
    "version": 4,
    "seed": None,
    "data_digest": "",
    "trained_month": 5,
    "gate_month": 0,
    "gain": 0.001,
    "threshold": 0.5,
    "fallback": None,
    "monitors": ["accuracy"],
}


def audit(release, min_gain=0.003):
    problems = []
    if release["seed"] is None:
        problems.append("no fixed seed: training can't be repeated")
    if not release["data_digest"]:
        problems.append("no data digest: the data can't be traced")
    if release["gate_month"] < release["trained_month"]:
        problems.append("gate set is older than the training data")
    if release["gain"] < min_gain:
        problems.append(f"gain {release['gain']} is below {min_gain}")
    if release["threshold"] == 0.5:
        problems.append("threshold left at the default 0.5")
    if release["fallback"] is None:
        problems.append("no fallback")
    for needed in ["drift", "calibration"]:
        if needed not in release["monitors"]:
            problems.append(f"{needed} is not monitored")
    return problems


for problem in audit(release):
    print(problem)
```

```text
no fixed seed: training can't be repeated
no data digest: the data can't be traced
gate set is older than the training data
gain 0.001 is below 0.003
threshold left at the default 0.5
no fallback
drift is not monitored
calibration is not monitored
```

Every line rests on a section: the seed (1), the data digest (1 and 3),
an old gate set (11), the margin at the gate (5), the default threshold
(14), the fallback (14), and monitoring drift (10) and calibration (11).
In real teams this audit is a **release checklist** and runs inside the
pipeline: a version that doesn't pass the list doesn't enter the registry
with the "live" label.

## Next

In this module we built everything on a single computer, with small,
measurable pieces: the registry was a dictionary, the store a folder, the
pipeline a function. In real projects ready-made tools do the same jobs;
but knowing what they look at is the only way to set them up correctly
and understand their warnings. The rule is the same: **measure, record,
pass the gate, monitor.**
