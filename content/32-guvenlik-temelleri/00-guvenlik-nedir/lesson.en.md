# What Is Security? The CIA Triad

A computer system keeps something or does some job: a school system that
holds your grades, a banking app that sends money, a phone that backs up
your photos. **Information security** means making sure the system keeps
working the way its owners intend: only the people who should see the
information see it, nobody can change it without being noticed, and it can
be reached when it is needed.

This path looks from the **defending** side. You will learn about attacks,
but the aim is not to carry them out; it is to understand why they work and
to see how they are closed. The exercises always run on your own computer,
on small examples you build yourself.

## What are we protecting? Assets

Security starts with a question: **what** are we protecting? Anything worth
protecting is called an **asset**:

- **Data:** student grades, customer addresses, passwords, source code.
- **Services:** a website, a payment system, an e-mail server.
- **Hardware:** servers, laptops, phones.
- **Trust and reputation:** people continuing to trust you with their data.

Every asset has a different value, so they are not all protected equally
hard. The canteen menu and the students' health records do not sit behind
the same lock. You will learn how to decide how much protection an asset
gets in the next two sections (Threats, Vulnerabilities and Risk; Assessing
Risk).

## The CIA triad

An asset being "secure" means three separate things. From their initials
this is called the **CIA triad**; it has nothing to do with the
intelligence agency:

<figure class="fig anat">
  <div class="anat-row"><span><b>C</b>: Confidentiality</span><span>Only those authorised to see the information see it. If broken: the grade list ends up in everyone's hands.</span></div>
  <div class="anat-row"><span><b>I</b>: Integrity</span><span>The information cannot be changed without authorisation or without being noticed. If broken: a transfer amount is changed from 100 to 900 on the way.</span></div>
  <div class="anat-row"><span><b>A</b>: Availability</span><span>The information and the service can be reached by authorised people when needed. If broken: the system does not open on exam day.</span></div>
  <figcaption>The three legs of security. An incident can break one, two or all three of them.</figcaption>
</figure>

The three are independent and **can pull against each other**. If you lock
a file in a safe and throw away the key, its confidentiality is perfect,
but its availability drops to zero. A large part of security work is
balancing these three.

### Confidentiality

**Confidentiality** means the information is only disclosed to those
authorised to see it. Breaking it is called a **data leak**: a wrongly
configured shared folder, a stolen laptop, an e-mail sent to the wrong
person. To protect it we check who someone is (authentication), decide who
may see what (access control) and make the information unreadable
(encryption). Each of these has its own section.

### Integrity

**Integrity** means the information stays correct and complete: nobody can
change it without authorisation, and if it changes, that is noticed. What
breaks integrity is not always an attack; a file copy cut off halfway or a
failing disk also breaks it. To protect it we limit who can write, record
changes and take the data's **fingerprint**.

A fingerprint works like this: a short, fixed-length value is computed from
a text, and the smallest change in the text changes this value completely.
This value is called a **hash**; how it works is a topic of the
Cryptography module. For now, let us only look at how it behaves:

```python
import hashlib

original = "pay 100 to Ada"
changed = "pay 900 to Ada"
for text in [original, changed]:
    print(hashlib.sha256(text.encode()).hexdigest()[:16], text)
```

```text
7765ba48a9885011 pay 100 to Ada
81313d488d626434 pay 900 to Ada
```

There is only one character of difference between the two texts (`9`
instead of `1`), yet even the first 16 characters of the hashes look
nothing alike. Someone who keeps the hash of the original text in a safe
place notices at once when the text changes.

### Availability

**Availability** means the system is working when it is needed. Flooding
a server with more requests than it can carry (denial of service), a disk
failure, a power cut or malware that locks the files all break
availability. To protect it we take backups, run the same service on more
than one machine (redundancy) and limit overload.

Availability is often promised as a percentage: "the system will be up
99.9% of the year". Such a promise is called a **service level agreement**
(SLA). The percentages look very close to each other, but the time you are
allowed to be down changes a lot:

```python
minutes_per_year = 365 * 24 * 60
for percent in [99, 99.9, 99.99, 99.999]:
    down = minutes_per_year * (1 - percent / 100)
    print(f"{percent}% -> {down:.1f} minutes per year")
```

```text
99% -> 5256.0 minutes per year
99.9% -> 525.6 minutes per year
99.99% -> 52.6 minutes per year
99.999% -> 5.3 minutes per year
```

Each extra "9" cuts the allowed downtime by a factor of ten. 99% means
being down for 3.65 days a year; 99.999% means five
minutes a year. That is why high availability is very expensive.

## Which leg does an incident break?

A **security incident** is anything that breaks, or tries to break, at
least one of C, I and A. Naming the incident correctly is the first step to
choosing the right control. A small function that finds which legs an
incident breaks:

```python
def pillars(leaked, modified, unreachable):
    found = []
    if leaked:
        found.append("C")
    if modified:
        found.append("I")
    if unreachable:
        found.append("A")
    return found


print("grades leaked:", pillars(True, False, False))
print("amount changed:", pillars(False, True, False))
print("site down 3 hours:", pillars(False, False, True))
print("files locked, copy sold:", pillars(True, True, True))
```

```text
grades leaked: ['C']
amount changed: ['I']
site down 3 hours: ['A']
files locked, copy sold: ['C', 'I', 'A']
```

The last line is an example of **ransomware**: malware that encrypts files
and demands money to unlock them. The files cannot be used (availability),
their contents have been changed (integrity) and the attacker often takes a
copy and threatens to sell it (confidentiality). A single incident can
break all three legs.

## Three concepts next to CIA

CIA is the foundation but it does not cover everything. Three more
concepts you will meet often:

- **Authenticity:** a message or a person really comes from the source it
  claims. "Did my bank really send this e-mail?"
- **Accountability:** every action can be traced back to whoever did it.
  Logs are kept for this.
- **Non-repudiation:** a person cannot later deny an action they took by
  saying "it wasn't me". Digital signatures provide this (Cryptography
  module).

## Security is a balance

There is no perfect security; there is only security that is "enough for
this asset". Every control has a price: money, time and ease of use. A
system that asks for three different passwords at every login looks more
secure, but people start writing the passwords on paper and sticking them
to the screen, and the result is worse.

<figure class="fig"><div class="versus">
  <div class="no"><h4>Security as a product</h4>Bought once, installed, done. "We have a firewall, so we are safe."</div>
  <div class="ok"><h4>Security as a process</h4>Assets, threats and the system keep changing. Risk is measured regularly, controls are reviewed, lessons are learned from incidents.</div>
</div><figcaption>No single control protects a system for ever.</figcaption></figure>

## Summary

- Security means protecting an **asset**; first decide what is protected.
- **Confidentiality:** only the authorised see it. **Integrity:** it does
  not change unnoticed. **Availability:** it can be reached when needed.
- One incident can break more than one leg; ransomware breaks all three.
- Each "9" in an availability percentage cuts the allowed downtime by ten.
- Security is a balance and a process; a control nobody can use is useless.
