The choice of test depends on **how the data was collected**, not on how
the numbers look. Two columns side by side are not paired just because of
that, and data in two separate tables is not independent just because of
that either.

## Paired examples

- The load time of the same pages before and after a change.
- The task time of the same users with the old and the new version.
- The sales of the same shops last month and this month.
- The same student's pre-test and post-test scores.

What they share: each measurement has an **exact partner** in the other
group, and partners resemble each other.

## Independent examples

- Different users randomly assigned to groups A and B in an A/B test.
- Two samples taken from two different cities.
- Mobile and desktop users.

## The cost of the wrong choice

| Mistake | Result |
|---|---|
| An independent test on paired data | Differences between units count as noise; power collapses. In this section the rate of catching the real saving went from 78.2% to 0.0% |
| A paired test on independent data | Rows in random order get matched; the result is meaningless |

## Gaining pairing by design

A paired design can often be chosen on purpose: showing both versions to the
same user (in random order), measuring the same page twice. If units differ
a lot from each other, that means far fewer measurements for the same
power. The CUPED method of the second module is the same idea adapted to A/B
tests: it uses a user's behaviour before the experiment as "their own
partner".
