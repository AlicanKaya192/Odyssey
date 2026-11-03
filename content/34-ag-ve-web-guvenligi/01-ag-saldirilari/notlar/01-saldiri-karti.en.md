## Attack, layer, defence

| Attack | Layer | What it breaks | Defence |
|---|---|---|---|
| Eavesdropping | Every layer | Confidentiality | Encryption (TLS) |
| Man in the middle | Every layer | Confidentiality, integrity | Encryption + certificate check |
| ARP spoofing | Link | Confidentiality, integrity | Switch checks, detection, TLS |
| Forged source address | Internet | Authenticity | Ingress and egress filtering |
| SYN flood | Transport | Availability | SYN cookies, timeouts, rate limiting |
| DDoS | All | Availability | Capacity, upstream filtering |
| Port scanning | Transport | (Reconnaissance) | Closed ports, detection from logs |
| Replay | Application | Integrity | Nonce, timestamp |

## Terms

- **Eavesdropping** (sniffing): reading the traffic on the road.
- **Man in the middle** (MitM): getting between two sides to read and
  change messages.
- **ARP**: the local network protocol that asks for the MAC address of an
  IP address; it does not verify the answer.
- **Reflection / amplification**: asking questions with the victim's
  address so the answers rain down on them; amplification if the answer is
  bigger than the question.
- **Botnet**: a network of devices taken over without their owners
  knowing.
- **SYN cookie**: the server reserving no room until the ACK arrives.
- **Nonce**: a value used only once.

## Rules

- **An IP address is not proof of identity.** Tie permissions to
  authentication, not to the address.
- Encryption hides the content, **not the headers**.
- You **do not click past** the browser's certificate warning.
- Rate limits are kept **per source**.
