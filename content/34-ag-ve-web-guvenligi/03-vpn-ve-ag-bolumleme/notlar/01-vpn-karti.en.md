## A VPN at a glance

| Question | Answer |
|---|---|
| What does it build? | An encrypted tunnel between two points |
| How? | The inner packet is encrypted and put in an outer packet |
| What does someone on the road see? | Only the outer packet: source, VPN gateway, size, time |
| Remote access | A computer connects to the company network |
| Site-to-site | Two networks are connected to each other |
| Split tunneling | Only company traffic goes through the tunnel |

## Protects / does not protect

| Protects | Does not protect |
|---|---|
| Eavesdropping on shared Wi-Fi | Malware on the computer |
| Getting in the middle on the local network | A password typed into a phishing page |
| Using internal servers without opening them to the internet | The road after the gateway |
| | The visited site's holes |
| | Anonymity (the VPN provider sees it) |

## Rules

- A device connected to the VPN becomes **part of the internal network**;
  the device and the person are checked strictly (MFA, an up-to-date
  device).
- Not everyone coming over the VPN gets the whole internal network;
  segmentation still applies.
- Management ports (SSH, remote desktop) are opened to the VPN or the
  management network, not to the internet.
- The VPN gateway itself is a server open to the internet: it is kept up
  to date and watched.

## Terms

- **VPN gateway**: the company end of the tunnel.
- **Tunnel**: the road on which encrypted inner packets are carried inside
  outer packets.
- **Split tunneling**: only selected traffic going through the tunnel; the
  opposite is a **full tunnel**.
