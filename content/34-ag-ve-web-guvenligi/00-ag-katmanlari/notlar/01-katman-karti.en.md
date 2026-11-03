## TCP/IP layers

| Layer | OSI no | What it carries | Example |
|---|---|---|---|
| Application | 7 | The program's message | HTTP, DNS, SSH |
| Transport | 4 | Port numbers | TCP, UDP |
| Internet | 3 | IP addresses | IPv4, IPv6 |
| Link | 2 | MAC addresses | Ethernet, Wi-Fi |

Encapsulation: data → segment (TCP header) → packet (IP header) → frame
(Ethernet header). The receiver strips them in reverse order.

## Address ranges

| Range | Meaning |
|---|---|
| `10.0.0.0/8` | Private |
| `172.16.0.0/12` | Private (`172.16` – `172.31`) |
| `192.168.0.0/16` | Private |
| `127.0.0.0/8` | Loopback (this computer) |
| `169.254.0.0/16` | Link-local (when no address could be obtained) |
| `203.0.113.0/24` | Reserved for examples in documentation |

## Well-known ports

| Port | Service | Port | Service |
|---|---|---|---|
| 22 | SSH | 443 | HTTPS |
| 25 | SMTP | 3306 | MySQL |
| 53 | DNS | 5432 | PostgreSQL |
| 80 | HTTP | 3389 | Remote desktop |

## Python patterns

- Address: `ipaddress.ip_address("192.168.1.10")`; `int(ip)`, `ip.version`.
- Network: `ipaddress.ip_network("192.168.1.0/24")`; `net.num_addresses`,
  `net.netmask`, `net.broadcast_address`.
- Is it inside: `ip in net`.
- Kind: `ip.is_loopback`, `ip.is_private`, `ip.is_global`. Loopback also
  counts as `is_private`: check `is_loopback` first.
- Split into subnets: `net.subnets(new_prefix=26)`.

## TCP and UDP

| | TCP | UDP |
|---|---|---|
| Connection | Yes (SYN, SYN-ACK, ACK) | No |
| Loss | Resent | Lost |
| Order | Kept | No guarantee |
| Example | HTTP, SSH, e-mail | DNS query, video call |
