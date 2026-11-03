## The parts

| Part | Its job |
|---|---|
| Resolver | The server your computer asks; follows the chain, caches |
| Root and TLD servers | Say "this domain's authoritative server is over there" |
| Authoritative server | The real owner of the domain's records |
| TTL | How long the answer stays in the cache (seconds) |
| `NXDOMAIN` | The "no such name" answer |

## Record types

| Type | Meaning |
|---|---|
| A / AAAA | IPv4 / IPv6 address |
| CNAME | Alias; continue with the target name |
| MX | Mail server |
| NS | Authoritative servers |
| TXT | Free text (verification rules etc.) |
| DS | Hash of the child domain's key (DNSSEC) |

## Attacks and defences

| Risk | Defence |
|---|---|
| Cache poisoning | Random query ID and source port; DNSSEC |
| Queries being listened to | Encrypted DNS (DoT, DoH) |
| Hijacked DNS settings | Router password and updates |
| Takeover of the domain account | MFA, account lock |
| Dangling CNAME (subdomain takeover) | Deleting the record of a closed service too |
| Lookalike names | Monitoring, using bookmarks |

## Rules

- DNSSEC provides **integrity**, not **confidentiality**; encrypted DNS the
  opposite.
- A wrong answer in the cache is given to everyone **until the TTL ends**.
- DNS records are assets too: they have an owner and a review schedule.
