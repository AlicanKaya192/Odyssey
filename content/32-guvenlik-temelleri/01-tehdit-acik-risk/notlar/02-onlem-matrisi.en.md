Controls are classified by two separate questions. **When** does it work
(preventive, detective, corrective) and **what kind** is it (technical,
administrative, physical)?

- **Technical:** a control applied with software or hardware.
- **Administrative:** rules, processes, training; a control that tells
  people what to do.
- **Physical:** doors, locks, cameras; a control that limits getting into a
  place.

Together the two questions form a table. One example for each cell:

| | Preventive | Detective | Corrective |
|---|---|---|---|
| **Technical** | Passwords, encryption, firewalls | Reviewing logs, an intrusion detection system | Restoring from backup, patches |
| **Administrative** | A password policy, security training | Regular audits, access reviews | An incident response plan |
| **Physical** | A locked server room, card access | Security cameras, door alarms | A fire suppression system |

## How is it used?

When dealing with a risk, look across the rows and columns: are all the
controls in the same cell? For example, for the risk "an employee lost
their laptop":

- **Preventive, technical:** encrypting the disk.
- **Detective, administrative:** a rule that the loss is reported at once.
- **Corrective, technical:** locking and wiping the device remotely,
  setting up a new device from backup.

Controls piled up in a single cell leave the whole system defenceless when
that cell is bypassed. Spreading controls across different cells is called
**defence in depth**; it comes in detail in the Security Principles
section.

## Types that are sometimes added

- **Deterrent:** tries to make the attacker give up; a sign saying "this
  area is watched by cameras".
- **Compensating:** a control put in place when the main one cannot be
  applied; separating an old system from the network if it cannot be
  patched.
