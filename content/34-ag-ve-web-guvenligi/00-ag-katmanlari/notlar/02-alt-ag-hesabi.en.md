When you write a firewall rule, split a network, or work out whether an
address in a log is "one of ours", you always do the same calculation.

## Number of addresses

An IPv4 network with prefix `/n` has `2 ** (32 - n)` addresses.

| Prefix | Addresses | Left for devices |
|---|---|---|
| `/16` | 65536 | 65534 |
| `/24` | 256 | 254 |
| `/26` | 64 | 62 |
| `/30` | 4 | 2 |
| `/32` | 1 | One device |

The "left for devices" count drops the first address (the network itself)
and the last address (broadcast).

## Splitting a network

If `192.168.1.0/24` is split into four equal parts, each part is a `/26`:

- `192.168.1.0/26`
- `192.168.1.64/26`
- `192.168.1.128/26`
- `192.168.1.192/26`

Adding one prefix bit splits the network in two, two bits in four. Network
segmentation (the VPNs and Network Segmentation section) is done with
exactly this calculation: the guest Wi-Fi is one part, the servers another.

## Which network is an address in?

AND the address with the netmask bit by bit: the result is the network
address. `192.168.1.77` with `255.255.255.0` → `192.168.1.0`. In Python,
`ip in net` does this for you.

## Common mistakes

- **"If it starts with 172 it is private"**: wrong; the private range is
  `172.16` – `172.31`.
- **Taking loopback for private:** `is_private` is also `True` for
  `127.0.0.1`; do not read the log as "it came from the local network", it
  came from this computer.
- **Taking a `/24` for 256 devices:** 254 addresses are left for devices.
- **Comparing as text:** `"192.168.1.9" < "192.168.1.10"` is `False` as
  text; turn addresses into `ipaddress` objects and compare those.
