The segment table is the most read and the most misread part of a report.

## Before writing

- Which segments will be looked at is written into the plan (e.g. only
  platform).
- How many users each segment will have is computed; the calculation from
  the Sample Size section is repeated with the segment's own size. Most
  segments are not large enough to give a meaningful result on their own.

## In the table

- Write each segment's **confidence interval**, not only the point. A wide
  interval means "we do not know".
- Put the total result at the top; the segments below it.
- Write how many segments were looked at.

## In the interpretation

- To say "B does not work on mobile", mobile's interval must **clearly**
  separate from the total effect; containing zero is not enough.
- The largest and the smallest segment are most likely the extremes of
  chance; both are far from the true effect.
- A segment that really looks different is the question of a new test: in
  that segment, with one primary metric written in advance.

## Red flags

- Rescuing a test that is not significant in total with "but it is
  significant in this segment".
- Changing a segment's definition after looking at the result (e.g.
  shifting age bands).
- Building segments on a property determined **after** assignment (e.g.
  those who clicked a lot in the test): B may have changed that property.
