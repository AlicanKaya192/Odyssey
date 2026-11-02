# Security Principles

Tools change every year; new languages, new cloud services and new kinds of
attack appear. But the ideas behind well-protected systems have stayed
almost the same for half a century. Most of them were listed in a classic
paper written in 1975, and they are still the first questions of any
security review. This section looks at those **security principles**: what
each one says, why it works and how it looks in code.

## Least privilege

**Least privilege:** every user, every program and every service runs with
**just enough** privilege to do its job, and no more. A program written to
enter grades cannot delete student records; an employee who reads reports
cannot change them.

Why does it work? When an account is taken over or a program makes a
mistake, the damage is limited to that account's privileges. A single
administrator account that can do everything loses everything in a single
mistake. This principle has its own section (Least Privilege and Separation
of Duties).

## Deny by default

**Fail-safe defaults:** access decisions are made from an **allowlist**.
Everything not explicitly allowed is refused. The opposite is a
**blocklist**: what is forbidden is written down, the rest is free. The
problem with a blocklist is that you cannot forbid what you did not think
of.

Let us see it with the extension check of a file upload page:

```python
blocked = {"exe", "bat"}
allowed = {"pdf", "png", "jpg"}
for name in ["report.pdf", "tool.exe", "script.ps1", "photo.png"]:
    ext = name.rsplit(".", 1)[-1]
    print(f"{name:<11}", "blocklist:", ext not in blocked, "allowlist:", ext in allowed)
```

```text
report.pdf  blocklist: True allowlist: True
tool.exe    blocklist: False allowlist: False
script.ps1  blocklist: True allowlist: False
photo.png   blocklist: True allowlist: True
```

`script.ps1` passed the blocklist, because whoever wrote the list did not
think of this extension. The allowlist refused it by itself. Something
forgotten in an allowlist only leads to a user's complaint ("I cannot
upload a PNG"); something forgotten in a blocklist leads to a
vulnerability.

A related idea is **secure by default**: a product should be secure as it
comes out of the box. If the user touches no setting, debugging should be
off, a password required and encryption on.

## Fail securely

Programs fail: a file is not found, the network drops, an unexpected value
arrives. **Failing securely** means the system stays **closed** when
something goes wrong: if you cannot be sure, do not allow it. Look at what
a permission check returns when there is an error:

```python
def can_open_bad(user, acl):
    try:
        return acl[user] == "allow"
    except KeyError:
        return True


def can_open_good(user, acl):
    try:
        return acl[user] == "allow"
    except KeyError:
        return False


acl = {"ada": "allow", "alan": "deny"}
for user in ["ada", "alan", "mallory"]:
    print(user, can_open_bad(user, acl), can_open_good(user, acl))
```

```text
ada True True
alan False False
mallory True False
```

`mallory`, who is not in the list at all, got in with the bad version. The
error made it fail "open". For doors the opposite is sometimes wanted
(doors should not stay locked in a fire), but for access to data the rule
is to stay closed.

## Defence in depth

**Defence in depth:** do not rely on a single control; put **several
layers** one behind the other. Think of a castle: a moat, a wall, a gate,
a keep. Even if the attacker gets past one, the others can stop them.

If the chance of getting past each layer is written down, then as long as
the layers are independent of each other, the chance of getting past all
of them is the product:

```python
layers = {"firewall": 0.3, "patching": 0.2, "mfa": 0.1}
chance = 1.0
for name, passes in layers.items():
    chance *= passes
    print(f"after {name:<9} {chance:.3f}")
```

```text
after firewall  0.300
after patching  0.060
after mfa       0.006
```

On its own every layer looks weak (one lets one attack in three through),
but the three together let only six in a thousand through. The important
condition is **independence**: if all three layers rely on the same
password, they all fall at once when that password is stolen, and the
multiplication no longer holds. That is why it matters that layers are of
different kinds (technical, administrative, physical).

## Complete mediation

**Complete mediation:** every access is checked **every time**.
Remembering a permission given once and never asking again causes trouble
when the permission is taken back:

```python
permissions = {"ada": {"read", "write"}}
cached = set(permissions["ada"])
permissions["ada"].discard("write")
print("cached answer:", "write" in cached)
print("checked now:", "write" in permissions["ada"])
```

```text
cached answer: True
checked now: False
```

Ada's write permission was removed, but the code that read the permission
once and kept it still says "can write". The open session of someone who
left the company, or an access token that has not expired, is exactly this
problem.

## Open design

**Open design:** security should not depend on **how the system works**
staying secret; it should only depend on the keys staying secret. Everyone
knows how a lock is designed; the key is in your pocket. In cryptography
this idea is known as **Kerckhoffs's principle**.

Protecting a system by hiding its design is called **security through
obscurity**, and on its own it is weak: code leaks, a former employee
talks, someone studies the program. Hiding can be an extra layer, but it
cannot be the main one.

## Simplicity

**Economy of mechanism:** a security mechanism should be as small and
simple as possible. Every line is a chance for a bug, and a complex system
is hard to review. A permission check of a hundred lines is easier to
verify than one of a thousand.

## Separation of privilege

**Separation of privilege:** an important job is not left in the hands of
a single person or a single condition. A bank vault opens with two
separate keys; one person prepares a large payment and someone else
approves it. Taking over a single account, or one person's bad intent, is
not enough. Two-step login (next section) is the same idea applied to
authentication.

## Usability

**Psychological acceptability:** a security control should not make
people's work needlessly hard. If it does, people find a way around it:
they stick the password on the screen, they wedge the door open. A good
control makes the right behaviour the easiest behaviour.

## Summary

<figure class="fig anat">
  <div class="anat-row"><span>Least privilege</span><span>Enough privilege for the job, no more.</span></div>
  <div class="anat-row"><span>Deny by default</span><span>An allowlist; everything not mentioned is forbidden.</span></div>
  <div class="anat-row"><span>Fail securely</span><span>When there is an error, stay closed.</span></div>
  <div class="anat-row"><span>Defence in depth</span><span>Several layers, independent of each other.</span></div>
  <div class="anat-row"><span>Complete mediation</span><span>Check every access, every time.</span></div>
  <div class="anat-row"><span>Open design</span><span>The key is secret, not the design.</span></div>
  <div class="anat-row"><span>Simplicity</span><span>A small mechanism, few bugs.</span></div>
  <div class="anat-row"><span>Separation of privilege</span><span>Two hands for an important job.</span></div>
  <div class="anat-row"><span>Usability</span><span>Make the right behaviour the easiest one.</span></div>
  <figcaption>When reviewing a system, ask about every principle in turn: is it applied here?</figcaption>
</figure>
