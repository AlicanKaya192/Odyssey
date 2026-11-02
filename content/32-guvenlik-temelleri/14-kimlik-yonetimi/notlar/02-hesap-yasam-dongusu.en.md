What to do at each event of an account. Organisations often tie this to
the record in human resources: when a hire, role change or exit record is
opened, the identity system acts on its own.

## Joiner

- Accounts are opened with the **role's** standard permissions; extra
  permissions for the person are given with a separate approval.
- The first password is single-use and changed at the first login;
  multi-factor authentication is set up on the first day.
- The account's **owner** (manager) is recorded.

## Mover

- The new role's permissions are added, the old role's permissions are
  removed **the same day**.
- If a transition period is needed, the old permission is left with an
  **end date**.
- Separation of duties is checked again: does the new role, together with
  the old one, form a conflicting pair of permissions?

## Leaver

- The directory record is closed; every system not connected to the
  directory is closed one by one (a list is kept).
- **Shared secrets** the person knew (shared account passwords, API keys)
  are changed.
- Open sessions and tokens are revoked.
- Devices and cards are returned.
- The person's files and the service accounts they owned are handed over
  to someone else.

## Regular work

- **Access review:** managers approve or remove their team's permissions.
- **Orphaned account scan:** the list of active employees is compared with
  every system's account list.
- **Unused account:** an account with no login for a long time is first
  locked, then closed.
- **Service accounts:** each one's owner, purpose and last password change
  are recorded.
