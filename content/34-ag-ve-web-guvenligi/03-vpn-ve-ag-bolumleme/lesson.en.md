# VPNs and Network Segmentation

The Firewalls section left two questions open: how does someone working
from home or a café reach the company's internal network **safely**, and if
a computer inside is compromised, how do we stop the attacker **spreading
everywhere**? The answer to the first is a VPN, to the second network
segmentation. At the end of the section we look at an idea that goes
beyond both: being inside the network is not a reason for trust. The
examples are again toy data structures in Python.

## VPN: an encrypted tunnel

A **VPN** (virtual private network) builds an **encrypted tunnel** between
two points over the internet. Packets travelling through the tunnel flow as
if both sides were on the same private network. The encapsulation from the
Network Layers section goes one level deeper here: the **real packet** (the
inner packet) is encrypted as a whole and put inside **another packet**
(the outer packet).

<figure class="fig"><div class="flow">
  <span class="node">Inner packet</span><span class="arrow">→</span>
  <span class="node">Encrypt</span><span class="arrow">→</span>
  <span class="node">Outer packet</span><span class="arrow">→</span>
  <span class="node acc">VPN gateway</span>
</div><figcaption>The outer packet goes only to the VPN gateway; the gateway opens it and drops the inner packet onto the internal network.</figcaption></figure>

Someone watching the road sees only the outer packet:

```python
import json

inner = {"src": "10.8.0.2", "dst": "10.20.0.15", "dport": 80,
         "data": "GET /payroll"}
payload = json.dumps(inner)
outer = {"src": "203.0.113.50", "dst": "198.51.100.1", "dport": 443,
         "payload": f"<encrypted {len(payload)} bytes>"}

print("inner:", inner["src"], "->", inner["dst"], inner["dport"])
print("outer:", outer["src"], "->", outer["dst"], outer["dport"])
print("observer sees:", outer["payload"])
```

```text
inner: 10.8.0.2 -> 10.20.0.15 80
outer: 203.0.113.50 -> 198.51.100.1 443
observer sees: <encrypted 77 bytes>
```

The inner packet holds the company's internal addresses (`10.20.0.15`) and
the page requested; someone looking from outside cannot see them. All they
see is encrypted traffic of a certain size going from the employee's
address in the café (`203.0.113.50`) to the company's VPN gateway
(`198.51.100.1`). The internal network is entered only through the gateway
too; so the company's internal servers are never opened to the internet,
only the gateway is.

There are two ways to use it:

- **Remote access:** an employee's computer connects to the company
  network. A VPN client runs on the computer.
- **Site-to-site:** the networks of two branches are connected; the
  computers do not even know, two routers build the tunnel.

## What does a VPN protect, and what not?

A VPN is a very often misunderstood tool. What it protects is **one part of
the road**: the road between your computer and the VPN gateway.

<figure class="fig"><div class="versus">
  <div class="ok"><h4>Protects</h4>Someone listening to the café Wi-Fi or getting in the middle with ARP spoofing cannot read your traffic. The internal network's servers can be used remotely without being opened to the internet.</div>
  <div class="no"><h4>Does not protect</h4>Malware on your computer, a password you typed into a phishing page, the road after the VPN gateway, or the website's own holes. A VPN is not anonymity either: the VPN provider sees your traffic.</div>
</div><figcaption>A VPN is a tunnel; it does not solve the problems at its two ends.</figcaption></figure>

One more trap: a computer connected to the VPN becomes **part of the
internal network**. If that computer is compromised, the attacker comes in
through the tunnel too. That is why who may connect to the VPN with which
device is checked strictly (multi-factor authentication, the Authentication
and MFA section) and not everyone coming over the VPN gets the whole
internal network. This brings us to segmentation.

In a setting called **split tunneling**, only traffic to the company
network goes through the tunnel; the rest goes straight out to the
internet. It eases the load on the company's connection, but that traffic
skips the company's security checks; the choice is made deliberately.

## The problem with a flat network

Many small networks are **flat**: all devices are on the same network and
can reach each other freely. When an attacker gets into the network through
one weak point (a laptop where a phishing e-mail was opened, a camera that
was never updated), they move on from there to the other devices. This is
called **lateral movement**. On a flat network nothing stands in the way of
lateral movement:

```python
from collections import deque


def reachable(links, start):
    seen = {start}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for nxt in links.get(node, []):
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    return sorted(seen - {start})


hosts = ["laptop", "printer", "camera", "hr-db", "web", "backup"]
flat = {h: [o for o in hosts if o != h] for h in hosts}
segmented = {"laptop": ["web"], "web": ["hr-db"], "backup": ["hr-db"]}

print("flat:     ", reachable(flat, "laptop"))
print("segmented:", reachable(segmented, "laptop"))
```

```text
flat:      ['backup', 'camera', 'hr-db', 'printer', 'web']
segmented: ['hr-db', 'web']
```

On the flat network, all five other devices can be reached from the
compromised laptop. On the segmented network only the web server, and
through it the human resources database. The printer, the camera and the
backup server can no longer be reached.

The second line of the result also teaches something: there is still **a
path** to the database, through the web server. Segmentation does not stop
the attacker; it **makes the path longer and narrower**, and that narrow
path (the web server) is especially well protected and watched. The backup
server having no path from the laptop matters too: as we will see in the
Backup and Disaster Recovery section, the attacker not reaching the backups
is the condition for being able to recover after an attack.

