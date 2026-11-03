# Network Attacks

In the Network Layers section we saw the road a packet travels: each layer
adds a header, and someone watching the road can read the headers. This
section explains the attacks made on that road **as concepts** and **why
they work**; the aim is to recognise each one and build its defence. The
examples are again toy data structures in Python: no packet is sent
anywhere, no real network is listened to. Example outside addresses come
from the `203.0.113.0/24` and `198.51.100.0/24` ranges reserved for
documentation.

One idea carries the whole section: most network protocols were designed in
years when the internet was a small, trusting community. **Many of them do
not verify who the other side is.** Most attacks take advantage of that
trust.

## Eavesdropping

On its way to the destination a packet passes through many devices: the
Wi-Fi access point in a café, the home router, the internet provider's
equipment. Someone with access to one of them can read unencrypted traffic
as it is. This is called **eavesdropping** (sniffing).

```python
packets = [
    {"dport": 80, "data": "POST /login user=ada&password=s3cret"},
    {"dport": 443, "data": "<TLS: unreadable bytes>"},
]
for p in packets:
    print(p["dport"], "->", p["data"])
```

```text
80 -> POST /login user=ada&password=s3cret
443 -> <TLS: unreadable bytes>
```

A password sent over plain HTTP (port 80) is right there in front of
everyone watching the road. Content sent over HTTPS (port 443) is
encrypted: the listener sees only meaningless bytes. **The defence is
encryption** (the TLS Handshake section of the Cryptography module). Note:
encryption hides the content, not the headers. The listener still sees who
exchanges data with which server, when, and how much.

## Man in the middle (MitM)

One step beyond eavesdropping, the attacker **gets between** the two sides.
Both think they are talking to each other, but every message passes
through the attacker, who can read it, change it or stop it. This is a
**man-in-the-middle** (MitM) attack.

<figure class="fig"><div class="flow">
  <span class="node">Client</span><span class="arrow">→</span>
  <span class="node acc">Attacker</span><span class="arrow">→</span>
  <span class="node">Server</span>
</div><figcaption>Both sides think they are talking to the other. Without authentication they cannot notice.</figcaption></figure>

Encryption alone is not enough against MitM; you need to **verify who the
other side is**. If you set up an encrypted connection with the attacker,
confidentiality is of no use. That is why TLS has certificate checks (the
Certificates and PKI section of the Cryptography module): the browser's
"this connection is not secure" warning means exactly "I could not verify
that the other end is that site". You do not click past that warning.

## ARP spoofing: getting in the middle on the local network

On the local network a packet travels to the next device **by MAC
address**. A device asks the network "what is the MAC of `192.168.1.1`?"
and the owner answers. This protocol is called **ARP**, and it **never
checks** whether the answer really comes from the owner of the address:
the last answer to arrive is written into the table.

```python
arp_table = {}
replies = [("192.168.1.1", "02:00:00:00:00:fe"),
           ("192.168.1.20", "02:00:00:00:00:14"),
           ("192.168.1.1", "02:00:00:00:00:66")]

for ip, mac in replies:
    old = arp_table.get(ip)
    if old and old != mac:
        print(f"WARNING {ip}: {old} -> {mac}")
    arp_table[ip] = mac
print(arp_table["192.168.1.1"])
```

```text
WARNING 192.168.1.1: 02:00:00:00:00:fe -> 02:00:00:00:00:66
02:00:00:00:00:66
```

When someone on the same network sent a fake answer saying "`192.168.1.1`
(the router) is me", the table changed silently; from now on every packet
going to the internet goes to them first. This is **ARP spoofing**, and it
is the best-known way to get in the middle on a local network. That is why
sending anything unencrypted on shared Wi-Fi is risky.

Defences:

- **Encryption:** even with someone in the middle, TLS protects the
  content, and the certificate check catches a fake server.
- **Checks in the network device:** company switches can know which IP–MAC
  pairing is valid on which port and drop fake ARP answers.
- **Detection:** a warning like the one above, "an address's MAC suddenly
  changed". A router's MAC normally never changes.

## Forged source addresses (IP spoofing)

The sender writes the **source address** in the IP header themselves, and
nobody on the way checks it. An attacker can write someone else's address.
This is used for two things:

- **Hiding identity:** the packet reaches the target without showing where
  it came from (but since the reply goes to the forged address, the
  attacker cannot see the reply).
- **Reflection:** the attacker writes the victim's address as the source
  and sends a small question to many servers; all the answers rain down on
  the victim. If the answer is bigger than the question this is called
  **amplification**: if a 60-byte question produces a 3000-byte answer,
  every byte of the attacker's comes back to the victim as 50 bytes.

The basis of the defence is **ingress filtering**: if a packet coming from
outside carries an address from your own internal network or loopback as
its source, the packet is forged and is dropped. A packet leaving from
inside must also have an internal source; not letting the others out stops
your network from being used to attack others.

```python
import ipaddress

INTERNAL = ipaddress.ip_network("192.168.1.0/24")


def ingress_ok(src):
    ip = ipaddress.ip_address(src)
    return not (ip in INTERNAL or ip.is_loopback)


for src in ["203.0.113.7", "192.168.1.20", "127.0.0.1"]:
    print(src, "accept" if ingress_ok(src) else "drop")
```

```text
203.0.113.7 accept
192.168.1.20 drop
127.0.0.1 drop
```

This rule does not catch forgery that writes an outside address (nobody
can catch that alone), but it catches an outside packet claiming "I am
inside". It also answers why address-based trust should not be relied on:
**an IP address is not proof of identity.**

## Denial of service (DoS and DDoS)

