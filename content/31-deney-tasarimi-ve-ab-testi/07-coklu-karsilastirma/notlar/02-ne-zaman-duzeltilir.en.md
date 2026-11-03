Not every p-value needs correcting. The question is: **which of these
tests makes the decision?**

## No correction needed

- **One primary metric written in advance.** If the decision depends on
  it, the family of tests is a single test.
- **Guardrail metrics**, if they are only checked for "did it break" and a
  break stops the test. Here the price of a false alarm is an unnecessary
  stop, not a wrong launch.

## Correction needed

- Tying the decision to **any one** of several metrics ("we launch if
  buying or revenue rises").
- Comparing several variants with the control and picking the best.
- Searching for metrics, segments or time windows after the test ends.
  Here even correcting is not enough: there is no way to know m. What is
  found becomes the **question** of a new test, not its result.

## In the report

- Write how many metrics were looked at.
- Give the primary metric in one table and the secondary ones in another.
- If a secondary metric is still significant after correcting, write
  "interesting, should be confirmed by a separate test"; the decision is
  not based on it.
