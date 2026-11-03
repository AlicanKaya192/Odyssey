Most protections are on by default today. But "default" does not always
mean "on": an old build script, a compatibility setting or a flag switched
off to build faster can silently remove a protection. That is why
protections are **checked**, not assumed.

## What is checked?

- **Build flags:** the canary (`-fstack-protector-strong` or `/GS`), a
  position-independent build (PIE; needed so ASLR can apply to the program
  itself too), DEP compatibility (`/NXCOMPAT`).
- **The running system:** whether ASLR and DEP are on in the operating
  system, and which programs are on the exception list.
- **Memory permissions:** whether any program opens an `rwx` region, and if
  so, whether it is really needed.

## The check becomes a list

In a build pipeline (CI) the same questions are asked for every new
release. Instead of doing this by hand, a **checklist** is turned into a
script: each program's properties are read, missing protections are
reported, and the release is stopped if something is missing. The
`missing_protections` exercise is a toy version of this idea.

| Finding | Severity | What is done? |
|---|---|---|
| No canary | High | Turn the build flag on, rebuild |
| No PIE (ASLR missing) | High | Build position-independent |
| An `rwx` region | Medium | Remove it if not needed, write the reason if it is |
| No CFI | Low–medium | Turn it on if supported |

## Why is "switching off" a warning sign?

A protection is almost never switched off for the program to work
correctly; it usually goes off because of an old habit or a compatibility
problem. If a review finds a protection switched off, the first question
is "why?", and the answer should be written down. An exception with no
reason is removed.

## Limits

- Protections are only against **memory** bugs; they have no effect on SQL
  injection, a wrong permission or a leaked password.
- None of them removes the bug; at best they stop the program safely.
  Stopping is a loss of availability too (the availability in the CIA
  triad); the bug itself is still fixed.
