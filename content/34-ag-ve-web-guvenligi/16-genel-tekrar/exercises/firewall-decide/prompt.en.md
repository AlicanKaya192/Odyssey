Combine the Network Layers and Firewalls sections. Each rule has
`action`, `src` (CIDR) and `port` (a number or `"*"`).

`decide(rules, packet)` should try the rules **from top to bottom**; if the
packet's source (`ipaddress`) is in the rule's network and the port
matches, return the decision of the **first** matching rule. If none
matches, `"deny"`.

**Expected output:**

```
10.0.5.7 22 deny
10.1.2.3 22 allow
192.168.1.5 443 allow
192.168.1.5 22 deny
```
