`plan_test(p_a, p_b, daily_visitors)` should return `[n per group, days]`:
n with 80% power and α = 0.05 (rounded up), days by dividing both groups'
total by the daily visitors and rounding up, but **at least 7**. The
starter code counts one group and forgets the at-least-a-week rule.

**Expected output:**

```text
[6562, 9]
[1092, 7]
```
