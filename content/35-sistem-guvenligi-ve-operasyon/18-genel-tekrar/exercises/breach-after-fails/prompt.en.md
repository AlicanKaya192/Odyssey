Log lines have the form `"<time> <STATUS> user=<name> ip=<address>"`,
in time order. `breaches(lines, limit)` should return, sorted, the
addresses where a successful (`OK`) login came **after** at least `limit`
failed attempts. An address with many failures but no successful login is
an alert, not an incident. Logging and Monitoring, Intrusion Detection,
Incident Response.

**Expected output:**

```
['10.0.0.7']
[]
```
