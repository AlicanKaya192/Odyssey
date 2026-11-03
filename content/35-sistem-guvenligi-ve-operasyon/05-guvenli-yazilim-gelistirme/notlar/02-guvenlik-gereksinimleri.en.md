The first step of a secure SDLC is the one most often skipped: writing
security down as a **requirement**. "The application must be secure" is not
a requirement; it cannot be tested. A good security requirement is a
sentence that can be verified by looking at whether a test passes.

## A bad and a good requirement

| Bad | Good |
|---|---|
| The application must be secure | Only the author of a post or an admin can delete the post |
| Passwords must be protected | Passwords are stored with a slow, salted hash; plain text is written nowhere |
| Sessions must be secure | A session ends after 30 minutes without activity |
| Inputs must be checked | The quantity field accepts only whole numbers from 1 to 100 |

What good requirements share: who, what, under which condition, and **what
must not happen** are written out clearly.

## From requirement to test

Every security requirement has at least one test. Requirements are written
into a list with an id, and tests state which requirement they test. That
way a **requirement with no test** is visible at a glance. This matching is
called **traceability**.

| Requirement | Test |
|---|---|
| SEC-1: only the author or an admin deletes | `stranger cannot delete`, `admin can delete` |
| SEC-2: a session ends after 30 minutes | `session expires after 30 minutes` |
| SEC-3: quantity 1–100 | `quantity rejects 0`, `quantity rejects 250` |

## Where requirements come from

- **The threat model:** a defense for every important threat, a
  requirement for every defense.
- **Law and contracts:** personal data (the Privacy and Data Protection
  section), sector rules.
- **Standards:** the organisation's security policy (the Security Policy
  and Standards section), common checklists.
- **Past incidents:** a bug that happened once becomes a requirement and a
  test, so it cannot happen again.

## Prioritisation

Not every security problem found is equally urgent. Teams sort findings by
severity (critical, high, medium, low) and fix them in that order. What
matters is that the order rests on a **written rule**: "a critical finding
stops the release, a low finding may wait for the next release", for
example.