## Zones and the DMZ

The usual way to segment is to split the network into **zones** and put a
firewall between the zones. Each zone is a subnet (the subnet arithmetic
of the Network Layers section):

<figure class="fig anat">
  <div class="anat-row"><span><b>DMZ</b></span><span>Servers that serve the internet (web, e-mail). Reachable from outside, with narrow access inwards.</span></div>
  <div class="anat-row"><span><b>Servers</b></span><span>Databases, internal applications. Never reachable from the internet.</span></div>
  <div class="anat-row"><span><b>Staff</b></span><span>Laptops and desktops. They reach the few services they need.</span></div>
  <div class="anat-row"><span><b>Guest</b></span><span>The visitors' Wi-Fi. Goes out to the internet only, never reaches the internal network.</span></div>
  <div class="anat-row"><span><b>Management</b></span><span>The management interfaces of network devices and servers. Administrators only.</span></div>
  <figcaption>The zones of a typical company network. Real networks also have other zones, such as IoT devices and production systems.</figcaption>
</figure>

The **DMZ** (demilitarized zone) takes its name from the buffer zone
between two countries: it is an area between the internet and the internal
network, separated from both. Even if the web server is compromised, the
attacker stays in the DMZ; from there only narrow, defined paths into the
internal network are open (such as a single port from the web server to the
database).

Finding which zone an address is in is a subnet check:

```python
import ipaddress

ZONES = [("dmz", "10.10.0.0/24"), ("servers", "10.20.0.0/24"),
         ("staff", "10.30.0.0/24"), ("guest", "10.99.0.0/24")]


def zone_of(text):
    ip = ipaddress.ip_address(text)
    for name, cidr in ZONES:
        if ip in ipaddress.ip_network(cidr):
            return name
    return "internet"


for text in ["10.10.0.5", "10.20.0.15", "10.99.0.42", "203.0.113.7"]:
    print(text, zone_of(text))
```

```text
10.10.0.5 dmz
10.20.0.15 servers
10.99.0.42 guest
203.0.113.7 internet
```

The rules between zones are an allow list too, as in the Firewalls
section; a flow not in the list is refused:

```python
POLICY = {("internet", "dmz", 443), ("dmz", "servers", 5432),
          ("staff", "dmz", 443), ("staff", "servers", 443)}


def allowed(src_zone, dst_zone, port):
    return (src_zone, dst_zone, port) in POLICY


for flow in [("internet", "dmz", 443), ("internet", "servers", 5432),
             ("guest", "staff", 445), ("dmz", "servers", 5432)]:
    print(*flow, "allow" if allowed(*flow) else "deny")
```

```text
internet dmz 443 allow
internet servers 5432 deny
guest staff 445 deny
dmz servers 5432 allow
```

There is no direct access from the internet to the database; there is no
file sharing (445) from the guest network to the staff computers. The web
server has a single port to the database. Zones do not have to be built
with separate cables: a **VLAN** (virtual local area network) builds
separate networks on the same switch and cables. Shrinking zones down to
individual servers and applications is called **microsegmentation**.

## Zero trust

The classic model is the **perimeter** model: if the outer wall is solid,
the inside is trusted. This model clashes with two facts: attackers may
already be inside (a compromised laptop), and staff are no longer always
inside (working from home, from a phone, from the cloud). The **zero
trust** model says: **location on the network is not a reason for trust.**
Every request is judged **every time** by who is asking, from which device,
and what they want to reach.

```python
def perimeter(request):
    return request["inside"]


def zero_trust(request):
    return (request["mfa"] and request["device_ok"]
            and request["resource"] in request["grants"])


attempts = [
    {"who": "infected laptop", "inside": True, "mfa": False,
     "device_ok": False, "resource": "hr-db", "grants": []},
    {"who": "remote engineer", "inside": False, "mfa": True,
     "device_ok": True, "resource": "wiki", "grants": ["wiki"]},
]
for r in attempts:
    print(f"{r['who']:<16} perimeter={perimeter(r)!s:<5} zero_trust={zero_trust(r)}")
```

```text
infected laptop  perimeter=True  zero_trust=False
remote engineer  perimeter=False zero_trust=True
```

The perimeter model trusted the infected laptop inside and refused the
authorised engineer outside; zero trust decided correctly in both cases.
Zero trust is not a product but a design principle: the **complete
mediation** (check every access, every time) and **least privilege**
principles from the Security Principles section applied to the network.
Segmentation does not go away; zero trust comes on top of it.

## Summary

- A **VPN** builds an encrypted tunnel between two points; the inner packet
  is encrypted and put in an outer packet. Used for remote access and
  site-to-site.
- A VPN protects **one part of the road** (between you and the gateway); it
  does not protect against malware, phishing or the site's holes, and it is
  not anonymity.
- A device connected to the VPN becomes part of the internal network; the
  connecting device and person are checked strictly.
- On a **flat network**, **lateral movement** goes everywhere from a single
  compromised device; **segmentation** makes the path longer and narrower.
- The network is split into **zones** (DMZ, servers, staff, guest,
  management) with an allow list between zones.
- The **DMZ** separates the servers that serve the internet from the
  internal network.
- **Zero trust:** location on the network is not a reason for trust; every
  request is judged every time by identity, device and permission.
