# Digital Forensics Basics

In the Incident Response section we set a rule for containment: the
machine is not switched off or wiped; the traces on it are kept. Examining
those traces is called **digital forensics**: collecting, preserving and
examining digital evidence, and reporting the findings in a way others can
verify too.

The first rule of forensics is about trust, not technique: evidence is
valuable if it can be **shown not to have changed** from the moment it was
collected until the report. All the "evidence" in this section is fake: a
few bytes of text, made-up file records. No code touches a real disk or
system.

## The evidence hash

As soon as evidence is collected its **hash** is taken and recorded (the
Hash Functions section). The examination is done not on the evidence
itself but on a **copy**; if someone later asks "did the evidence change?",
the hash is calculated again:

```python
import hashlib

evidence = b"disk image of pc-bob (toy)"
recorded = hashlib.sha256(evidence).hexdigest()
print(recorded[:16])

copy = bytes(evidence)
print(hashlib.sha256(copy).hexdigest() == recorded)
changed = evidence.replace(b"bob", b"eve")
print(hashlib.sha256(changed).hexdigest() == recorded)
```

```text
1f27ccdc5b39f4f7
True
False
```

The copy's hash matches the record: the examination can be done on the
copy. Once a single word changed, the hash no longer matched. In real
examinations a disk is read through a **write blocker**, which stops
anything being written to it while it is copied.

## The chain of custody

Who held the evidence, when, and why is documented with an unbroken record;
this is called the **chain of custody**. Every handover records the giver
and the taker; if a link is missing, the question "what happened to the
evidence in between?" has no answer:

```python
CUSTODY = [
    ("2026-11-01 02:40", "responder-ada", "lab-locker", "collected, sha256 recorded"),
    ("2026-11-01 09:15", "lab-locker", "analyst-eve", "copy made for analysis"),
    ("2026-11-02 17:00", "analyst-joe", "lab-locker", "returned"),
]
holder = CUSTODY[0][1]
for when, giver, taker, note in CUSTODY:
    if giver != holder:
        print("gap before", when, ": expected", holder, "but got", giver)
    holder = taker
print("last holder:", holder)
```

```text
gap before 2026-11-02 17:00 : expected analyst-eve but got analyst-joe
last holder: lab-locker
```

The evidence was given to `analyst-eve`, but the one who brought it back
was `analyst-joe`. There is no record of the evidence changing hands in
between; such a gap can lower the value of the findings in court or in an
internal investigation.

## Collection order: volatility

Some traces disappear very fast. When a computer is switched off,
everything in memory is erased; the disk remains, and backups last even
longer. That is why evidence is collected **from the most volatile to the
most lasting**:

```python
SOURCES = [
    ("backup tapes", 5),
    ("memory (RAM)", 1),
    ("disk", 4),
    ("network connections", 2),
    ("running processes", 2),
    ("temporary files", 3),
]
for name, volatility in sorted(SOURCES, key=lambda s: (s[1], s[0])):
    print(volatility, name)
```

```text
1 memory (RAM)
2 network connections
2 running processes
3 temporary files
4 disk
5 backup tapes
```

Memory and open connections come first: switching the machine off destroys
exactly these. That is the reason for the "do not switch off, take it off
the network" rule in the Incident Response section.

## What the file says, what is inside

A file's extension is only part of its name and is easily changed. A
file's **real type** is told by its first bytes; these are called the
**file signature** or **magic bytes**. A file whose extension does not
match its type draws attention in an examination:

```python
SIGNATURES = {b"%PDF": "pdf", b"\x89PNG": "png", b"PK\x03\x04": "zip"}
FILES = {
    "report.pdf": b"%PDF-1.7 ...",
    "photo.png": b"PK\x03\x04 ...",
    "notes.txt": b"meeting at noon",
}
for name, data in FILES.items():
    kind = next((k for sig, k in SIGNATURES.items() if data.startswith(sig)), "unknown")
    ext = name.rsplit(".", 1)[1]
    flag = "" if kind in (ext, "unknown") else "  <- mismatch"
    print(f"{name:<11} {kind}{flag}")
```

```text
report.pdf  pdf
photo.png   zip  <- mismatch
notes.txt   unknown
```

The file named `photo.png` is really a zip archive: it may have been done
to hide something from view. Text files have no fixed signature; that is
why `unknown` was not counted as a mismatch.

## File times and the timeline

File systems keep several times for each file: last **modified**, last
**accessed**, and created or metadata changed. These times are another
source for the timeline from the Incident Response section:

```python
RECORDS = [
    ("/tmp/x.zip", "created", "02:17:40"),
    ("/srv/data/customers.csv", "accessed", "02:19:58"),
    ("/tmp/x.zip", "modified", "02:20:03"),
    ("/home/bob/.bash_history", "modified", "02:21:10"),
]
for path, kind, time in sorted(RECORDS, key=lambda r: r[2]):
    print(time, f"{kind:<8}", path)
```

```text
02:17:40 created  /tmp/x.zip
02:19:58 accessed /srv/data/customers.csv
02:20:03 modified /tmp/x.zip
02:21:10 modified /home/bob/.bash_history
```

A few seconds after the customer file was read, the archive in the
temporary folder changed: an order that suggests the exported data was
being packed. But file times are **not conclusive evidence**: they can be
changed and their interpretation depends on the file system. That is why
findings are confirmed with several independent sources (network logs,
application logs).

## The report

At the end of the examination a **report** is written: what was collected,
what its hashes were, which tool and method were used, what was found and
what was **not** found. The report says only what the evidence shows, does
not present a guess as evidence, and is detailed enough that another
expert could follow the same steps and reach the same result.

## Summary

- **Digital forensics:** collecting, preserving and examining digital
  evidence and reporting it verifiably.
- When evidence is collected its **hash** is recorded; the examination is
  done on a **copy**.
- The **chain of custody** documents every change of hands without a
  break.
- Collection starts **with the most volatile**: memory, connections,
  processes, then disk.
- A file's real type is told by its **signature**, not its extension.
- File times are useful but not conclusive; findings are confirmed with
  several sources.
