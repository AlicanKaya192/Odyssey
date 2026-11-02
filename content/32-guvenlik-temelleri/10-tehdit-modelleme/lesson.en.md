# Threat Modelling and STRIDE

The cheapest time to close a vulnerability is before it has even been
written. **Threat modelling** means asking "what can go wrong here?" **in
a structured way** before building or changing a system. A code review
looks at lines already written; threat modelling looks at the design,
that is, at how the parts are connected.

## Four questions

All threat modelling methods rest on four questions:

1. **What are we working on?** A drawing of the system.
2. **What can go wrong?** A list of threats.
3. **What are we going to do about it?** An answer to every threat (a
   control, acceptance, transfer; the four answers from the Assessing Risk
   section).
4. **Did we do a good job?** Is the list complete, were the controls
   applied?

This section focuses on the first two questions.

## Drawing the system: a data flow diagram

A common way of drawing the system is a **data flow diagram** (DFD). It has
only five parts:

| Part | Meaning | Example |
|---|---|---|
| **External entity** | A person or system not under your control | A student, a payment service |
| **Process** | Code that handles data | The web application |
| **Data store** | Where data sits | A database, a file |
| **Data flow** | Data going between parts | A login request, a query |
| **Trust boundary** | The line where the level of trust changes | Between the internet and the internal network |

The simplest form of a school grades system:

<figure class="fig"><div class="flow">
  <span class="node">Student</span><span class="arrow">→</span>
  <span class="node acc">Web application</span><span class="arrow">→</span>
  <span class="node">Grades database</span>
</div><figcaption>The student is on the internet, the application and the database on the internal network. The first arrow crosses a trust boundary.</figcaption></figure>

The **trust boundary** is the most important part. Most attacks happen on a
data flow that crosses a boundary: nothing that comes from outside should
be used inside without being checked. Finding whether a flow crosses a
boundary is easy; if its two ends are in different zones, it crosses:

```python
zones = {"student": "internet", "web app": "internal", "grades db": "internal"}
flows = [("student", "web app"), ("web app", "grades db"), ("grades db", "web app")]
for src, dst in flows:
    crosses = zones[src] != zones[dst]
    print(f"{src} -> {dst}:", "crosses boundary" if crosses else "same zone")
```

```text
student -> web app: crosses boundary
web app -> grades db: same zone
grades db -> web app: same zone
```

## What can go wrong? STRIDE

Writing "what can go wrong?" on an empty page is hard. **STRIDE** splits
the question into six categories; every letter is a kind of threat and
every kind breaks one security property:

```python
STRIDE = {
    "S": ("Spoofing", "authenticity"),
    "T": ("Tampering", "integrity"),
    "R": ("Repudiation", "non-repudiation"),
    "I": ("Information disclosure", "confidentiality"),
    "D": ("Denial of service", "availability"),
    "E": ("Elevation of privilege", "authorization"),
}
for letter, (threat, prop) in STRIDE.items():
    print(letter, f"{threat:<23}", prop)
```

```text
S Spoofing                authenticity
T Tampering               integrity
R Repudiation             non-repudiation
I Information disclosure  confidentiality
D Denial of service       availability
E Elevation of privilege  authorization
```

With examples:

| Letter | Threat | Property it breaks | Example in the grades system |
|---|---|---|---|
| **S** | Spoofing | Authenticity | Logging in as a teacher with someone else's password |
| **T** | Tampering | Integrity | A grade changed on the way or in the database |
| **R** | Repudiation | Non-repudiation | A teacher who changed a grade saying "it wasn't me"; there is no log |
| **I** | Information disclosure | Confidentiality | All grades showing up in an error message |
| **D** | Denial of service | Availability | The site flooded with requests on results day |
| **E** | Elevation of privilege | Authorization | A student being able to use the grade entry page |

The first five letters match CIA and the concepts next to it (What Is
Security section); the sixth matches authorization. That is why STRIDE
works like a checklist: six questions are asked for every part.

## Which letters for which part?

Not every letter fits every part. A data store does not spoof anyone; you
cannot tamper with an external entity (it is not under your control).
Which letters are asked for which part is decided by a table; this is
called **STRIDE per element**:

```python
PER_ELEMENT = {"external_entity": "SR", "process": "STRIDE",
               "data_store": "TRID", "data_flow": "TID"}
system = [("student", "external_entity"), ("web app", "process"),
          ("grades db", "data_store"), ("login request", "data_flow"),
          ("query", "data_flow")]
total = 0
for name, kind in system:
    letters = PER_ELEMENT[kind]
    total += len(letters)
    print(f"{name:<14} {letters}")
print("threats to consider:", total)
```

```text
student        SR
web app        STRIDE
grades db      TRID
login request  TID
query          TID
threats to consider: 18
```

Even a small drawing of five parts produces 18 questions. For
each one we think "is this threat possible here, and if so what do we do?".
For some the answer will be "there is already a control" or "this makes no
sense in this system"; what matters is that none is skipped. The **R** for
a data store is for when the store is a log store: if the logs are tampered
with, repudiation becomes easy.

## What is done with the threats found?

Every threat becomes a row: which part, which letter, what could happen,
likelihood and impact (the scores from the Assessing Risk section), the
answer and the person responsible. Then they are sorted, starting with the
highest scores. A threat model is not written once and put in a drawer: it
is updated when a new part, a new data flow or a new trust boundary is
added to the system.

## When is it done?

- While designing a new system, before code is written.
- For a big change: a new outside service, a new kind of data, a new way
  in.
- After an incident: had the model foreseen it?

Threat modelling is not a job an expert does alone. The best results come
from talking it through at a table, over the diagram, with the people who
build the system.

## Summary

- Threat modelling asks "what can go wrong?" in a structured way at the
  design stage. Four questions: what are we doing, what can go wrong, what
  will we do, did we do a good job.
- **Data flow diagram:** external entity, process, data store, data flow
  and **trust boundary**. Attacks happen most on flows that cross a
  boundary.
- **STRIDE:** spoofing, tampering, repudiation, information disclosure,
  denial of service, elevation of privilege; each one breaks a security
  property.
- **STRIDE per element** says which letter is asked for which part.
- Threats are scored and answered, and the model is updated as the system
  changes.
