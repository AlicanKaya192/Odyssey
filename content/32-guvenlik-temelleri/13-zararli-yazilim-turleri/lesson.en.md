# Types of Malware

**Malware** (malicious software) is a program written to harm a computer,
control it or steal information from it against its owner's wishes. This
section is about **recognising** the kinds, how they get in and how we
defend against them. We do not write or study harmful code; every example
here is a small tool from the defending side and works on harmless text.

## Kinds

Malware is named by **how it spreads** and **what it does**. One program
can have features of more than one kind.

| Kind | How it spreads / what it does |
|---|---|
| **Virus** | Attaches itself to another file or program; runs when that file is run and copies itself into other files. It needs a user to open something. |
| **Worm** | Spreads from computer to computer **by itself**, using vulnerabilities on the network, without waiting for anyone to open anything. |
| **Trojan** | Looks like a useful program (a free game, a "driver updater"); the user installs it themselves, and it does something else in the background. It does not spread by itself. |
| **Ransomware** | Encrypts files and demands money to unlock them; often also steals a copy and threatens to publish it. |
| **Spyware** | Secretly collects information: sites visited, documents, location. |
| **Keylogger** | Records the keys pressed; to capture passwords. |
| **Adware** | Shows unwanted adverts; often arrives bundled with other programs. |
| **Rootkit** | Settles deep in the system to **hide** its presence from the operating system and security tools. |
| **Backdoor** | A hidden way left so that the attacker can come back later, skipping normal authentication. |
| **Bot and botnet** | A taken-over computer that receives commands remotely; thousands together are used for denial of service or spam. |
| **Cryptojacking** | Uses the computer's processor to produce cryptocurrency without the owner knowing. |
| **Fileless malware** | Runs in memory through tools already on the system, without leaving a file on disk; so a file scan does not see it. |

The difference between a virus and a worm is a common exam question: **a
virus needs a carrier and a user**, **a worm needs neither**. A trojan
gets in through **deception**, not by spreading.

## How do they get in?

- **E-mail attachments and links** (Social Engineering section).
- **Fake downloads:** "free" versions, fake update warnings.
- **Unpatched vulnerabilities:** worms and automated attacks spread through
  these (the old CVEs from the Threats, Vulnerabilities and Risk section).
- **Removable storage:** USB sticks, external disks.
- **The supply chain:** a program or library you trust is itself taken
  over; harmful code arrives with an update. In detail in the System
  Security module.
- **Remote access services** with weak or stolen passwords.

## How are they detected?

There are two basic approaches.

**Signature-based detection:** the hashes of known harmful files are kept
in a list; if the hash of a scanned file is in the list, it is caught. It
is fast and makes few mistakes. Its weakness is this:

```python
import hashlib


def sha(data):
    return hashlib.sha256(data).hexdigest()


known_bad = {sha(b"TOY-SAMPLE-A"), sha(b"TOY-SAMPLE-B")}
files = {"report.pdf": b"quarterly numbers",
         "tool.exe": b"TOY-SAMPLE-A",
         "tool2.exe": b"TOY-SAMPLE-A!"}
for name, data in files.items():
    print(name, "match" if sha(data) in known_bad else "no match")
```

```text
report.pdf no match
tool.exe match
tool2.exe no match
```

The "files" here are only harmless text. `tool2.exe` differs from the known
sample by **a single byte**; because its hash changed completely, the
signature list did not recognise it. Real malware also changes itself a
little with every infection to escape signatures. A signature list also
knows nothing about a brand-new kind.

**Behaviour-based detection:** it looks not at the file itself but at
**what it does**. Ransomware reads a large number of files in a short time
and replaces them with encrypted versions; a backup program also writes
many files but does not change their extensions:

```python
events = {"backup.exe": {"files_written": 4000, "extensions_changed": 0},
          "unknown.exe": {"files_written": 3800, "extensions_changed": 3700},
          "editor.exe": {"files_written": 12, "extensions_changed": 0}}
for name, e in events.items():
    ratio = e["extensions_changed"] / e["files_written"]
    alarm = e["files_written"] > 1000 and ratio > 0.5
    print(f"{name:<12} {ratio:.2f}", "suspicious" if alarm else "ok")
```

```text
backup.exe   0.00 ok
unknown.exe  0.97 suspicious
editor.exe   0.00 ok
```

Behaviour detection can also catch new kinds, but it is more prone to
**false positives**: a legitimate program that changes its files'
extensions in bulk can be flagged too. Real tools use both approaches
together.

A trace of an attack is called an **indicator of compromise** (IOC): the
hash of a known harmful file, a suspicious domain connected to, an
unexpected service. In incident response, logs are searched for these
indicators (System Security module).

## Defence

A single product is not enough against malware; all the principles of the
earlier sections come together here:

- **Updating:** a patched vulnerability stops the worm that spreads
  through it.
- **Least privilege:** malware opened from a non-administrator account
  cannot settle deep into the system.
- **Application allowlisting:** allowing only approved programs to run;
  deny by default.
- **E-mail and web filters**, user training.
- **Network segmentation:** a worm that gets into one computer cannot
  spread to the whole network.
- **Backups:** the strongest answer to ransomware.

## The 3-2-1 backup rule

Ransomware tries to encrypt not only files but also the **backups** it can
reach. That is why how a backup is kept matters at least as much as having
one. The common rule is **3-2-1**: at least **3** copies of the data
(including the original), on at least **2** different media, at least
**1** of them somewhere else. Today one more condition is added: at least
one copy must be **offline** or **immutable**, so that malware on the
network cannot reach it.

```python
copies = [{"media": "laptop", "offsite": False, "offline": False},
          {"media": "usb-disk", "offsite": False, "offline": True},
          {"media": "cloud", "offsite": True, "offline": False}]
print("3 copies:", len(copies) >= 3)
print("2 media:", len({c["media"] for c in copies}) >= 2)
print("1 offsite:", any(c["offsite"] for c in copies))
print("1 offline:", any(c["offline"] for c in copies))
```

```text
3 copies: True
2 media: True
1 offsite: True
1 offline: True
```

A backup must also be **tested**: whether a backup that has never been
restored works is only found out on the day of the disaster, which is too
late.

## If a ransom is demanded

Most organisations advise not paying: paying does not guarantee the files
come back, it encourages the attacker to strike again, and in some
countries it creates legal problems. The right order: separate the
affected computers from the network, start the incident response plan,
restore from a clean backup, find how they got in and close that door.

## Summary

- Kinds of malware are named by spreading and behaviour: a virus needs a
  carrier, a worm spreads by itself, a trojan deceives, ransomware
  encrypts, a rootkit hides.
- Ways in: e-mail, fake downloads, unpatched vulnerabilities, USB, the
  supply chain, weak remote access.
- **Signature-based** detection is fast but fooled by a one-byte change;
  **behaviour-based** detection catches the new but can raise false
  alarms.
- Defence: updating, least privilege, allowlisting, filters, training,
  network segmentation, backups.
- Backups: **3-2-1** and at least one offline copy; backups are restored
  and tested regularly.
