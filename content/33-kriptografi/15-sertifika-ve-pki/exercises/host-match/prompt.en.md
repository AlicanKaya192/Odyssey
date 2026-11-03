`host_matches(pattern, host)` should return whether the certificate name
`pattern` covers `host`. A wildcard (`*.example.test`) stands for
**exactly one** label: `shop.example.test` yes; `a.b.example.test` and
`example.test` no. Without a wildcard the names must be identical. The
starter code only looks at the ending for a wildcard.

**Expected output:**

```
True
False
True
False
```
