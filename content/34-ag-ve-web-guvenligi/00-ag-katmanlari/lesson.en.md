# Network Layers and Addresses

This module explains how a web page reaches your computer and what can go
wrong at each step on the way. To understand attacks, you first need to
know the road itself: which pieces a message is split into, what is
written on top of each piece, how the receiver is found. In this section we
connect to no network at all; we imitate addresses and packets with small
data structures in Python.

## Why layers?

Think of sending a letter. You write the letter; you write the address on
the envelope for the post office; the post office puts the envelope in a
bag, and the bag travels on a lorry. The person who wrote the letter does
not know the lorry's route, and the lorry driver does not know what the
letter says. Everyone does only their own job.

Networks work the same way. The work is split into **layers**; each layer
uses the service of the one below and serves the one above. The model used
on the internet today is the **TCP/IP** model, and it has four layers:

<figure class="fig anat">
  <div class="anat-row"><span><b>Application</b></span><span>The language programs speak: HTTP for the web, DNS for domain names, SSH for remote login.</span></div>
  <div class="anat-row"><span><b>Transport</b></span><span>Takes data to the right program: TCP (reliable, in order) or UDP (fast, no guarantees). Port numbers live here.</span></div>
  <div class="anat-row"><span><b>Internet</b></span><span>Takes data to the right computer: IP addresses and routing live here.</span></div>
  <div class="anat-row"><span><b>Link</b></span><span>Takes data to the next device on the same local network: Ethernet, Wi-Fi, MAC addresses.</span></div>
  <figcaption>The four layers of the TCP/IP model, from top to bottom.</figcaption>
</figure>

Textbooks also mention the seven-layer **OSI model**. It is the same idea
split more finely: the TCP/IP application layer becomes three in OSI
(application, presentation, session) and the link layer becomes two (data
link, physical). Phrases in security writing such as "a layer 3 attack" or
"a layer 7 firewall" use OSI numbers: **3 is network (IP), 4 is transport
(TCP/UDP), 7 is application (HTTP).**

## Encapsulation: an envelope inside an envelope

As a web request sets off, each layer adds its own **header** to it. The
transport layer writes the port numbers, the internet layer the IP
addresses, the link layer the MAC addresses. This is called
**encapsulation**. On the receiving side each layer reads and strips its
own header and passes the inside up.

<figure class="fig"><div class="flow">
  <span class="node">Data</span><span class="arrow">→</span>
  <span class="node">Segment</span><span class="arrow">→</span>
  <span class="node">Packet</span><span class="arrow">→</span>
  <span class="node acc">Frame</span>
</div><figcaption>Each layer wraps the previous one in its own header: a TCP segment, an IP packet, an Ethernet frame.</figcaption></figure>

Let us imitate this with nested dictionaries:

```python
data = "GET /index.html"
segment = {"sport": 51514, "dport": 80, "data": data}
packet = {"src": "192.168.1.10", "dst": "203.0.113.7", "segment": segment}
frame = {"src_mac": "02:00:00:00:00:01", "dst_mac": "02:00:00:00:00:fe",
         "packet": packet}

for name, header in [("frame", frame), ("packet", packet), ("segment", segment)]:
    fields = [k for k, v in header.items() if not isinstance(v, dict)]
    print(f"{name:<8} {fields}")
print("data    ", repr(segment["data"]))
```

```text
frame    ['src_mac', 'dst_mac']
packet   ['src', 'dst']
segment  ['sport', 'dport', 'data']
data     'GET /index.html'
```

There is an important consequence for security: **someone watching the
road can read every header.** Who talks to whom, on which port, is plain
from the headers. If the content (`data`) is not encrypted, it can be read
too. The eavesdropping attack in the next section relies on exactly this.

## IP addresses

At the internet layer every device has an **IP address**. The most widely
used version today is **IPv4**: an address is a 32-bit number, written as
four bytes separated by dots so that it is easy to read (`192.168.1.10`).
Each byte is between 0 and 255. The `ipaddress` module in Python's standard
library makes working with addresses easy:

