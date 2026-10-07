Semantic Versioning (semver.org) is made of three numbers:
**MAJOR.MINOR.PATCH**. The kind of change decides which one goes up.

| Change | Example | New version (from `1.4.2`) |
|---|---|---|
| A bug fix; nobody using it has to change anything | A wrongly computed total is fixed | `1.4.3` (PATCH) |
| A new feature; the old ones work the same | A new export option | `1.5.0` (MINOR; PATCH resets) |
| An incompatible change; users must change their code | A function's name or parameters changed | `2.0.0` (MAJOR; the others reset) |

## Rules

- When a number goes up, the ones to its right reset: `1.9.7` → `2.0.0`.
- `0.x.y` means "not stable yet"; anything can change at any time. That is
  why Odyssey's `0.9.x` versions start with 0.
- A released version's content is never changed; a fix is a new version.
- Pre-releases get a suffix: `2.0.0-beta.1`, `2.0.0-rc.1` (*release
  candidate*).

## Tag names

Git sets no rule for tag names, but the convention is `v` + the version:
`v1.4.2`. Agree on one form as a team; a mix of `1.4.2`, `v1.4.2` and
`release-1.4.2` confuses sorting and tools.

## Release notes

Each release gets **release notes** (a *changelog*): what was added, what
changed, what was fixed. `git log --oneline v1.4.2..v1.5.0` gives a good list
to start from; but notes aren't a commit list, they answer the user's
question "what changed for me?".
