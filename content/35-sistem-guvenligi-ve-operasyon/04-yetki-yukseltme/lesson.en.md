# Privilege Escalation

An attacker usually gets into a system with **little privilege**: an
ordinary user's account, the inside of a restricted service, or an ordinary
session in a web application. The real goal is more: other people's data or
administrator privilege. Moving from little privilege to much is called
**privilege escalation**.

This section covers privilege escalation **from the defender's side**: which
configuration mistakes open the door to it, how those mistakes are found
and how they are closed. The code is again a toy: checkers working on fake
tables and fake log lines.

## Two directions: horizontal and vertical

<figure class="fig"><div class="versus">
  <div><h4>Horizontal escalation</h4>Reaching the privilege or data of <b>another user</b> at the same level. Like one customer seeing another customer's invoice.</div>
  <div><h4>Vertical escalation</h4>Climbing to a <b>higher level</b>. Like an ordinary user being able to do administrator operations.</div>
</div><figcaption>The cause is the same in both: an authorization check is missing or wrong somewhere.</figcaption></figure>

## Horizontal escalation: the ownership check

If an application fetches an invoice by its number alone, any logged-in
user can see someone else's invoice by changing the number:

```python
INVOICES = {
    101: {"owner": "ada", "total": 120},
    102: {"owner": "bob", "total": 75},
}


def get_invoice_unsafe(user, invoice_id):
    return INVOICES[invoice_id]


def get_invoice(user, invoice_id):
    invoice = INVOICES.get(invoice_id)
    if invoice is None or invoice["owner"] != user:
        return "not found"
    return invoice


print(get_invoice_unsafe("ada", 102))
print(get_invoice("ada", 101))
print(get_invoice("ada", 102))
```

```text
{'owner': 'bob', 'total': 75}
{'owner': 'ada', 'total': 120}
not found
```

The first function gave `ada` `bob`'s invoice. The fixed version checks
**ownership** on every request. Saying "not found" rather than "forbidden"
for someone else's invoice is deliberate too: that way it does not leak
which numbers exist. Being authenticated does not mean being able to reach
every object; the rule from the Authorization section applies here too.

## Vertical escalation: trusting the client

If an endpoint that updates a profile writes every incoming field to the
user's record, the user can make themselves an administrator by adding a
`role` field to the request. This is called **mass assignment**:

```python
def update_unsafe(user, changes):
    user.update(changes)
    return user


ALLOWED = {"email", "display_name"}


def update_safe(user, changes):
    for key, value in changes.items():
        if key in ALLOWED:
            user[key] = value
    return user


request = {"display_name": "Ada", "role": "admin"}
print(update_unsafe({"name": "ada", "role": "user"}, request)["role"])
print(update_safe({"name": "ada", "role": "user"}, request)["role"])
```

```text
admin
user
```

The safe version writes only the fields on the **allow list**; `role` was
silently skipped. The rule: data from the client cannot decide for itself
which fields it may change. Fields such as role and privilege change only
through a separate, checked operation on the server.

## In the operating system: misconfiguration

In operating systems the most common cause of privilege escalation is not a
program bug but a **configuration mistake**. As we saw in the File
Permissions section, if the script of a scheduled task running on behalf of
the administrator can be changed by others, every line added to that script
runs with administrator privilege. A checker that finds this looks at the
script of every task running as administrator:

```python
TASKS = [
    {"name": "backup", "runs_as": "root", "owner": "root", "mode": 0o755},
    {"name": "cleanup", "runs_as": "root", "owner": "root", "mode": 0o777},
    {"name": "report", "runs_as": "root", "owner": "bob", "mode": 0o755},
    {"name": "stats", "runs_as": "bob", "owner": "bob", "mode": 0o777},
]
for task in TASKS:
    others_write = task["mode"] & 0o022
    if task["runs_as"] == "root" and (task["owner"] != "root" or others_write):
        print("risky:", task["name"])
```

```text
risky: cleanup
risky: report
```

`cleanup` was flagged because anyone can write it, and `report` because it
belongs to an ordinary user: in both cases someone who is not an
administrator can change what the administrator will run. `stats` is not
privilege escalation, since it already runs as `bob`; but its `777`
permission is still a separate mistake from the File Permissions section.

## A setuid inventory

The **setuid** bit we saw in the File Permissions section runs a program
with the privilege of the file's owner, not of the person running it. Every
setuid program owned by an administrator is, if it has a bug, a door to
escalation. The defense is simple: keep an allow list of the programs that
**need** to be setuid, and report every setuid file not on the list.

```python
import stat

FILES = [
    {"path": "/usr/bin/passwd", "mode": 0o4755},
    {"path": "/opt/tools/report-tool", "mode": 0o4755},
    {"path": "/usr/bin/ls", "mode": 0o755},
]
ALLOWED = {"/usr/bin/passwd"}
for f in FILES:
    if f["mode"] & stat.S_ISUID and f["path"] not in ALLOWED:
        print("unexpected setuid:", f["path"])
print(stat.filemode(stat.S_IFREG | 0o4755))
```

```text
unexpected setuid: /opt/tools/report-tool
-rwsr-xr-x
```

The setuid bit appears in the permission string as `s` in place of the
owner's `x`. The password-changing program stayed quiet because it is on the
list; the tool not on the list was reported. A new setuid file appearing
**unexpectedly** is a warning sign in itself too.

## Detection: traces in the logs

Prevention is not always enough; escalation **attempts** are monitored too.
Every operation that requests privilege (`sudo` on Linux, an administrator
prompt on Windows) leaves a log entry. The same user being refused several
times in a short time is a sign to pay attention to:

```python
from collections import Counter

LOG = [
    "09:58 sudo user=ada result=ok cmd=update",
    "10:01 sudo user=bob result=denied cmd=passwd",
    "10:02 sudo user=bob result=denied cmd=restart",
    "10:02 sudo user=bob result=denied cmd=useradd",
    "10:05 sudo user=eve result=denied cmd=update",
]
denied = Counter()
for line in LOG:
    fields = dict(part.split("=") for part in line.split()[2:])
    if fields["result"] == "denied":
        denied[fields["user"]] += 1
print(dict(denied))
print([user for user, count in denied.items() if count >= 3])
```

```text
{'bob': 3, 'eve': 1}
['bob']
```

`bob` was refused 3 times and crossed the threshold; `eve`'s
single refusal is most likely a mistake. The lower the threshold, the more
false alarms; the higher, the more missed attempts. This balance is the
topic of the Logging and Monitoring and Intrusion Detection sections.
Changes such as a new member being added to the administrators group are
monitored in the same way.

## Prevention list

| Cause | Prevention |
|---|---|
| No ownership check on objects | Check ownership on the server on every request |
| A field from the client is written directly | An allow list of fields that may change |
| An admin task runs a script others can write | The script belongs to the admin account, `755` or narrower |
| Unneeded setuid programs | An allow list; remove the bit from anything not on it |
| Unpatched kernel and services | Patch management |
| A system where everyone is an administrator | Least privilege; daily work with a standard account |

## Summary

- **Privilege escalation** is moving from little privilege to much; it is
  **horizontal** (another user) or **vertical** (a higher level).
- Against horizontal escalation, an **ownership check** on every request.
- Against vertical escalation, an **allow list** for fields from the
  client.
- In the operating system the cause is usually **configuration**:
  privileged scripts others can write, unneeded setuid programs.
- **Detection:** privilege requests refused several times in a row and
  changes to the administrators group are monitored.
