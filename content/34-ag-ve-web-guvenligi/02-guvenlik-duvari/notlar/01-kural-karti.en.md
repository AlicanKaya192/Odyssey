## The parts of a rule

| Field | Example | Meaning |
|---|---|---|
| Action | `allow` / `deny` | What to do |
| Direction | in / out | Which traffic is looked at |
| Protocol | `tcp`, `udp`, `any` | The transport protocol |
| Source | `192.168.1.0/24` | The address or network the packet comes from |
| Destination | `203.0.113.7/32` | The address or network the packet goes to |
| Port | `443` | The destination port |
| Logging | on / off | Whether matching packets are logged |

`0.0.0.0/0` means all addresses, `/32` a single address.

## How is the decision made?

1. The rules are tried from top to bottom.
2. The **first matching rule** decides; the rest are not looked at.
3. If none matches, the **default**: deny.

## Types

| Type | What it looks at | Note |
|---|---|---|
| Stateless filter | A single packet's headers | Replies need a wide hole |
| Stateful firewall | Headers + connection table | Today's default |
| Host firewall | That computer's traffic | Also looks at traffic from inside |
| WAF | The content of the HTTP request (OSI 7) | Extra layer; does not close the hole in the application |

## Rules

- **Deny by default**; everything to be opened is opened one by one,
  deliberately.
- Narrow rules at the top, broad rules at the bottom.
- Management ports (SSH, remote desktop) are opened only to the management
  network, not to the internet.
- **The way out is filtered too**; blocked attempts are logged.
- Every rule has an owner and a description; rules that never match are
  cleaned out.
