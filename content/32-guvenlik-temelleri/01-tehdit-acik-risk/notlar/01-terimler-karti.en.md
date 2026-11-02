| Term | Meaning | In the house |
|---|---|---|
| **Asset** | Something worth protecting | The things in the house |
| **Threat** | Something that could harm the asset | A burglar in the neighbourhood, a fire |
| **Threat actor** | The person or group behind a threat | The burglar himself |
| **Vulnerability** | A weakness a threat can use | A back window that does not lock |
| **Exploit** | A way of using the vulnerability | Opening the window and climbing in |
| **Risk** | Likelihood × impact | The chance he gets in and the size of the loss |
| **Control** | Anything that reduces risk | A window lock, an alarm, insurance |
| **Patch** | A fixed version that closes a vulnerability | Repairing the window |
| **Zero-day** | A vulnerability with no patch yet | A secret door nobody knows about |

## CVE and CVSS

- **CVE:** the shared identifier given to every known vulnerability,
  `CVE-YEAR-NUMBER`; the number has at least four digits.
- **CVSS:** the vulnerability's score from 0 to 10. Severity names: 0.0
  None, 0.1–3.9 Low, 4.0–6.9 Medium, 7.0–8.9 High, 9.0–10.0 Critical.
- CVSS describes the vulnerability, not your risk: the same vulnerability
  is urgent on a server open to the internet and less urgent on a closed
  test machine.

## Threat actors

| Actor | Aim | Capability |
|---|---|---|
| Curious / inexperienced | Trying, showing off | Low, ready-made tools |
| Criminal group | Money | Medium to high, organised |
| Insider | Revenge, money or just a mistake | Already has access |
| Hacktivist | Sending a message | Varies |
| State-backed group | Espionage, sabotage | Very high, patient |

## Remember

- Risk needs a threat **and** a vulnerability; you usually cannot remove
  the threat, but you can close the vulnerability.
- Not every threat is a person: failures, fire and floods are threats too.
