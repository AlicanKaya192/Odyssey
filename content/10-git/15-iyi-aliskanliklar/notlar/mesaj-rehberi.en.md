## Format

```text
Fix crash when the cart is empty            ← subject: ≤ 50 characters, imperative

The total was divided by the item count,     ← after a blank line: why
which is zero for an empty cart. Return 0
instead and show the "empty" message.

Fixes #42                                    ← an issue link, if any
```

In the terminal: `git commit -m "Subject" -m "Body" -m "Fixes #42"` (each
`-m` is a paragraph).

## Subject patterns

| Verb | When |
|---|---|
| `Add` | A new file, feature, test. |
| `Fix` | A bug fix. |
| `Remove` | Deleting. |
| `Update` | Updating something existing (a dependency version, text). |
| `Rename` / `Move` | A name or location change. |
| `Refactor` | Reorganising code without changing behaviour. |
| `Improve` | Speed, readability. |

## Ask yourself

- If I read this message in six months, will I understand what was done and
  **why**?
- Is there an "and" in the subject? Then it's probably two commits.
- Does the subject name the file? The diff already shows that; describe the
  work.

## Which language?

Git accepts any. English is common in open source and international teams;
being consistent in one language matters more than the language itself. Use
what your team uses.

## I noticed after committing

| Situation | Fix |
|---|---|
| A typo in the message, not pushed yet | `git commit --amend -m "..."` |
| Several small commits should have been one, not pushed | `git reset --soft HEAD~n` + commit, or `git rebase -i` |
| Already pushed | Leave it; be careful next time (don't rewrite history) |
