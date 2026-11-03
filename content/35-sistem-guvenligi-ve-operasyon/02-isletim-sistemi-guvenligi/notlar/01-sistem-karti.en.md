## Basic concepts

| Concept | Meaning |
|---|---|
| Kernel mode | The mode that reaches everything; the operating system's kernel runs here |
| User mode | The restricted mode; applications run here |
| System call | An application asking the kernel for a privileged job |
| Process | A running program; it has its own memory space |
| Process isolation | One process cannot read another's memory |
| Sandbox | Running a program in an even more restricted space |
| Hardening | Making the default installation more secure |
| Security baseline | The configuration list every system must follow |

## Privileged accounts

| System | Administrator account | Requesting privilege temporarily |
|---|---|---|
| Linux | `root` | `sudo command` |
| Windows | Administrator | A User Account Control prompt |

Daily work is done with a standard account; administrator privilege is
dropped once the job is done.

## Python patterns

- Refuse if not in the policy: `operation in POLICY.get(role, set())`.
- Turn a version into a tuple of numbers: `tuple(int(p) for p in text.split("."))`.
- Tuples are compared number by number: `(2, 4, 10) > (2, 4, 9)`.
- Checking with a rule list: `if config.get(key) != wanted: ...`.

## Keep in mind

- `"2.4.10" < "2.4.9"` is **True** as text; versions are not compared as
  text.
- A missing key is a rule violation too: `config.get(key)` returns `None`
  and does not equal the wanted value.
- Every unused service and account is a door nobody watches.
