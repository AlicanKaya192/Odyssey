# Secure Software Development (SDLC)

So far we have seen individual vulnerabilities and the defenses against
them. But secure software does not come out of a "security check" done the
day before release. Security is a **process** spread over every step of
the software's life, from the idea to its retirement.

The steps software goes through from start to finish are called the
**Software Development Life Cycle** (SDLC). The version with security work
added to every step is called a **secure SDLC**. This section covers those
steps and the work done in each, with small Python examples.

## The steps of the cycle

<figure class="fig"><div class="flow">
  <span class="node">Requirements</span><span class="arrow">→</span>
  <span class="node">Design</span><span class="arrow">→</span>
  <span class="node">Coding</span><span class="arrow">→</span>
  <span class="node">Verification</span><span class="arrow">→</span>
  <span class="node ok">Release and maintenance</span>
</div><figcaption>Security is in every step; not only in one check at the end.</figcaption></figure>

| Step | Security work |
|---|---|
| **Requirements** | Writing security requirements: who reaches what, which data is secret, which law applies |
| **Design** | Threat modelling (the Threat Modelling and STRIDE section), choosing secure defaults |
| **Coding** | Secure coding rules, input validation, code review |
| **Verification** | Security tests, static analysis, dependency scanning |
| **Release and maintenance** | A release gate, patching, monitoring, incident response |

The earlier you find a bug, the cheaper it is to fix: a missing permission
noticed during design means changing a drawing, while the same gap noticed
after release is an incident. Pulling security work towards the start of
the cycle is called **shifting left**.

## Principle 1: fail securely

What should happen when a check meets an unexpected error? There are two
options: **fail open** (allow when there is an error) or **fail closed**
(refuse when there is an error).

```python
def lookup_role(user):
    roles = {"ada": "admin", "bob": "user"}
    return roles[user]


def is_admin_fail_open(user):
    try:
        return lookup_role(user) == "admin"
    except Exception:
        return True


def is_admin_fail_closed(user):
    try:
        return lookup_role(user) == "admin"
    except KeyError:
        return False


print(is_admin_fail_open("mallory"))
print(is_admin_fail_closed("mallory"))
```

```text
True
False
```

No role was found for the unregistered `mallory`. The version that fails
open read this error as "administrator"; the one that fails closed refused.
In security checks the rule is always the same: **when in doubt, refuse**.
Also, `except Exception` swallows every error and so hides other errors
too; only the expected error (`KeyError`) is caught.

## Principle 2: secure defaults

What happens when a program's settings are not given decides a large part
of its security, because most installations never change the defaults.
That is why defaults are chosen to be **secure** and the settings the user
gives are applied only for known keys:

```python
DEFAULTS = {"debug": False, "tls": True, "session_minutes": 30}


def load_config(user_config):
    config = dict(DEFAULTS)
    for key, value in user_config.items():
        if key in DEFAULTS:
            config[key] = value
    return config


print(load_config({}))
print(load_config({"debug": True, "colour": "red"}))
```

```text
{'debug': False, 'tls': True, 'session_minutes': 30}
{'debug': True, 'tls': True, 'session_minutes': 30}
```

With no settings at all, debugging comes off and encrypted connections on.
The unknown `colour` key was silently skipped. A dangerous setting such as
debug mode is switched on only when **explicitly** asked for: something
insecure should be a conscious choice, not a forgotten default.

## Principle 3: validate input

Every piece of data from outside (a form, a file, a request) is untrusted.
Validation is done with an **allow list**: what is valid is described, and
everything else is refused.

```python
def parse_quantity(text):
    if not text.isdigit():
        return None
    value = int(text)
    if not 1 <= value <= 100:
        return None
    return value


for text in ["3", "0", "250", "-1", "2e3", " 4", ""]:
    print(repr(text), parse_quantity(text))
```

```text
'3' 3
'0' None
'250' None
'-1' None
'2e3' None
' 4' None
'' None
```

Only `3` passed. Zero and 250 are out of range; the input with a minus
sign, the one in scientific notation, the one with a space and the empty
one failed the format check. "Describing what is good" is safer than
"filtering out bad characters" (a deny list), because forgetting to add
something to a deny list is always possible. The details of input
validation are in the Input Validation and Output Encoding section.

## Verification: security tests

If security requirements are written as tests, they are checked
automatically after every change. The most valuable security tests are the
**"must not"** cases: testing not only that the author can delete but also
that a stranger cannot.

```python
def can_delete(user, post):
    return user["role"] == "admin" or post["author"] == user["name"]


TESTS = [
    ("author can delete", {"name": "ada", "role": "user"}, {"author": "ada"}, True),
    ("stranger cannot delete", {"name": "bob", "role": "user"}, {"author": "ada"}, False),
    ("admin can delete", {"name": "eve", "role": "admin"}, {"author": "ada"}, True),
]
for name, user, post, expected in TESTS:
    result = "pass" if can_delete(user, post) == expected else "FAIL"
    print(f"{result}: {name}")
```

```text
pass: author can delete
pass: stranger cannot delete
pass: admin can delete
```

All three tests passed. If someone later changes `can_delete` and breaks
the ownership check, the "stranger cannot delete" test fails at once and
the bug is caught before release.

## The release gate

At the end of the cycle stands a **release gate**: no release goes out
until certain security work is done. The gate is a checklist and is
checked automatically in the build pipeline (CI):

```python
CHECKLIST = {
    "threat_model_reviewed": True,
    "security_tests_pass": True,
    "dependencies_scanned": False,
    "secrets_scan_clean": True,
}
blockers = sorted(item for item, done in CHECKLIST.items() if not done)
print("release blocked" if blockers else "release ok")
print(blockers)
```

```text
release blocked
['dependencies_scanned']
```

The release stopped because the dependency scan was not done. A gate's
value is in being applied **without exception**: a gate passed "just this
once" stops being a gate.

## Summary

- Security is a process spread over every step of the **SDLC**; it is not
  a single check done at the end.
- The earlier a bug is found, the cheaper it is: **shift left**.
- **Fail securely:** refuse when there is an error; catch only the
  expected error.
- **Secure defaults:** a dangerous setting is switched on only when
  explicitly asked for.
- **Validate input with an allow list:** describe the good, refuse the
  rest.
- **Security tests** also test the "must not" cases; the **release gate**
  is applied without exception.
