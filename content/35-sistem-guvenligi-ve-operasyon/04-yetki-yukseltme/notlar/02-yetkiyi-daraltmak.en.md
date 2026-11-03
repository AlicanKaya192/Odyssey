The most effective defense against privilege escalation is keeping the
privilege that could be escalated **small** from the start. If nobody has a
privilege they do not need, a bug or a taken-over account cannot reach that
privilege either.

## At the account level

- **Personal accounts:** a shared administrator account makes it impossible
  to track who did what.
- **A separate admin account:** a person with administrator privilege does
  their daily work (email, browser) with an account that is not an
  administrator.
- **Just-in-time privilege:** administrator privilege is not permanent; it
  is given for a job and for a limited time, and taken back automatically
  when the time is up.
- **Regular review:** who is in which groups is read from time to time; the
  privilege of someone who changes role or leaves is removed.

## At the application level

- Every endpoint looks at **who** is asking and **what** they touch; these
  are two separate checks.
- The authorization check is written in one place and every request passes
  through it; one of many scattered checks always gets forgotten.
- The default answer is "no": when a new endpoint is added without an
  authorization check, the request is refused.

## At the system level

- Services run with their own restricted accounts.
- Every script and program that runs with privilege is owned by a
  privileged account and nobody else can change it.
- An inventory of setuid programs and scheduled tasks is kept; a new entry
  that is not in the inventory is investigated.
- Patches are installed regularly: closing a known vulnerability is always
  cheaper than detecting its use.

## Monitoring changes

The result of privilege escalation is usually a **change**: a new member of
the administrators group, a new scheduled task, a new setuid file. That is
why snapshots of these lists are taken regularly and compared with the
previous one. Every unexpected difference should be explained by a change
record; a difference that cannot be explained is treated as an incident
(the Incident Response section).
