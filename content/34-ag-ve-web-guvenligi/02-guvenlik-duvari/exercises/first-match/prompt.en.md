`rules` is a list of dictionaries `{"action", "proto", "port"}`;
`proto` or `port` can be `"any"`. `decide(rules, packet)` should try the
rules in order and return the `action` of the first matching rule. If none
matches, it should return `"deny"` (deny by default).

**Expected output:**

```
tcp 443 allow
tcp 22 deny
udp 53 allow
udp 123 deny
```
