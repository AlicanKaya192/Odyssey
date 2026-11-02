## The three legs

| Leg | The question it asks | What breaks it | What protects it |
|---|---|---|---|
| **Confidentiality** | Do only the authorised see it? | A leak, a stolen device, wrong sharing | Authentication, access control, encryption |
| **Integrity** | Is the information correct and complete, and is a change noticed? | Unauthorised change, a half-finished copy, a failing disk | Limiting write access, hashes, logs |
| **Availability** | Can it be reached when needed? | Overload, failure, ransomware | Backups, redundancy, load limits |

## Concepts next to it

| Concept | Meaning |
|---|---|
| **Asset** | Anything worth protecting: data, services, hardware, reputation. |
| **Security incident** | An event that breaks, or tries to break, at least one of C, I and A. |
| **Data leak** | Secret information reaching unauthorised people. |
| **Denial of service** | Making a system unable to serve its real users. |
| **Ransomware** | Malware that encrypts files and demands money to unlock them. |
| **Authenticity** | A message or person really comes from the source it claims. |
| **Accountability** | Every action can be traced back to whoever did it. |
| **Non-repudiation** | An action taken cannot be denied later. |
| **SLA** (service level agreement) | A promise about availability, usually as a percentage. |

## Remember

- The three legs can pull against each other: locking it away and throwing
  away the key raises confidentiality and ends availability.
- Not everything that breaks integrity is an attack; failures count too.
- When naming an incident, ask "which leg?"; the control is chosen from
  that.
