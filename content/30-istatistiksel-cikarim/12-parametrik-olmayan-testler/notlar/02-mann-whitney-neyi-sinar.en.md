The Mann–Whitney test is often described as "the test that compares
medians". That is not quite right and can lead to wrong conclusions.

## Its real question

"Does a random B value **tend** to be larger than a random A value?" That
is, is $P(B > A)$ different from 0.5?

- If the two groups' distributions have **the same shape** and one is a
  shifted copy of the other, this question amounts to a difference in
  medians.
- If the shapes differ (one very spread, the other compact), the test can be
  significant even with equal medians, or not significant with different
  medians.

## It does not talk about the mean

If you ask a question about a **mean**, like total revenue, Mann–Whitney is
not the right tool. A few huge orders really change the mean and so the
revenue; a rank-based test deliberately "shrinks" them. For a revenue test
use the t-test or the bootstrap with a large sample.

## When is it exactly right?

- The question "is the typical user better off?" on a skewed metric.
- Small samples and outliers.
- Ordinal data: scales like a 1–5 satisfaction score, where the distance
  between values has no clear meaning.

## When reporting

Put the common language effect size ($U / n_A n_B$) and the two groups'
medians next to p. "B's median is higher, and a random B order is larger
than a random A order with probability 57%" is much easier to understand
than p.
