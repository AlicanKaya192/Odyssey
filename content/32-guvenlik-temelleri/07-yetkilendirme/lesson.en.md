# Authorization

Authentication answered the question "who are you?". **Authorization**
answers the second question: "are you allowed to do this?" Knowing who Ada
is does not say whether she may see the payroll. This section explains
what a permission decision is made of, how permissions are kept, and where
authorization breaks most often.

## The parts of a decision

Every authorization decision has three parts:

- **Subject:** whoever wants to do the job. A user, a program, a service.
- **Object** or **resource:** the thing the job is to be done on. A file,
  a table, an invoice.
- **Action:** the job to be done. Read, write, delete, approve.

The decision is the answer to this sentence: "May the **subject** do the
**action** on the **object**?" For example "May Alan read the `payroll`
file?"

## The access control matrix

We can write every decision into one table: the rows are subjects, the
columns are objects, the cells are the allowed actions. This is called an
**access control matrix**:

```python
matrix = {
    "ada": {"grades": {"read", "write"}, "payroll": set()},
    "alan": {"grades": {"read"}, "payroll": {"read"}},
    "grace": {"grades": set(), "payroll": {"read", "write"}},
}
objects = ["grades", "payroll"]
print(f"{'':<6}", *[f"{o:<11}" for o in objects])
for subject, row in matrix.items():
    cells = [",".join(sorted(row[o])) or "-" for o in objects]
    print(f"{subject:<6}", *[f"{c:<11}" for c in cells])
```

```text
       grades      payroll    
ada    read,write  -          
alan   read        read       
grace  -           read,write
```

The matrix is a perfect idea for understanding, but a real system has
thousands of users and millions of files; almost all the cells are empty.
That is why the matrix is stored in two different ways.

## Access lists and capability lists

An **access control list** (ACL) stores the matrix **column by column**:
next to every object it says who may do what to it. File system permissions
work this way.

```python
acl = {}
for subject, row in matrix.items():
    for obj, actions in row.items():
        if actions:
            acl.setdefault(obj, {})[subject] = sorted(actions)
print(acl["grades"])
print(acl["payroll"])
```

```text
{'ada': ['read', 'write'], 'alan': ['read']}
{'alan': ['read'], 'grace': ['read', 'write']}
```

A **capability list** stores the matrix **row by row**: next to every
subject it says what they may do to what. The information a login token
carries, "this person may do these things", is like this.

```python
caps = {s: {o: sorted(a) for o, a in row.items() if a} for s, row in matrix.items()}
print(caps["alan"])
print(caps["grace"])
```

```text
{'grades': ['read'], 'payroll': ['read']}
{'payroll': ['read', 'write']}
```

Both hold the same information but make different questions easy:

| Question | ACL | Capability list |
|---|---|---|
| "Who can access this file?" | Easy: look at the file's list | Hard: scan everyone's list |
| "What can Alan access?" | Hard: scan every file | Easy: look at Alan's list |
| Removing all permissions on one object | Easy | Hard |
| Removing all permissions of one person | Hard | Easy |

Removing every privilege of someone who leaves the company means looking
at every object one by one in a system that uses ACLs. That is why real
systems often use an extra layer such as roles (next section).

## Where is the decision made?

The most important rule of authorization: **the decision is made on the
server.** Hiding a button on the screen is not authorization. Even if the
user does not see the button, they can send the request by hand. The
interface only offers the user convenience; the real check is done in the
code that receives the request, on every request (complete mediation).

The second rule: the check is done **at the object level**. "Has permission
to view invoices" is not enough; the question must be "may they view
**this** invoice?". The vulnerability that appears when this question is
forgotten is called an **insecure direct object reference** (IDOR): a user
who changes `/invoices/101` in the address bar to `102` sees someone else's
invoice.

```python
invoices = {101: "ada", 102: "alan", 103: "ada"}


def can_view_bad(user, invoice_id):
    return invoice_id in invoices


def can_view(user, role, invoice_id):
    owner = invoices.get(invoice_id)
    if owner is None:
        return False
    return owner == user or role == "accountant"


tests = [("ada", "customer", 101), ("ada", "customer", 102),
         ("bob", "accountant", 102), ("ada", "customer", 999)]
for user, role, invoice_id in tests:
    print(user, invoice_id, can_view_bad(user, invoice_id),
          can_view(user, role, invoice_id))
```

```text
ada 101 True True
ada 102 True False
bob 102 True True
ada 999 False False
```

The bad version only checks whether the invoice **exists**: Ada can see
Alan's invoice 102. The good version asks for the owner; the `accountant`
role can see everyone's invoices. For an invoice that does not exist both
versions say `False`, but the good version does it explicitly, as "deny by
default".

## Horizontal and vertical privilege abuse

Authorization mistakes go in two directions:

<figure class="fig"><div class="versus">
  <div><h4>Horizontal</h4>Reaching the data of <b>another user</b> at the same level. Ada seeing Alan's invoice.</div>
  <div><h4>Vertical</h4>Using <b>a higher privilege</b> one does not have. An ordinary user running "delete user" from the admin page.</div>
</div><figcaption>Both come from a missing or wrong check on the server.</figcaption></figure>

Vertical abuse is also called **privilege escalation**; its system-level
form is covered separately in the System Security module.

## Good authorization code

- **One place:** the permission decision is made in a single function;
  every endpoint calls that function. If decisions are spread through the
  code, it is easy to forget one.
- **Deny by default:** everything not in the rule is refused.
- **On the server, on every request:** a "I am an administrator" claim from
  the client is not trusted; the role is read from the record on the
  server.
- **At the object level:** the question is not only "this kind of object"
  but "this object".
- **Logging:** refused requests are recorded; someone trying different
  invoice numbers one after another shows up there.

## Summary

- Authorization is the question "may the subject do the action on the
  object?".
- The **access control matrix** shows every decision in one table; an
  **ACL** stores it column by column, a **capability list** row by row.
- The decision is made on the server, on every request and at the object
  level; hiding a button is not authorization.
- When the object-level check is forgotten, **IDOR** appears.
- **Horizontal** abuse reaches another user's data, **vertical** abuse
  reaches a higher privilege.
