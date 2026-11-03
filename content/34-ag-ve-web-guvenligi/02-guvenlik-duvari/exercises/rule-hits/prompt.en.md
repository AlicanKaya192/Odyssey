`matches(rule, packet)` is ready. `rule_hits(rules, packets)` should
count each packet against the first rule it matches and return the
counters as a list: one number for each rule and, **at the end**, the
number of packets that matched no rule (fell to the default). A rule left
at zero is never used.

**Expected output:**

```
[2, 0, 1, 1]
```
