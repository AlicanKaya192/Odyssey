A confidence interval is short to write and easy to misread. Four common
mistakes and their correct versions:

## 1. "The true value is in this interval with 95% probability."

The true value is a fixed number; it is either in this interval or not. The
"95%" belongs to **the method**: 95% of intervals built with the same method
catch the truth.

**Correct:** "The 95% confidence interval for the true mean is 7.42–9.35."

## 2. "95% of users are in this interval."

No. The interval says where **the mean** may be, not individual users. Most
session lengths are far outside this interval: the interval for the mean is
nearly two minutes wide, while users themselves spread from half a minute
to over 90 minutes. An interval that says where single values will fall is called a
**prediction interval**, and it is much wider.

## 3. "The two groups' intervals overlap, so there is no difference."

Overlapping intervals do not show that the difference is **not
significant**. Two separate intervals each carry their own group's
uncertainty; the uncertainty of the difference is smaller than their simple
sum. If the question is the difference, compute the confidence interval of
**the difference** (in the t-test section).

## 4. "The interval is narrow, so the result is right."

A narrow interval only says that the effect of **chance** is small. If the
sample is biased (like the "frequent visitors only" survey of the first
section), the interval is narrow and wrong: it gathers tightly around a wrong
value.

## How to write it in a report

- Give the estimate, the interval and the confidence level together: "mean
  8.38 minutes (95% CI: 7.42–9.35, n = 100)".
- Say how the sample was chosen; an interval does not show bias.
- For a proportion, state which method (Wilson) you used.
