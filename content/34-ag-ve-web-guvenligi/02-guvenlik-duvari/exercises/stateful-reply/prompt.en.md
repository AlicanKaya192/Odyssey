Connections are `[src, sport, dst, dport]` lists.
`replies_ok(outgoing, incoming)` should return, as a `True`/`False` list,
whether each packet coming from outside is the **reverse**
(`[dst, dport, src, sport]`) of a connection started from inside. Hint: a
list cannot go into a set, a `tuple` can.

**Expected output:**

```
[True, False, False]
```
