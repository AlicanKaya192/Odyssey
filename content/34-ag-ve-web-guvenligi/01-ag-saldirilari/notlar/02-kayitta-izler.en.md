Most attacks leave traces in the logs. What matters for the defending side
is knowing which trace points to what. The thresholds below are examples;
every network's "normal" is different and the threshold is chosen against
that normal.

## What do you think when you see it?

| Trace in the log | Possible meaning |
|---|---|
| The router's MAC address suddenly changed | ARP spoofing |
| A packet from outside has an internal source address | Forged source address |
| Many SYNs, almost no ACKs | SYN flood |
| Many different ports from one source in a short time | Port scanning |
| Many login attempts from one source | Password-guessing attack |
| The same request arriving twice with the same signature | Replay |
| Large answers to questions never asked | Being the victim of a reflection attack |

## When you find a trace

- **Verify first.** If a new router was installed, the MAC changing is
  normal; a backup job may also open many connections.
- **Record and keep.** Write down the time, source and destination; these
  records are needed in incident response (the Incident Response section).
- **Filter or limit.** Block the source for a while or lower its rate. In
  an attack with forged addresses, blocking the source can punish an
  innocent address; be careful.
- **Close.** Switch off a service that a scan found open but nobody uses.

## Things not to do

- "Counter-attacking" the attacker's address: the address may be forged
  and it is illegal in most places.
- Only blocking addresses and not encrypting content: eavesdropping and
  MitM are still possible.
- Relying on a single threshold: the attacker can stay just below it (a
  slow scan). Several traces are judged together.
