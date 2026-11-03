# Firewalls

One tool kept appearing in the defence list of the Network Attacks section:
a filter that lets packets through or stops them according to a rule. This
is a **firewall**. This section explains how a firewall decides, how rules
are written and the most common mistakes. We will again try the rules with
a small evaluator in Python; we do not touch a real firewall.

## What does a firewall do?

A firewall sits between two networks (or between a computer and a network)
and decides for every packet **whether it may pass or not**. It decides by
looking at the headers: the protocol (TCP/UDP), the source and destination
addresses, the destination port. In the language of the Network Layers
section, an ordinary firewall works at the **internet and transport
layers** (OSI 3–4).

It is found in two places:

- **Network firewall:** at the internet connection of a company or home,
  in front of the whole network. Home routers have a simple one inside too.
- **Host firewall:** runs on each computer itself; it also looks at
  traffic coming from inside the network. Both together are defence in
  depth.

## Rules, order and the default

A firewall keeps a **rule list**. Each rule says "do this to packets with
these properties". When a packet arrives the rules are tried **from top to
bottom** and the **first rule that matches** decides. If none matches, the
**default** decision applies. The "deny by default" rule from the Security
Principles section is applied directly here: everything not allowed is
forbidden.

```python
import ipaddress

RULES = [
    {"action": "allow", "proto": "tcp", "port": 443, "src": "0.0.0.0/0"},
    {"action": "allow", "proto": "tcp", "port": 22, "src": "192.168.1.0/24"},
]


def matches(rule, packet):
    return (rule["proto"] in ("any", packet["proto"])
            and rule["port"] in ("any", packet["port"])
            and ipaddress.ip_address(packet["src"]) in ipaddress.ip_network(rule["src"]))


def decide(packet):
    for number, rule in enumerate(RULES, 1):
        if matches(rule, packet):
            return f"{rule['action']} (rule {number})"
    return "deny (default)"


for packet in [{"proto": "tcp", "port": 443, "src": "203.0.113.7"},
               {"proto": "tcp", "port": 22, "src": "192.168.1.20"},
               {"proto": "tcp", "port": 22, "src": "203.0.113.7"},
               {"proto": "udp", "port": 53, "src": "203.0.113.7"}]:
    print(packet["port"], packet["src"], "->", decide(packet))
```

```text
443 203.0.113.7 -> allow (rule 1)
22 192.168.1.20 -> allow (rule 2)
22 203.0.113.7 -> deny (default)
53 203.0.113.7 -> deny (default)
```

The rules say: anyone may reach the web server (443) (`0.0.0.0/0` means
"all addresses"); SSH (22) may be reached only from the internal network.
The SSH attempt from outside matched no rule and was refused by the
default. The same happened to UDP 53, because no rule was written for it.
**What you do not write, you have not allowed**; everything that must be
open is opened deliberately, one by one.

Printing the decision together with the rule number is not pointless: real
firewalls also log which rule handled which packet. The answer to "why did
this packet pass" or "why was it stopped" is there.

## Order matters: shadowed rules

Because the first matching rule wins, **order** matters as much as the rule
itself. If a broad rule sits above a narrower one, the narrow one never
runs. This is called a **shadowed rule**:

```python
def first_action(rules, port):
    for rule_port, action in rules:
        if rule_port in ("any", port):
            return action
    return "deny"


intended = [(23, "deny"), (80, "allow"), (443, "allow")]
broken = [("any", "allow"), (23, "deny")]
print("intended:", first_action(intended, 23), first_action(intended, 8080))
print("broken:  ", first_action(broken, 23), first_action(broken, 8080))
```

```text
intended: deny deny
broken:   allow allow
```

In the second list, someone hunting a problem added an "allow everything
for now" rule at the top and forgot it. The "close 23 (an old, unencrypted
remote login)" rule below it is still in the list, and whoever reads it
thinks they are safe, but no packet ever reaches it. On top of that, deny
by default stopped working: 8080 opened too. This mistake is very easy to
make as a rule list grows; that is why rules are reviewed regularly and
**rules that never match** are cleaned out.

## Stateless and stateful