```python
import ipaddress

ip = ipaddress.ip_address("192.168.1.10")
print(ip.version)
print(list(ip.packed))
print(int(ip))

value = 0
for part in [192, 168, 1, 10]:
    value = value * 256 + part
print(value)
```

```text
4
[192, 168, 1, 10]
3232235786
3232235786
```

An address is really a single number; the dotted form is only for reading.
Each byte is added to the number after multiplying the previous value by
256, which is why the hand calculation gave the same result as `int(ip)`.
IPv4 has about 4.3 billion addresses and that is not enough; longer
(128-bit) **IPv6** addresses (`2001:db8::1`) came for this reason. The ideas
are the same, and we use IPv4 in the examples.

## Networks and subnets: CIDR

Addresses are handed out not one by one but as **networks**. The notation
`192.168.1.0/24` (CIDR) says: the first 24 bits identify the network, the
remaining 8 bits identify the device on that network. Addresses whose
network part is the same are on the same local network.

```python
import ipaddress

net = ipaddress.ip_network("192.168.1.0/24")
print(net.netmask)
print(net.num_addresses)
print(net.network_address, net.broadcast_address)
print(ipaddress.ip_address("192.168.1.77") in net)
print(ipaddress.ip_address("192.168.2.5") in net)
```

```text
255.255.255.0
256
192.168.1.0 192.168.1.255
True
False
```

A `/24` network has 256 addresses. The first (`.0`) stands for the network
itself and the last (`.255`) is the **broadcast** address; the remaining
254 addresses are given to devices. The **netmask** `255.255.255.0` is an
older way of writing the same information: the bits that are 1 are the
network part. The larger the prefix, the smaller the network:

```python
import ipaddress

for prefix in [8, 16, 24, 28, 32]:
    net = ipaddress.ip_network(f"10.0.0.0/{prefix}")
    print(f"/{prefix:<3}{net.num_addresses:>10}  {net.netmask}")
```

```text
/8    16777216  255.0.0.0
/16      65536  255.255.0.0
/24        256  255.255.255.0
/28         16  255.255.255.240
/32          1  255.255.255.255
```

Each extra prefix bit halves the number of addresses. `/32` is a single
device; it is often used in firewall rules to say "only this computer".

## Private, public and loopback addresses

Some address ranges are not routed on the internet and are used only inside
home and company networks. These are **private** addresses: `10.0.0.0/8`,
`172.16.0.0/12` and `192.168.0.0/16`. That is why all the devices in your
home start with `192.168...`; on the way out, the router hides them all
behind a single **public** address. `127.0.0.1` is the **loopback** address:
it means "this computer itself", and the packet never goes out on a cable.

```python
import ipaddress

for text in ["127.0.0.1", "10.1.2.3", "172.31.0.9", "172.32.0.9",
             "192.168.0.1", "203.0.113.7", "100.20.30.40"]:
    ip = ipaddress.ip_address(text)
    print(f"{text:<14} private={ip.is_private!s:<5} loopback={ip.is_loopback}")
```

```text
127.0.0.1      private=True  loopback=True
10.1.2.3       private=True  loopback=False
172.31.0.9     private=True  loopback=False
172.32.0.9     private=False loopback=False
192.168.0.1    private=True  loopback=False
203.0.113.7    private=True  loopback=False
100.20.30.40   private=False loopback=False
```

Note three details:

- The `172.16.0.0/12` range ends at `172.31.255.255`. `172.31.0.9` is
  private, `172.32.0.9` is public. Saying "it starts with 172, so it is
  private" by eye is wrong.
- For `127.0.0.1`, `is_private` is also `True`. When you classify an
  address, you have to separate loopback **first**.
- `203.0.113.0/24` is a range reserved for use as an **example** in
  documentation; it belongs to no real device, and because it is not
  routed on the internet Python counts it as `is_private` too. In this
  module we use this range when we talk about a server outside.

This distinction comes up often in security: if a request that should come
from inside arrives from an outside address, or a packet coming from
outside carries a private address claiming "I am inside", something is
wrong.

## Ports: the right program on the same computer

