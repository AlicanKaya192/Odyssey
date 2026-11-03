# Overall Review

You have reached the end of the Experiment Design and A/B Testing module.
The Statistical Inference module taught you to **read** a test's result;
this module taught you to **set up** the test correctly, to recognise
real-life traps and to write the decision. This section walks the path once
more; at the end we gather every rule into a single function.

<figure class="fig">
  <div class="flow">
    <span class="node">Plan</span><span class="arrow">→</span>
    <span class="node">Assign</span><span class="arrow">→</span>
    <span class="node">Trust</span><span class="arrow">→</span>
    <span class="node">Read</span><span class="arrow">→</span>
    <span class="node acc">Decide</span>
  </div>
  <figcaption>The module's path: first write the question and the rules, assign at random, check whether the data can be trusted, read the result without falling into traps, and decide with rules written in advance.</figcaption>
</figure>

## 1. Plan

| Topic | Remember |
|---|---|
| The experiment question | one sentence; one primary metric, guardrail metrics, a practical threshold |
| The metric | sensitive, close to the change, related to the decision; revenue is noisy |
| Sample size | n is inversely proportional to the square of the effect; at least two full weeks |
| Random assignment | a salted hash: the same user always in the same group, experiments independent of each other |

## 2. Trust

- **The A/A test:** does the system alarm about 5% of the time when there
  is no difference?
- **SRM:** do the group sizes match the plan? If the chi-square p < 0.001,
  find the cause first; the result is not read.
- **Balance:** are the values before the test the same in both groups?

## 3. Reading

| Question | Tool |
|---|---|
| Two rates | z-test, `confint_proportions_2indep` |
| Two means, skewed data | Welch or the bootstrap |
| A statistic without a formula | the bootstrap (at the unit of assignment) |
| An assumption-free test | permutation |
| A ratio metric (clicks / views) | the delta method |
| A noisy metric | CUPED (with the value before the test) |

## 4. Traps

| Trap | Symptom | Remedy |
|---|---|---|
| Peeking | looking every day and stopping when significant | the last day or sequential thresholds written in advance |
| Multiple comparisons | a few "significant" among 20 metrics | one primary metric; Holm or BH |
| Simpson's paradox | the assignment ratio changed over time | a stratified estimate |
| Segment hunting | the most striking segment | a few segments written in advance |
| The novelty effect | the effect fades over time | a long test, a new-user cohort, a holdout |
| Interference | B takes from A | cluster assignment |
| Bandit data | a rarely chosen arm is biased | an A/B test if the size will be reported |

## 5. Deciding

The confidence interval falls in one of four places relative to zero and
to a threshold written in advance: **launch**, **harmful**,
**inconclusive**, **not worth it**. An inconclusive result is not "no
effect"; the report is one page, in the same order and with its limits.

## Every rule in one function

```python
from scipy import stats
from statsmodels.stats.proportion import confint_proportions_2indep
from ab_data import make_experiment


def analyse(test, threshold=0.003):
    n = test.groupby("group").size()
    if stats.chisquare(n).pvalue < 0.001:
        return "stop: SRM"
    k = test.groupby("group")["bought"].sum()
    low, high = confint_proportions_2indep(k["B"], n["B"], k["A"], n["A"])
    if high < 0:
        return "harm"
    if low >= threshold:
        return "ship"
    if high < threshold:
        return "not worth it"
    return "inconclusive"


for lift in [0.15, 0.0, -0.15]:
    print(lift, analyse(make_experiment(seed=161, lift=lift)))
```

```text
0.15 ship
0.0 inconclusive
-0.15 harm
```

With a true effect of 15% it says "launch", with zero "inconclusive", with
−15% "harmful". Let us test the function itself too: on 200 A/A tests where
nothing changes, how often does it wrongly say "launch"?

```python
verdicts = [analyse(make_experiment(seed=2000 + s, lift=0.0))
            for s in range(200)]
print({v: verdicts.count(v) for v in sorted(set(verdicts))})
```

```text
{'harm': 3, 'inconclusive': 180, 'not worth it': 16, 'ship': 1}
```

It says "launch" in 1 of the 200 A/A tests: since the bottom of
the interval must clear both zero and the threshold, a wrong launch is
rare. This is the measurable benefit of writing the rules in advance and
reading the interval against the threshold.

## Summary

- The plan comes before the test: question, metric, threshold, sample,
  looking rule, segments.
- Trust first (A/A, SRM, balance), then reading.
- Every trap has a recognisable symptom and a known remedy.
- The decision follows rules written in advance; the report is written with
  its limits.
