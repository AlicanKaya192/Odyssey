# Operating System Security

The operating system is the referee of everything on a computer: it decides
which program may open which file, touch which memory, or reach the
network. For an attacker, taking over the operating system means taking
over everything; for a defender, setting the operating system up correctly
means protecting every program on it.

This section covers how the operating system provides security and how we
**harden** a system. The code is again toy models: it does not touch real
system settings, it only builds the same logic with dicts.

## Kernel mode and user mode

The processor runs in two modes. **Kernel mode** can reach everything: all
memory, all hardware. **User mode** is restricted. Applications (the
browser, a game, your Python program) run in user mode and, for a
privileged job such as opening a file, they **make a request** to the
kernel. This request is called a **system call**. The kernel checks every
request and either allows or refuses it.

<figure class="fig"><div class="versus">
  <div><h4>User mode</h4>Applications run here. They cannot reach the hardware or other programs' memory directly; for every privileged job they make a <b>system call</b>.</div>
  <div><h4>Kernel mode</h4>The operating system's kernel runs here. It reaches everything and <b>checks</b> every system call: who is asking, and are they allowed?</div>
</div><figcaption>The boundary stops a bug in user mode from taking over the whole system.</figcaption></figure>

Let us see this split with a small model. The operations each role may do
are in a set; the "kernel" answers a request by looking at the set:

```python
POLICY = {
    "user": {"read_own_file", "open_window"},
    "admin": {"read_own_file", "open_window", "install_driver", "change_time"},
}


def syscall(role, operation):
    if operation in POLICY.get(role, set()):
        return "allowed"
    return "denied"


print(syscall("user", "open_window"))
print(syscall("user", "install_driver"))
print(syscall("admin", "install_driver"))
print(syscall("guest", "open_window"))
```

```text
allowed
denied
allowed
denied
```

The ordinary user could open a window but not install a driver; the admin
could. The `guest` role, which is not in the policy at all, could do
nothing: what is not on the list is **refused**. This is the operating
system's version of the **default deny** principle from the Security
Principles section.

## Process isolation

Every running program is called a **process**. The operating system gives
each process its own memory space and stops one process from reading
another's memory. The session cookie in the browser sits where a game open
at the same time cannot reach it:

```python
memory = {
    "browser": {"cookie": "abc123"},
    "game": {"score": 4200},
}


def read(process, owner, key):
    if process != owner:
        return "access denied"
    return memory[owner][key]


print(read("browser", "browser", "cookie"))
print(read("game", "browser", "cookie"))
```

```text
abc123
access denied
```

The browser read its own cookie; the game's identical request was refused.
In real systems the hardware (the memory management unit) and the kernel
do this check together. Thanks to isolation, a bug in one program or a
malicious add-on cannot reach other programs' data on its own. Browsers
running each tab in a separate process (a **sandbox**) take this idea one
step further.

## Accounts and least privilege

Every process on the operating system runs on behalf of an **account** and
carries that account's privileges. A program running with an administrator
account (`root` on Linux, Administrator on Windows) can do everything; a
bug in that program can do everything too. That is why:

- Daily work is done with a **standard** account; administrator privilege
  is requested only at the moment and for the job that needs it (`sudo` on
  Linux, a User Account Control prompt on Windows).
- Services run with their own restricted accounts, not as administrator.
- Unused accounts (the guest account, former employees' accounts) are
  disabled.

This is the principle from the Least Privilege and Separation of Duties
section applied to the operating system.

## Updates: the version comparison trap

Most known vulnerabilities are used against systems where the fix has
already been released but **not installed**. Checking for updates is
therefore a basic security job. A script that does it compares the
installed version with the version in which the vulnerability was fixed.
But comparing versions as text gives the wrong answer:

```python
print("2.4.10" < "2.4.9")


def version(text):
    return tuple(int(part) for part in text.split("."))


print(version("2.4.10") < version("2.4.9"))
print(version("2.4.10"))
```

```text
True
False
(2, 4, 10)
```

Text comparison goes character by character, and since `"1"` comes before
`"9"`, `2.4.10` is taken to be smaller than `2.4.9`. A check written with
this bug may think a system running `2.4.10` is "old", or worse, count an
old version as "current". The right way is to turn the version into a
tuple of numbers: tuples are compared number by number and `10 > 9`.

## Hardening the system

**Hardening** means making a system's default installation more secure:
switching off what is not needed and switching on the protections that
are. Instead of doing this by hand on every computer, the rules are
written into a list and the system's configuration is checked against it:

```python
CONFIG = {
    "auto_update": False,
    "firewall": True,
    "guest_account": True,
    "admin_daily_use": True,
    "disk_encryption": False,
}
RULES = [
    ("auto_update", True, "turn on automatic updates"),
    ("firewall", True, "turn on the firewall"),
    ("guest_account", False, "disable the guest account"),
    ("admin_daily_use", False, "use a standard account daily"),
    ("disk_encryption", True, "encrypt the disk"),
]
for key, wanted, advice in RULES:
    if CONFIG.get(key) != wanted:
        print("-", advice)
```

```text
- turn on automatic updates
- disable the guest account
- use a standard account daily
- encrypt the disk
```

4 of the five rules failed; only the firewall was as wanted. In
organisations these lists are written as a **security baseline** and every
computer is checked against them at regular intervals.

| Hardening step | Why? |
|---|---|
| Turn on automatic updates | Known vulnerabilities get closed |
| Switch off unused services | The attack surface shrinks |
| Disable guest and old accounts | No unwatched way in remains |
| Do daily work with a standard account | A bug does not gain admin privilege |
| Encrypt the disk | Data on a stolen device cannot be read |
| Turn on the firewall | Unneeded connections are blocked |

Every unneeded service is, as we saw in the Attack Surface section, an
extra door: it has vulnerabilities even if unused, and its updates get
forgotten.

## Summary

- The operating system is the **referee**: applications run in user mode,
  make **system calls** for privileged jobs, and the kernel checks them.
- What is not in the policy is **refused** (default deny).
- **Process isolation:** each process sees its own memory; one program's
  bug does not reach another's data.
- Daily work with a **standard account**; administrator privilege only
  when needed.
- Versions are compared as **tuples of numbers**, not as text.
- **Hardening:** switch off what is not needed, switch the protections
  on, check the configuration regularly against a baseline.
