`hosts` is machine name → list of addresses and domains seen in its logs.
`hosts_to_isolate(hosts, indicators)` should return, in alphabetical order,
the names of the machines that touched at least one of the indicators of
compromise.

**Expected output:**

```
['pc-bob', 'srv-db']
[]
```
