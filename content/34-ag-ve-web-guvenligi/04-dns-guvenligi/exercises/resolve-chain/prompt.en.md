`records` is a dictionary mapping each name to a `[kind, value]` list;
`kind` is `"A"` or `"CNAME"`. `resolve(records, name)` should follow the
CNAMEs and return the address of the A record. If the name does not exist,
`"NXDOMAIN"`. CNAMEs can point at each other and form a loop: if **8**
CNAMEs have been followed without reaching an A, return `"LOOP"`. The
starter code looks only one step.

**Expected output:**

```
www.example.com 203.0.113.10
mail.example.com NXDOMAIN
a.example LOOP
```
