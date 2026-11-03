## Basic principles

| Principle | Meaning |
|---|---|
| Integrity | The evidence hash is recorded when collected and can be verified at every step |
| Work on a copy | The original evidence is not touched; it is read through a write blocker |
| Chain of custody | Every change of hands: who gave, who took, when, why |
| Order of volatility | Memory and connections first, then disk, then backups |
| Repeatability | Another expert must reach the same result with the same steps |
| Documentation | Every step is recorded with its tool and version |

## Order of volatility

| Order | Source |
|---|---|
| 1 | Memory (RAM) |
| 2 | Network connections, running processes |
| 3 | Temporary files |
| 4 | Disk |
| 5 | Backups, archives |

## Some file signatures

| Type | First bytes (hex) | As text |
|---|---|---|
| PDF | `25 50 44 46` | `%PDF` |
| PNG | `89 50 4E 47` | `.PNG` |
| ZIP (and docx, xlsx) | `50 4B 03 04` | `PK..` |

## Python patterns

- Evidence hash: `hashlib.sha256(data).hexdigest()`.
- Signature: `data.startswith(signature)`; from hex text to bytes `bytes.fromhex("89504e47")`.
- Extension: `name.rsplit(".", 1)[1]`.
- Checking the chain: at every handover `giver == previous_taker`.

## Keep in mind

- Evidence is valuable if it can be shown not to have changed.
- An extension changes easily; the first bytes tell the file's type.
- File times can be changed; alone they are not conclusive evidence.
- The report also states what was not found; a guess is not presented as
  evidence.
