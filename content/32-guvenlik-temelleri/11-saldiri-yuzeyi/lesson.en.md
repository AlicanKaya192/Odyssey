# Attack Surface

The more doors and windows a house has, the more places a burglar can try.
A system's **attack surface** is the sum of all the points where an
attacker can send data to the system, reach it or affect it. Each point is
called an **entry point**. The larger the surface, the more places there
are to defend and the higher the chance that a door goes unnoticed.

## Three kinds of surface

| Kind | Examples of entry points |
|---|---|
| **Digital** | Web pages and forms, API endpoints, file uploads, open network services, the admin panel, the update mechanism, the outside libraries used |
| **Physical** | USB ports, an unlocked server room, laptops that can get lost, papers left in the printer |
| **Human** (social) | Employees reachable by e-mail and phone, the help desk, suppliers |

This section focuses on the digital surface; the human surface is the topic
of the Social Engineering section.

## Inventory first

You cannot lock a door you do not know about. The first step in shrinking
the attack surface is taking an **inventory**: which servers, which
endpoints, which services are there, and who uses them? A test server a
team opened without asking anyone, or a forgotten old page (**shadow IT**),
are the doors most often missed.

## Not every entry point is the same

Two questions largely decide how exposed an entry point is:

- **Who can reach it?** Everyone on the internet, only those on the
  internal network, only the person at that machine?
- **Is authentication needed?** If it can be used without logging in,
  everyone in the world can try it.

Let us give a toy score with these two questions: internet 3, internal
network 2, local only 1; double the score if there is no authentication.
Real measurement methods are more detailed, but the idea is the same.

```python
WEIGHT = {"internet": 3, "internal": 2, "local": 1}
entry_points = [
    ("login page", "internet", True),
    ("search api", "internet", False),
    ("admin panel", "internet", True),
    ("report export", "internal", True),
    ("debug console", "local", False),
]
total = 0
for name, exposure, needs_auth in entry_points:
    score = WEIGHT[exposure] * (1 if needs_auth else 2)
    total += score
    print(f"{name:<14} {exposure:<9} auth={needs_auth!s:<5} score={score}")
print("total:", total)
```

```text
login page     internet  auth=True  score=3
search api     internet  auth=False score=6
admin panel    internet  auth=True  score=3
report export  internal  auth=True  score=2
debug console  local     auth=False score=2
total: 16
```

This table shows two things at once: the search API, which needs no login,
is the most open door, and the admin panel can be reached from the
internet. If there is no reason for the admin panel to be open to everyone,
it is the first place that can be closed.

## Shrinking the surface

The ways to shrink the attack surface are usually simple:

- **Remove what is not used:** old pages, features tried and abandoned,
  endpoints nobody calls, packages installed but not used.
- **Narrow who can reach it:** the admin panel only from the internal
  network or a VPN; the database never open to the internet.
- **Make off the default:** a feature is turned on when it is needed and
  stays off otherwise ("secure by default" from Security Principles).
- **Take debugging tools out of the live system:** consoles that are useful
  during development are a door in the live system.

In the example system, let us move the admin panel to the internal network
and remove the debug console:

```python
after = [("login page", "internet", True), ("search api", "internet", False),
         ("admin panel", "internal", True), ("report export", "internal", True)]
after_total = sum(WEIGHT[e] * (1 if a else 2) for _, e, a in after)
print("before:", total, "after:", after_total)
print(f"reduced by {(total - after_total) / total:.0%}")
```

```text
before: 16 after: 13
reduced by 19%
```

Two small changes cut the surface's score by 19%. The real gain is
not in the score: there is no longer an admin panel reachable from the
internet.

## Finding what is unused

The logs tell which endpoints are really used. An endpoint that has not
received a single request in the last three months has most likely been
forgotten and is a candidate for removal:

```python
hits = {"/login": 5120, "/search": 830, "/grades": 2210,
        "/admin": 4, "/legacy-upload": 0}
print([path for path, count in hits.items() if count == 0])
```

```text
['/legacy-upload']
```

Forgotten endpoints are doubly dangerous: nobody updates them and nobody
watches whether they are being attacked. An old file upload page can be
the way around every check on the new page.

## The surface changes with every release

Every new feature can be a new entry point. That is why it is a good habit
to look at **how the surface changed** before publishing a release: every
newly added endpoint is handled separately in code review and in the
threat model.

```python
v1 = {"/login", "/search", "/grades", "/admin"}
v2 = {"/login", "/search", "/grades", "/admin", "/export", "/debug"}
print("new:", sorted(v2 - v1))
print("removed:", sorted(v1 - v2))
```

```text
new: ['/debug', '/export']
removed: []
```

The new release has two endpoints more. `/export` may be a deliberately
added feature; `/debug` is most likely going to production by mistake.
This difference list is the answer to "what should we review in this
release?".

## A small surface is not a hidden surface

Shrinking the attack surface means **removing** or **locking** doors.
Hiding a door (putting the admin panel at an address that is hard to
guess) does not shrink the surface; it is only security through obscurity
(Security Principles). One day the address leaks, and the door is still
there.

## Summary

- The **attack surface** is the sum of all the **entry points** where an
  attacker can reach the system: digital, physical and human.
- The first step is an **inventory**: an unknown door cannot be locked;
  shadow IT is missed most often.
- How exposed an entry point is depends on **who can reach it** and
  **whether authentication is needed**.
- To shrink it, remove what is unused, narrow who can reach it, make off
  the default.
- Look at how the surface changed in every release; hiding is not
  shrinking.