The IP address takes a packet to the right computer; but that computer may
be running a web server, a mail server and a database at the same time. The
**port number** picks the right program. A port is a 16-bit number
(0–65535). Common services have well-known ports:

```python
WELL_KNOWN = {22: "ssh", 25: "smtp", 53: "dns", 80: "http",
              443: "https", 3306: "mysql"}

for host, port in [("203.0.113.7", 443), ("203.0.113.7", 22),
                   ("192.168.1.20", 3306), ("192.168.1.20", 8081)]:
    print(f"{host}:{port} -> {WELL_KNOWN.get(port, 'unknown')}")
```

```text
203.0.113.7:443 -> https
203.0.113.7:22 -> ssh
192.168.1.20:3306 -> mysql
192.168.1.20:8081 -> unknown
```

The pair of address and port (`203.0.113.7:443`) identifies one end of a
connection. The side that starts the connection usually uses a large,
randomly chosen port on its own end (like `51514` in the encapsulation
example).

What this means for security: **every open port is a listening program and
therefore part of the attack surface.** The rule from the Attack Surface
section applies here too: unused services are switched off. Ports that
should only be reached from inside, such as a database port (`3306`), are
never opened to the internet.

## TCP and UDP

There are two main protocols at the transport layer:

<figure class="fig"><div class="versus">
  <div><h4>TCP</h4>Sets up a connection first. Confirms that each piece arrives, resends what is lost, keeps the order. The web (HTTP/HTTPS), e-mail and SSH use it.</div>
  <div><h4>UDP</h4>Sets up no connection; it sends the packet and forgets it. No guarantee of delivery or order, but it is fast. DNS queries, video calls and games use it.</div>
</div><figcaption>A choice between reliability and speed.</figcaption></figure>

A TCP connection starts with a **three-way handshake**: the client says "I
want to connect" (SYN), the server answers "fine, me too" (SYN-ACK), the
client says "got it" (ACK). After that, data flows.

<figure class="fig"><div class="flow">
  <span class="node">SYN</span><span class="arrow">→</span>
  <span class="node">SYN-ACK</span><span class="arrow">→</span>
  <span class="node">ACK</span><span class="arrow">→</span>
  <span class="node acc">Data</span>
</div><figcaption>The TCP three-way handshake. After the second step, the server reserves room for the connection.</figcaption></figure>

The last sentence matters: when the server sends SYN-ACK, it reserves room
in memory for the half-finished connection. The **SYN flood** we will see
in the Network Attacks section relies on filling that room.

## Every layer has its own attacks

Layers do not only divide the work; they also help to classify security
problems. Roughly, here is the map of the coming sections:

<figure class="fig anat">
  <div class="anat-row"><span>Link</span><span>ARP spoofing: taking someone's place on the local network (Network Attacks).</span></div>
  <div class="anat-row"><span>Internet</span><span>Forged source addresses, address-based filtering (Network Attacks, Firewalls).</span></div>
  <div class="anat-row"><span>Transport</span><span>SYN floods, open ports (Network Attacks, Firewalls).</span></div>
  <div class="anat-row"><span>Application</span><span>DNS, HTTP, cookies, SQL injection, XSS (the rest of the module).</span></div>
  <figcaption>Defence is layered too: protecting one layer does not protect the others (defence in depth).</figcaption>
</figure>

## Summary

- Network work is split into **layers**: application, transport, internet,
  link (TCP/IP). OSI numbers: 3 network, 4 transport, 7 application.
- Each layer wraps the data in its own header (**encapsulation**); someone
  watching the road can read the headers.
- An **IPv4 address** is a 32-bit number; the `ipaddress` module works with
  addresses and networks.
- **CIDR** (`/24`) says how much of the address identifies the network;
  each prefix bit halves the number of addresses.
- The **private** ranges are `10/8`, `172.16/12`, `192.168/16`; `127.0.0.1`
  is **loopback**. Separate loopback first when classifying.
- A **port** picks the program on the same computer; every open port is
  attack surface.
- **TCP** is reliable and connection-based (three-way handshake), **UDP** is
  fast with no guarantees.