Here is the problem: when your computer connects to a web server outside,
the server's **reply** must also get in. The reply comes to a large port
you chose at random (like `51514`). A **stateless** filter that judges
every packet on its own cannot know this; to let replies through it has to
open all the high ports to the outside. That is a huge hole.

A **stateful** firewall remembers connections. When a connection starts
from inside to outside, it writes it into a table; it lets a packet from
outside through only if it is the **reverse** of a connection in the table:

```python
outgoing = set()


def send(src, sport, dst, dport):
    outgoing.add((src, sport, dst, dport))


def reply_ok(src, sport, dst, dport):
    return (dst, dport, src, sport) in outgoing


send("192.168.1.10", 51514, "203.0.113.7", 443)
print(reply_ok("203.0.113.7", 443, "192.168.1.10", 51514))
print(reply_ok("203.0.113.7", 443, "192.168.1.10", 51999))
print(reply_ok("198.51.100.9", 443, "192.168.1.10", 51514))
```

```text
True
False
False
```

Only the reply to a connection that was really started got through. A
packet from the same server to another port and one from another address
were stopped. Almost all of today's firewalls are stateful.

<figure class="fig"><div class="versus">
  <div><h4>Stateless</h4>Judges every packet on its own, looking only at its own headers. Fast and simple; but letting replies through means opening wide ranges.</div>
  <div><h4>Stateful</h4>Tracks connections in a table; lets a packet from outside through only if it replies to a connection started from inside. A connection started from outside stops by itself.</div>
</div><figcaption>A stateful firewall can ask "who started this".</figcaption></figure>

## Filter the way out too

Rules are often written only for traffic coming **in**. Yet when a computer
inside is infected with malware, it tries to connect to a server outside to
receive commands or send data. **Egress filtering** makes this harder: from
inside to outside only the needed ports are allowed, the rest are stopped
and **logged**:

```python
ALLOWED_OUT = {53, 80, 443}
attempts = [("192.168.1.10", 443), ("192.168.1.10", 8888),
            ("192.168.1.30", 53), ("192.168.1.30", 2525)]

for host, port in attempts:
    print(host, port, "allow" if port in ALLOWED_OUT else "block + log")
```

```text
192.168.1.10 443 allow
192.168.1.10 8888 block + log
192.168.1.30 53 allow
192.168.1.30 2525 block + log
```

A blocked attempt proves nothing on its own, but the question "why is this
computer trying to go out to `8888`?" can be the first clue of an incident.
This was the egress filtering rule from the Network Attacks section too:
stopping your own network from being used to attack others.

## At the application layer: WAF

An ordinary firewall looks at headers, not content. If you allowed port
443, every HTTP request on that port gets through, even one with SQL
injection inside. A **web application firewall** (WAF) works at the
application layer (OSI 7): it inspects the HTTP request's path, parameters
and headers and stops the ones that look like known attack patterns.

A WAF is a useful **extra layer**, but because it is a list of patterns it
can be bypassed; it does not close the hole in the application. As we will
see in the SQL Injection and XSS sections, the real defence is in the
application's own code (parameterised queries, output encoding). A WAF
does not replace it.

## What can a firewall not do?

- **It cannot see what is inside traffic you allowed.** An attack on 443
  gets through if 443 is open.
- **It cannot read encrypted content** (unless it was set up separately to
  decrypt it).
- **An attack that starts inside** (a compromised computer within the
  network) is not seen by the network firewall; that needs network
  segmentation and host firewalls (the VPNs and Network Segmentation
  section).
- **It does not replace authentication:** an address-based rule can be
  fooled with a forged address, as we saw in the Network Attacks section.

## Summary

- A firewall decides **pass or stop** for every packet; an ordinary one
  looks at the headers (address, port, protocol).
- Rules are tried **from top to bottom**, the **first match** wins; if none
  matches, **deny by default**.
- If a broad rule sits above a narrow one, the narrow one is **shadowed**;
  rules are reviewed regularly.
- A **stateful** firewall remembers connections and lets through only
  replies to connections started from inside.
- **Egress filtering** makes it harder for a compromised computer to
  connect out; blocked attempts are logged.
- A **WAF** is an extra layer that looks at HTTP content; it does not close
  the hole in the application.
- A firewall cannot inspect the inside of allowed traffic, an attack that
  starts inside, or identity.
