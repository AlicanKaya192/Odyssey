An organisation does not merely wait for reports; it writes in advance
how it will receive them. These written rules are published as a
**vulnerability disclosure policy**, and the `Policy` field in the
security.txt file links to it.

## What does the policy say?

| Part | Example content |
|---|---|
| Scope | Which sites and apps; which are out of scope |
| Allowed | Verifying with your own account, without touching others' data |
| Forbidden | Slowing or stopping the service, social engineering, physical access, downloading data |
| How to report | Address, encrypted contact channel, report format |
| The organisation's promises | Time to acknowledge, sharing the fix timeline, thanks |
| Safe harbour | No legal action against a researcher who follows the rules |
| Disclosure | When and how it will be announced together |

## The process on the organisation's side

1. **Receive:** collect reports through a single channel, acknowledge them
   quickly.
2. **Verify:** reproduce the vulnerability in your own test environment.
3. **Prioritise:** order by impact and severity.
4. **Fix:** write, test and release the fix; also look for similar places
   (the Code Review and Static Analysis section).
5. **Announce:** in agreement with the finder, together with the fix; get a
   CVE identifier if needed.
6. **Learn:** add it to the post-incident review (the Incident Response
   section).

## Measured behaviour for the finder

- If the organisation does not answer, first try another official
  channel; do not announce to everyone at once.
- Be flexible about the timeline; a complex fix can take time.
- Once the hole is closed, delete the notes and screenshots you still have.
- The aim of the announcement is to protect users, not to embarrass the
  organisation.
