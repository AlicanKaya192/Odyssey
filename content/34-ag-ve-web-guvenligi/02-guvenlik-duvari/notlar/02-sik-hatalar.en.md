Most firewall mistakes are habits, not technical errors: a rule is added
"for now" and stays for years.

## Everything everywhere

A rule like `allow any any` (from every source to every port) is the same
as switching the firewall off. It is usually added temporarily to fix a
problem. A temporary rule gets an **end date** written on it and is removed
on that date.

## Shadowed rules

A broad allow makes a narrow deny below it useless. The reader sees the "23
closed" line in the list and thinks they are safe. After every change, the
rule list is read with the question "can any packet ever reach this
rule?"; tools count how many packets each rule matched.

## Opening a management port to the internet

If SSH (22) or remote desktop (3389) is opened to `0.0.0.0/0`, every
automated scanner on the internet finds it and tries passwords. These
ports are opened only to the management network or to those coming over
the VPN (the VPNs and Network Segmentation section).

## Filtering only the way in

If the inbound rules are solid but outbound is "allow everything", a
compromised computer connects out freely and sends data. An allow list is
used on the way out too.

## Not logging

If refused packets are not logged, attack attempts are invisible; if
important accepted connections are not logged, nobody can work out what
happened after an incident.

## Trusting the firewall too much

Saying "we are behind the firewall" means trusting every computer inside.
The network firewall does not see an attack that starts inside. That is
why the network is split, every computer keeps its own firewall on, and
applications do not give up on authentication.

## Review checklist

- Is the default decision `deny`?
- Does every rule have an owner, a reason and (if temporary) an end date?
- Are there rules that never match or are shadowed?
- Are management ports closed to the internet?
- Is outbound traffic filtered and logged?
