The moment a fix for a vulnerability is released, the vulnerability
becomes something everyone knows about. A system that installs the fix is
protected; one that does not carries on with a vulnerability whose details
are now public. **Patch management** is the job of shortening the time in
between.

## The patch cycle

1. **Inventory:** which version of which software is installed on which
   computer? Unknown software cannot be updated.
2. **Monitoring:** follow the security announcements (advisories) for the
   software. Each advisory says in which version it was fixed.
3. **Comparison:** is the installed version older than the fixed version?
   (Versions are compared as tuples of numbers.)
4. **Prioritisation:** internet-facing systems and serious vulnerabilities
   first.
5. **Testing and installing:** try the patch on a small group first, then
   install it everywhere.
6. **Verification:** was it really installed, did the version change?

## What sets the priority?

| Question | If yes |
|---|---|
| Is the system reachable from the internet? | Move it up |
| Can the vulnerability be used remotely, without authentication? | Move it up |
| Is the vulnerability known to be in use? | Move it to the top |
| Does the system hold critical data? | Move it up |

These questions apply the likelihood and impact idea from the Assessing
Risk section to patching.

## If a patch cannot be installed right away

Sometimes a patch cannot be installed right away because of compatibility.
Then temporary measures that **reduce the impact** of the vulnerability are
taken: switching off the service involved, limiting access with a
firewall, increasing monitoring. These do not replace the patch, they only
buy time; a temporary measure has an end date.

## Common mistakes

- Thinking "everything is up to date" without an inventory.
- Comparing versions as text (`"2.4.10" < "2.4.9"`).
- Updating only the operating system and forgetting the applications and
  libraries.
- Not verifying after installing: a system that has not been restarted may
  keep running the old code.
