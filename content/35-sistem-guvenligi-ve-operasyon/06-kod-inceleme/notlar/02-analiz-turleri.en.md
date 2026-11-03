Static analysis is only one of the ways of testing code for security. Each
method sees something different and misses something different; that is
why they are used together.

## Methods

| Method | What does it do? | Strength | Weakness |
|---|---|---|---|
| Static analysis (SAST) | Reads code without running it | Early, looks at every line | False alarms, does not know intent |
| Dynamic analysis (DAST) | Sends requests to the running application from outside | Sees real behaviour | Only the part of the code that is reached |
| Dependency scanning (SCA) | Compares the packages used with known vulnerabilities | Finds others' vulnerabilities | Only known vulnerabilities |
| Secret scanning | Searches code and history for passwords, keys | Catches leaks early | Misses secrets of unknown format |
| Code review | A human reads | Sees logic bugs | Tires, is slow |

## False alarms and missed findings

Every check can be wrong in two ways: it reports a problem that is not
there (a **false positive**) or misses a problem that is (a **false
negative**). Tightening the rules raises the first, loosening them raises
the second. A good tool setting produces as many findings as the team can
really read.

## Accepting a finding

If a finding is examined and judged a false alarm, it is marked so the
tool does not report the same thing again on the next scan. This mark sits
in the code, with its reason and who made the decision. Bulk silencing
without a reason is the same as switching the tool off.

## In the build pipeline

1. Static analysis, secret scanning and dependency scanning run
   automatically on every change.
2. A new **critical** finding blocks the change from being merged.
3. Old findings are tracked in a list and reduced in order of severity;
   new bugs are not ignored because of old debt.
4. Human review is done after the tools pass: the reviewer does not waste
   time on things a tool could find.
