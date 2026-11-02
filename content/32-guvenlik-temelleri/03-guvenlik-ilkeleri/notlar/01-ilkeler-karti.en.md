| Principle | The question to ask in a review | An example of it being broken |
|---|---|---|
| **Least privilege** | Does this account or program really need this much privilege? | A web application connecting to its database with an administrator account |
| **Fail-safe defaults** (deny by default) | What happens when something not on the list arrives? | An upload page that only forbids `.exe` |
| **Secure by default** | If no setting is touched, is the system secure? | The `admin` / `admin` password that comes with the installation |
| **Fail securely** | When there is an error, does the door stay open or closed? | Allowing everyone when the permission file cannot be read |
| **Defence in depth** | If this control is bypassed, what is behind it? | Unencrypted backups protected by a single password |
| **Complete mediation** | Is the permission checked on every request? | The open session of someone whose access was removed carrying on |
| **Open design** | Would security break if the code were made public? | An admin page that relies on a secret address |
| **Economy of mechanism** | Can this check be read and understood in one sitting? | A permission rule with hundreds of exceptions |
| **Separation of privilege** | Is a single person or a single key enough? | The person who prepares a payment being able to approve it |
| **Psychological acceptability** | Will people try to get around this? | A complex password that must be changed every week |

## Two terms

- **Allowlist:** only what is on the list is allowed.
- **Blocklist:** only what is on the list is forbidden. Whatever is
  forgotten gets through; it is not used on its own.

## The condition of defence in depth

The chances of getting past each layer can only be multiplied if the
layers are **independent of each other**. Layers that rely on the same
password, the same server or the same person fall together.
