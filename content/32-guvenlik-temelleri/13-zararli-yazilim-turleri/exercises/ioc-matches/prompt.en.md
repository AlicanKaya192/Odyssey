In incident response, log lines are searched for indicators of
compromise (IOCs). `lines` are the log lines, `iocs` the indicators
searched for (domains, pieces of hashes).

`ioc_matches(lines, iocs)` should return the indicators that appear in at
least one line, without repeats and in alphabetical order.

**Expected output:**

```
9f86d081884c
cdn.toy-bad.test
```
