`decide(srm_p, guard_high, low, high, threshold=0.003, guard_limit=2.0)`
should apply the project's decision rule. The starter code looks at
"launch" first: a test with SRM or a broken guardrail also says "ship".
The trust and guardrail checks come before everything.

**Expected output:**

```text
ship
stop: SRM
```
