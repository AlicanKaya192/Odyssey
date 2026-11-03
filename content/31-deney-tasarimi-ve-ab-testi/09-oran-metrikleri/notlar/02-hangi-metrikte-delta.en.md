The only question to ask: **is the metric's denominator the unit of
assignment?**

## If the denominator is the unit of assignment: an ordinary test

- In a test assigned by user, the buying rate **per user** (users who
  bought / users). Every user is one trial; a proportion test or Welch is
  enough.
- Revenue per user, minutes per user. A user-level number; Welch or the
  bootstrap.

## If the denominator is something else: the delta method

- Clicks per view (CTR).
- Revenue per order (average basket): the number of orders varies from
  user to user.
- Time per session, pages per session.
- Clicks per search.

In all of these the same user has several views, orders or sessions, and
they resemble each other.

## The same idea elsewhere

- **Cluster assignment:** in a test assigned by store or city the unit is
  the store; the customers inside it are not counted as independent.
- **The denominator itself can change:** if B makes users see more pages,
  the ratio's denominator changes too. The ratio may look lower while total
  clicks have risen; report the numerator and the denominator separately as
  well.

## A quick check

Run the test of a ratio metric a few hundred times on A/A data: if false
alarms clearly exceed 5%, you are counting the wrong unit.
