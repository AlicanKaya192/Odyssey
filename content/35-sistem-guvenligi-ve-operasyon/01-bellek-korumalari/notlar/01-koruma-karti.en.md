## Four protections

| Protection | Idea | When is it checked? |
|---|---|---|
| Stack canary | A random value between the buffer and the return information | Before the function returns |
| DEP / NX | A data region cannot run (W^X) | The processor, on every instruction |
| ASLR | Addresses are random on every run | When the program is loaded |
| CFI | Jumps only to allowed targets | On every indirect jump |

## Permission strings

| Region | Usual permission | Why? |
|---|---|---|
| Code | `r-x` | Runs but cannot be changed |
| Data, heap | `rw-` | Changes but does not run |
| Stack | `rw-` | Changes but does not run |
| `rwx` | — | A W^X violation; only if unavoidable |

## Entropy and guessing

| Random bits | Chance | Average tries |
|---|---|---|
| 8 | 1 in 256 | 128 |
| 16 | 1 in 65,536 | 32,768 |
| 28 | 1 in 268,435,456 | 134,217,728 |

Every extra bit doubles the guessing work. The average number of tries is
half the number of possible addresses: `2 ** (bits - 1)`.

## Python patterns

- A W^X violation in a region: `"w" in perms and "x" in perms`.
- The canary check: `frame[size] == canary`.
- The chance as text: `f"1 in {2 ** bits:,}"` → `1 in 65,536`.

## Keep in mind

- The canary must be **secret** and **random**; a fixed value does not
  protect.
- The canary only looks on return; it does not see another variable
  damaged in the same function.
- Protections are the second line of defense; the real fix is fixing the
  bug or a memory-safe language.
