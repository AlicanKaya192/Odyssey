## Terms

| Term | Meaning |
|---|---|
| **Attack surface** | The sum of all the points where an attacker can reach the system |
| **Entry point** | Each of those points: a form, an endpoint, a port, a USB port, an employee |
| **Inventory** | The list of what is in the system |
| **Shadow IT** | Systems set up without the IT team knowing |
| **Exposure** | Who can reach an entry point |

## Questions to ask about an entry point

1. Who can reach it: the internet, the internal network, local only?
2. Is authentication needed?
3. What data does it take, what data does it touch?
4. Is it really used (logs)?
5. Who owns it, and when was it last updated?

## Shrinking checklist

- Remove unused endpoints, pages and services.
- Remove packages that are installed but not used.
- Make admin interfaces unreachable from the internet.
- Put databases where only the application can reach them.
- Turn debugging tools off in the live system.
- Start new features turned off by default.
- Look at the difference in the endpoint list in every release.

## Remember

- Hiding is not shrinking: a secret address leaks one day.
- A forgotten door is the most dangerous: it is neither updated nor
  watched.
- Outside libraries are part of the surface too; fewer dependencies, a
  smaller surface.