Not every attack steals data; some only make a service **unusable**. They
aim at the availability leg of the CIA triad. Coming from a single source
this is **DoS** (denial of service); coming from thousands of devices at
once it is **DDoS** (distributed). Often those devices are a **botnet** of
computers and cameras taken over without their owners knowing.

One of the best-known examples is the **SYN flood**. Remember the handshake
from the Network Layers section: when the server receives a SYN it sends a
SYN-ACK and reserves room for the half-finished connection. If the attacker
(often with forged source addresses) sends many SYNs and never sends the
ACK, that room fills up:

```python
BACKLOG = 5
half_open = []


def on_syn(src):
    if len(half_open) >= BACKLOG:
        return "refused"
    half_open.append(src)
    return "syn-ack"


for i in range(5):
    on_syn(f"198.51.100.{i}")
print(len(half_open), "half-open")
print("real client:", on_syn("192.168.1.10"))
```

```text
5 half-open
real client: refused
```

Five fake requests filled the table; the real customer was turned away.
Real servers have a much bigger table, but the attacker also sends many
more requests.

Defences:

- **SYN cookies:** the server reserves no room until the ACK arrives; it
  embeds the information it needs cryptographically in the SYN-ACK's
  sequence number and reads it back when the ACK comes. The table does not
  fill.
- **Timeouts:** not keeping half-open connections for long.
- **Rate limiting:** limiting how many requests a source can make in a
  given time (below).
- **Capacity and upstream filtering:** in a DDoS a single server's link can
  fill whatever it does; large networks that filter traffic in advance and
  distributed servers are used.

## Rate limiting

Rate limiting is a common defence against DoS, password-guessing attacks
and abuse. The **sliding window** method counts the requests in the last
`window` seconds; once `limit` is reached, it refuses new ones:

```python
from collections import deque


def make_limiter(limit, window):
    times = deque()

    def allow(now):
        while times and now - times[0] >= window:
            times.popleft()
        if len(times) >= limit:
            return False
        times.append(now)
        return True

    return allow


allow = make_limiter(3, 10)
print([allow(t) for t in [0, 1, 2, 3, 9, 10, 11, 12]])
```

```text
[True, True, True, False, False, True, True, True]
```

The first three requests passed; the fourth and fifth (seconds 3 and 9)
were refused. At second 10 the first request left the window, so room
opened up. Real systems keep the limit **separately for each source**;
otherwise one attacker uses up everyone's allowance. In a DDoS there are
so many sources that a per-source limit is not enough on its own.

## Port scanning and reconnaissance

Attacks often start with a **reconnaissance** phase: learning which ports
are open on the target and which services run there. Trying to connect to
many ports one after another for this is called **port scanning**. It does
no harm on its own but it is the herald of an attack; doing it without the
owner's permission is against the rules of most organisations and the law
of many countries (the Ethics and Law section).

There are two lessons for the defending side. First: if unused ports are
closed, a scan finds nothing. Second: scanning **leaves traces** in the
logs; a source that touches many different ports in a short time stands
out:

```python
from collections import defaultdict

log = [("198.51.100.9", port) for port in range(20, 32)] + [
    ("192.168.1.10", 443), ("192.168.1.10", 443), ("192.168.1.11", 22)]

ports_by_src = defaultdict(set)
for src, port in log:
    ports_by_src[src].add(port)
for src, ports in sorted(ports_by_src.items()):
    flag = "SUSPECT" if len(ports) >= 10 else "ok"
    print(f"{src:<14} {len(ports):>2} ports  {flag}")
```

```text
192.168.1.10    1 ports  ok
192.168.1.11    1 ports  ok
198.51.100.9   12 ports  SUSPECT
```

Intrusion detection systems (the Intrusion Detection section of the System
Security module) do a much more advanced version of this.

## Replay

Even if the attacker cannot read the content, they can **send a captured
valid message again as it is**: a "send 100" request is processed twice.
Encryption and HMAC do not prevent this on their own, because the message
really is valid. The defence is to put a **value used only once** (a nonce)
or a timestamp in the message and have the server reject what it has
already seen. That is why the API signature in the HMAC section had a
timestamp.

## A map of attacks and defences

<figure class="fig anat">
  <div class="anat-row"><span>Eavesdropping</span><span>Encryption (TLS). Headers are still visible.</span></div>
  <div class="anat-row"><span>Man in the middle</span><span>Encryption + verifying the other side (certificate).</span></div>
  <div class="anat-row"><span>ARP spoofing</span><span>Checks in the switch, detection, and TLS in every case.</span></div>
  <div class="anat-row"><span>Forged source address</span><span>Ingress and egress filtering; not treating an IP address as identity.</span></div>
  <div class="anat-row"><span>SYN flood, DoS</span><span>SYN cookies, timeouts, rate limiting, upstream filtering.</span></div>
  <div class="anat-row"><span>Port scanning</span><span>Closing unused ports, detection from logs.</span></div>
  <div class="anat-row"><span>Replay</span><span>A nonce or timestamp, rejecting what has been seen.</span></div>
  <figcaption>Each row is a separate layer. No single defence closes the whole list.</figcaption>
</figure>

## Summary

- Most network protocols **do not verify the other side**; attacks exploit
  that trust.
- **Eavesdropping** reads unencrypted content; encryption hides the
  content, not the headers.
- Against a **man in the middle** you need encryption + authentication;
  you do not click past a certificate warning.
- **ARP** answers are not checked; that is how one gets in the middle on a
  local network.
- A **source IP address** can be forged; ingress filtering drops an outside
  packet claiming "I am inside". An IP address is not proof of identity.
- A **SYN flood** fills the half-open connection table; SYN cookies,
  timeouts and **rate limiting** are the defence.
- **Port scanning** is reconnaissance; a closed port cannot be found, and a
  scan leaves traces in the log.
- Against **replay**, a nonce or a timestamp.
