# Least Privilege and Separation of Duties

In the Security Principles section we briefly saw two principles: **least
privilege** and **separation of duties**. Both are simple sentences, but
applying them in a real organisation takes constant effort. Because
privileges **grow** by themselves over time: nobody remembers to take a
privilege back. This section explains how to measure that growth and how
to stop it.

## Where is least privilege applied?

- **Personal accounts:** everyone gets enough for their job. An accounting
  intern does not see the whole payroll.
- **Administrator accounts:** someone with administrator rights does their
  daily work (e-mail, the web) with a **separate, ordinary** account. The
  administrator account is only used when needed; if the account that
  opens a phishing e-mail is not an administrator, the damage stays small.
- **Programs and services:** a web application connects to its database
  with a user that can only read and write the tables it needs; not with
  an administrator user that can drop tables.
- **Data:** **need to know**. Even if the clearance is high enough,
  information is not given if the job does not need it.

## Privilege creep

An employee works first in support, then in sales, then in finance. At
every team change the new role's privileges are given but the old ones are
not taken away. This is called **privilege creep**:

```python
role_perms = {
    "support": {"tickets:read", "tickets:reply"},
    "sales": {"crm:read", "crm:write"},
    "finance": {"invoices:read", "payments:approve"},
}
history = ["support", "sales", "finance"]
held = set()
for role in history:
    held |= role_perms[role]
needed = role_perms[history[-1]]
print("held:", len(held), "needed:", len(needed))
print("extra:", sorted(held - needed))
```

```text
held: 6 needed: 2
extra: ['crm:read', 'crm:write', 'tickets:read', 'tickets:reply']
```

Four of the six privileges this person holds are unnecessary for their
current job. If the account is taken over, the attacker reaches customer
records, support tickets and payments. Creep is silent: nothing breaks,
nobody complains, only the risk grows.

## Reviews and unused privileges

The most effective control against creep is a regular **access review**:
the owner or manager of every privilege is asked "is this still needed?".
One kind of data makes the answer easier: logs. If a privilege has not been
used for months, it is most likely unnecessary.

```python
granted = {"crm:read", "crm:write", "invoices:read", "payments:approve"}
used_last_90_days = {"invoices:read", "payments:approve", "crm:read"}
print(sorted(granted - used_last_90_days))
```

```text
['crm:write']
```

The set difference (`-`) finds what was granted but not used. This list is
a suggestion, not an automatic removal list: a privilege used once a year
(year-end closing) may not show up in 90 days of logs.

## Time-limited privileges

Some privileges are only needed for a short time: looking at the live
database to fix a problem, accessing backups for a migration. Giving them
**with an end date** instead of permanently prevents creep from the start.
The extreme form of this idea is called **just-in-time access**: the
privilege is requested, approved, and drops by itself a few hours later.

```python
from datetime import date

grants = [("ada", "prod-db", "2026-10-01"), ("alan", "prod-db", "2026-11-30"),
          ("grace", "backups", "2026-11-02")]
today = date(2026, 11, 2)
for user, resource, until in grants:
    status = "active" if date.fromisoformat(until) >= today else "expired"
    print(user, resource, status)
```

```text
ada prod-db expired
alan prod-db active
grace backups active
```

An expired privilege has to be really **removed**; a privilege marked
"expired" that still works is useless. The end day is counted as included
(`>=`): today is the last day of Grace's privilege.

## Separation of duties

**Separation of duties** means giving the steps of a job that could be
abused to different people. If one person can both register a new supplier
and approve a payment to it, they can send money to a fake company they
set up themselves. If the two steps are with two different people, fraud
needs two people to agree.

Organisations write down pairs of **conflicting duties** in advance and
check that nobody holds both halves of a pair:

```python
conflicts = [("vendor:create", "payment:approve"), ("code:write", "deploy:alone")]
user_perms = {
    "ada": {"vendor:create", "payment:approve", "crm:read"},
    "alan": {"vendor:create"},
    "grace": {"code:write", "deploy:alone"},
}
for user, perms in user_perms.items():
    found = [pair for pair in conflicts if set(pair) <= perms]
    print(user, found)
```

```text
ada [('vendor:create', 'payment:approve')]
alan []
grace [('code:write', 'deploy:alone')]
```

`set(pair) <= perms` means "are both halves of the pair among the person's
privileges?" (for sets, `<=` asks "is it a subset?"). Ada and Grace each
carry a conflict.

Relatives of separation of duties:

- **Two-person rule:** the approval of two people for an important action.
  Large payments, sending code to the live system, access to an encryption
  key.
- **Mandatory vacation and job rotation:** someone else does a person's
  job for a while; a hidden scheme comes to light.

## The emergency account

When everything is locked down, one day there is an emergency and the
normal approval path cannot wait. For this a **break-glass account** is
kept: its password sits in a safe, an alarm goes off the moment it is used
and every action is reviewed afterwards. That is why the exception to
least privilege is also explicit, logged and watched.

## Summary

- Least privilege applies to people, administrators, programs and data;
  daily work is done with a non-administrator account.
- Privileges **creep** by themselves; regular **reviews** and removing
  unused privileges stop it.
- For short-term needs, privileges are given **with an end date**.
- **Separation of duties** gives the steps that could be abused to
  different people; conflicting pairs are written down and checked.
- Exceptions (the break-glass account) are explicit, logged and watched.
