# Access Control Models

In the previous section we saw that permissions sit in a matrix. But **who
fills in** that matrix, and **based on what**? There are four big answers
to this question; each one is called an **access control model**:

| Model | Who decides? | Based on what? |
|---|---|---|
| **DAC** (discretionary) | The object's owner | The owner's wish |
| **MAC** (mandatory) | The system, a central rule | Classification labels |
| **RBAC** (role-based) | Administrators, by defining roles | The person's role |
| **ABAC** (attribute-based) | Written rules | Properties of subject, object, action and environment |

## DAC: the owner decides

**Discretionary access control** (DAC): every object has an **owner**, and
the owner decides who gets access. Sharing files on your computer with
someone, making a document "anyone with the link can view" is DAC.

```python
files = {"report.txt": {"owner": "ada", "readers": {"ada"}}}


def share(user, name, other):
    entry = files[name]
    if user != entry["owner"]:
        return "denied"
    entry["readers"].add(other)
    return "shared"


print(share("alan", "report.txt", "alan"))
print(share("ada", "report.txt", "alan"))
print(sorted(files["report.txt"]["readers"]))
```

```text
denied
shared
['ada', 'alan']
```

Alan could not give himself permission; Ada, the file's owner, gave it.
DAC is flexible and easy, but it has two weaknesses:

- **The owner can make mistakes:** sharing a secret document with the
  wrong person is one click. The organisation cannot prevent it; the
  decision belongs to the person.
- **Programs run with the owner's privileges:** a program Ada opens can
  read everything Ada can read. So can malware that gets onto Ada's
  computer. This is called the **Trojan horse problem**.

## MAC: the system sets the rule

**Mandatory access control** (MAC): the access decision is made not by a
person but by a system-wide rule, and users cannot change that rule. It
was born in military and government systems.

Every object is given a **classification**, every person a **clearance**;
both come from the same ordered list: `public` < `internal` < `secret` <
`top-secret`.

The best-known rule for protecting confidentiality is the **Bell-LaPadula**
model:

- **No read up:** a person may only read documents at their own level or
  lower.
- **No write down:** a person may only write at their own level or higher.

The second rule looks strange at first: why should someone at "secret"
level not write into a "public" document? Because if they could, they could
copy the secret information they have read into a public document, by
mistake or because of a Trojan horse inside it. The rule closes the
**path** of the leak.

```python
LEVELS = ["public", "internal", "secret", "top-secret"]


def blp(subject, obj, action):
    s, o = LEVELS.index(subject), LEVELS.index(obj)
    return s >= o if action == "read" else s <= o


for obj in LEVELS:
    can_read = blp("secret", obj, "read")
    can_write = blp("secret", obj, "write")
    print(f"{obj:<11}", "read:", can_read, "write:", can_write)
```

```text
public      read: True write: False
internal    read: True write: False
secret      read: True write: True
top-secret  read: False write: True
```

Someone at "secret" level can read downwards but not upwards; they can
write upwards but not downwards. At their own level both are allowed.

To protect integrity, the **Biba** model, which is the **opposite**, is
used: **no read down** (low-trust data must not pollute a high-trust
decision) and **no write up** (someone of low trust must not change
high-trust data). The software of a control room should not read a file
from the internet and act on it.

MAC is very strong but rigid: labelling every object and giving every
person a level is hard work, and workflows suffer. Today some operating
systems use a form of MAC next to DAC to protect their important parts.

## RBAC: by role

**Role-based access control** (RBAC): permissions are given not to people
but to **roles**; people are assigned roles. Like the roles "teacher",
"student" and "admin" in a school:

```python
role_perms = {
    "teacher": {"grades:read", "grades:write"},
    "student": {"grades:read_own"},
    "admin": {"users:manage"},
}
user_roles = {"ada": {"teacher"}, "alan": {"student"}, "grace": {"teacher", "admin"}}


def permissions(user):
    perms = set()
    for role in user_roles.get(user, set()):
        perms |= role_perms[role]
    return sorted(perms)


for user in ["ada", "alan", "grace"]:
    print(user, permissions(user))
```

```text
ada ['grades:read', 'grades:write']
alan ['grades:read_own']
grace ['grades:read', 'grades:write', 'users:manage']
```

RBAC's strength is easy management. When a new teacher arrives they get one
role; when a teacher becomes an administrator a role is added; when they
leave their roles are taken away and all their permissions go together.
Instead of handing out permissions person by person, a few roles are
managed.

Roles can **inherit** from each other (role hierarchy): the "head teacher"
role gets all the permissions of the "teacher" role and adds a few more.
The weak side is **role explosion**: if a new role is opened for every
exception ("a teacher who sees only class 9-B's grades"), there end up
being hundreds of roles and managing them gets hard.

## ABAC: by attributes

**Attribute-based access control** (ABAC): the decision is made from
**attributes**, according to a rule:

- Attributes of the **subject**: role, department, clearance.
- Attributes of the **object**: owner, department, classification.
- The **action**: read or write?
- The **environment**: time, location, the device used.

In a hospital the rule "a nurse may read the records of the patients in
her own department during working hours" cannot be written with a role
alone; it is written with ABAC:

```python
def abac(subject, resource, action, hour):
    same_dept = subject["dept"] == resource["dept"]
    if subject["role"] == "doctor":
        return same_dept
    if subject["role"] == "nurse":
        return same_dept and action == "read" and 7 <= hour < 19
    return False


nurse = {"role": "nurse", "dept": "cardiology"}
record = {"dept": "cardiology"}
for action, hour in [("read", 10), ("read", 23), ("write", 10)]:
    print(action, hour, abac(nurse, record, action, hour))
```

```text
read 10 True
read 23 False
write 10 False
```

ABAC is very flexible and prevents role explosion. The price is
complexity: as rules multiply, answering "who can access what?" gets hard
and the rules themselves need reviewing. Since a role is also an
attribute, ABAC can contain RBAC; most real systems do exactly that: basic
permissions by role, finer rules by attributes.

## Summary

- **DAC:** the owner decides; flexible, but the owner can make mistakes and
  programs carry all of the owner's privileges.
- **MAC:** the system decides by labels. **Bell-LaPadula** for
  confidentiality (no read up, no write down), **Biba** for integrity (the
  opposite).
- **RBAC:** permissions to roles, roles to people; easy to manage,
  exceptions lead to role explosion.
- **ABAC:** a rule over the attributes of subject, object, action and
  environment; the most flexible and the most complex.
- Real systems use the models together.
