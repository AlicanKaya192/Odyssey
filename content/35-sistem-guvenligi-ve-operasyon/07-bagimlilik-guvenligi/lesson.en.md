# Dependencies and the Supply Chain

Most programs written today do not write most of their code themselves:
they use packages (libraries). A web application uses a web framework, the
framework uses a template library, and that library uses other packages.
Behind the few hundred lines you write run tens of thousands of lines
written by others.

Each of these packages is part of the program, and **their
vulnerabilities are your vulnerabilities**. The whole path from a
package's developer to your computer is called the **software supply
chain**. This section covers how to protect that chain: pinning versions,
transitive dependencies, comparing against known vulnerabilities,
lookalike package names and hash verification. The examples are again
toys: no real package is downloaded, names and versions sit in dicts.

## Direct and transitive dependencies

A package you install explicitly is a **direct dependency**; the ones it
uses itself are **transitive dependencies**. Transitive dependencies are
usually unseen, but they run all the same:

```python
GRAPH = {
    "app": ["web", "db"],
    "web": ["templates", "http"],
    "db": ["http", "pool"],
    "templates": ["escape"],
    "http": [],
    "pool": [],
    "escape": [],
}


def all_deps(graph, root):
    seen = set()
    stack = list(graph[root])
    while stack:
        name = stack.pop()
        if name not in seen:
            seen.add(name)
            stack.extend(graph.get(name, []))
    return seen


print("direct:", len(GRAPH["app"]))
print("all:", len(all_deps(GRAPH, "app")), sorted(all_deps(GRAPH, "app")))
```

```text
direct: 2
all: 6 ['db', 'escape', 'http', 'pool', 'templates', 'web']
```

The application asked for only 2 packages but runs with
6. We never chose the `escape` package, yet a vulnerability in it
would be in our application too. The `seen` set makes sure the same
package (`http` comes from two places) is counted once and that a graph
with a cycle does not loop forever. This list of every package used is
called a **Software Bill of Materials** (SBOM).

## Pinning the version

If a file such as `requirements.txt` gives no package version, or only a
lower bound, every installation takes the newest version of that day. An
installation that works today may be installed with different code
tomorrow; that new version may be broken or malicious. That is why
versions are **pinned**:

```python
REQUIREMENTS = """numpy==2.1.3
pandas>=2.0
flask
# test tools
pytest==8.3.4
"""
for line in REQUIREMENTS.splitlines():
    line = line.strip()
    if not line or line.startswith("#"):
        continue
    status = "pinned" if "==" in line else "NOT pinned"
    print(f"{line:<14} {status}")
```

```text
numpy==2.1.3   pinned
pandas>=2.0    NOT pinned
flask          NOT pinned
pytest==8.3.4  pinned
```

`pandas>=2.0` and `flask` are not pinned: a different version may come on
every installation. Pinning makes the installation **reproducible**. The
cost is that updates no longer arrive on their own; pinned versions are
updated deliberately and regularly (the next step).

## Comparing against known vulnerabilities

Package vulnerabilities are published as **security advisories** that say
which versions are affected: in which version the vulnerability appeared
and in which it was fixed. If the installed version is in that range, the
package is affected. Versions are compared as tuples of numbers, as we saw
in the Operating System Security section:

```python
def version(text):
    return tuple(int(p) for p in text.split("."))


INSTALLED = {"web": "2.3.1", "http": "1.9.0", "pool": "0.4.2"}
ADVISORIES = [
    ("web", "2.0.0", "2.3.2", "ADV-1"),
    ("http", "1.0.0", "1.8.0", "ADV-2"),
    ("pool", "0.1.0", "0.5.0", "ADV-3"),
]
for name, introduced, fixed, adv in ADVISORIES:
    v = version(INSTALLED[name])
    if version(introduced) <= v < version(fixed):
        print(f"{name} {INSTALLED[name]} affected by {adv}, fix: {fixed}")
```

```text
web 2.3.1 affected by ADV-1, fix: 2.3.2
pool 0.4.2 affected by ADV-3, fix: 0.5.0
```

`web` and `pool` are in the affected range; `http` is already on a fixed
version. Doing this by hand every day is not possible; **dependency
scanning** tools (SCA) compare the installed package list with advisory
databases automatically and run in the build pipeline.

## Lookalike packages

Some supply chain attacks do not even bother finding a vulnerability: a
malicious package is published under a name **very similar** to a popular
package, waiting for a developer who mistypes one letter to install it.
This is called **typosquatting**. The defender can compare a newly added
package name with known popular names:

```python
import difflib

POPULAR = ["numpy", "pandas", "django", "flask", "pytest"]
for name in ["numpi", "pandas", "flaskk", "djang0", "leftpad"]:
    if name in POPULAR:
        print(name, "ok")
        continue
    close = difflib.get_close_matches(name, POPULAR, n=1, cutoff=0.8)
    print(name, "-> looks like " + close[0] if close else "unknown")
```

```text
numpi -> looks like numpy
pandas ok
flaskk -> looks like flask
djang0 -> looks like django
leftpad unknown
```

`numpi`, `flaskk` and `djang0` are very close to popular names: a human
should look before they are installed. `leftpad` resembles none of them;
not resembling does not mean safe, it is only not this check's concern.
`difflib`'s similarity ratio is between 0 and 1; the `cutoff` threshold,
like the threshold in the Privilege Escalation section, sets the balance
between false alarms and misses.

A related attack is **dependency confusion**: a package with the same name
as an organisation's internal package is published to a public index, and
misconfigured install tools choose the version on the public index. The
defense is writing explicitly which index internal packages come from.

## Hash verification and the lock file

Pinning a version says **which** version will be installed; it does not
prove that the downloaded file really is that version. A **lock file**
keeps, next to every package's version, the **SHA-256 hash** of its file.
On installation the downloaded file's hash is calculated and compared (the
Hash Functions section):

```python
import hashlib


def digest(data):
    return hashlib.sha256(data).hexdigest()


LOCK = {"web-2.3.2.zip": digest(b"web package v2.3.2")}
print(digest(b"web package v2.3.2") == LOCK["web-2.3.2.zip"])
print(digest(b"web package v2.3.2 + extra") == LOCK["web-2.3.2.zip"])
```

```text
True
False
```

Once a single thing was added to the file, the hash did not match and the
installation is stopped. In pip this is done with the `--require-hashes`
option: no package without a hash, or with a hash that does not match, is
installed.

## Prevention list

| Threat | Prevention |
|---|---|
| A version with a known vulnerability | Dependency scanning, regular updates |
| A version that changes between installations | Version pinning, a lock file |
| A file changed in transit or on the index | Hash verification in the lock file |
| A malicious lookalike package | A human reviews a new dependency, a name similarity check |
| An internal package name imitated on a public index | Write the internal packages' index explicitly |
| An unneeded package | Few dependencies: every package is a risk |

## Summary

- A program's **supply chain** is every package it uses, **transitive**
  dependencies included.
- **SBOM:** the list of every package used.
- **Pin** versions; update pinned versions deliberately and regularly.
- Compare with **security advisories**: if the installed version lies
  between the version where the vulnerability appeared and the version
  where it was fixed, the package is affected.
- **Typosquatting** and **dependency confusion** target names; a human
  reviews a new package.
- **The hash in a lock file** proves the downloaded file has not changed.
