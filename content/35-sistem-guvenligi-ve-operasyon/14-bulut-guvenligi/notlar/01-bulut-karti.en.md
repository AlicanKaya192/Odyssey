## Who protects what?

| Layer | IaaS | PaaS | SaaS |
|---|---|---|---|
| Data | Customer | Customer | Customer |
| Identities and access | Customer | Customer | Customer |
| Application | Customer | Customer | Provider |
| Operating system | Customer | Provider | Provider |
| Network and virtualisation | Provider | Provider | Provider |
| Physical data centre | Provider | Provider | Provider |

## The most common configuration mistakes

| Mistake | Check | Fix |
|---|---|---|
| A public storage area | `public` and the data type | Block public access at account level |
| Unencrypted data | `encrypted` | Turn default encryption on |
| A broad wildcard permission (`*`) | Policy statements | Write the actions one by one |
| A management port open to the internet | `0.0.0.0/0` and the port | Narrow the source address, a VPN |
| No multi-factor authentication on the admin account | Account setting | Make it mandatory |
| Old access keys | Key age | Rotate or remove |

## IAM evaluation order

1. Every statement that matches the action is found.
2. If even one is `deny`, **forbidden**.
3. If there is at least one `allow`, **allowed**.
4. If there is none, **forbidden** (default deny).

## Python patterns

- Wildcard matching: `fnmatch.fnmatchcase(action, pattern)` (case-sensitive).
- Deny wins: `if "deny" in matches: return False`.
- The whole internet: `source in ("0.0.0.0/0", "::/0")`.

## Keep in mind

- The cloud does not remove responsibility, it shares it.
- Data and identities belong to the customer in every model.
- Misconfiguration is the most common cause of incidents; infrastructure as
  code catches it before setup.
