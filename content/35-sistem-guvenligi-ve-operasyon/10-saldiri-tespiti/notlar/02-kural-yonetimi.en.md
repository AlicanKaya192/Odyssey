A detection system is as good as its rules. Writing a rule is easy; what is
hard is keeping hundreds of rules useful and quiet. This note collects the
life cycle of detection rules.

## A rule's life cycle

1. **Need:** which threat do we want to catch? A threat model or a past
   incident turns into a rule.
2. **Writing:** a pattern, a threshold or a sequence; what it will catch
   and what it will not are written down.
3. **Testing:** the rule is first run over past logs: how many alerts
   would it have produced, how many of them were real?
4. **Release in alert mode:** for a while the rule only alerts; it does not
   block.
5. **Tuning:** the false alarms are examined, the threshold and pattern are
   fixed.
6. **Review:** a rule nobody responds to, or that has not fired for years,
   is questioned.

## Every alert needs a response

If what to do when an alert arrives is not written down, the alert is
either ignored or everyone does something different. Next to every rule
sits a short **response guide** (playbook):

| Field | Example |
|---|---|
| Alert | A successful login after failed logins |
| Severity | High |
| First things to check | Attempts on other accounts from the same address? What was done after login? |
| First step | End the account's sessions, have the password reset |
| Who is told | The security team, the account owner |

## Grouping alerts

A hundred alerts from the same source in a short time are not a hundred
separate jobs but one event. Alerts are grouped by source (address,
account, machine) and time: if the gap between two alerts is shorter than
a set period, they are added to the same event. That way the team looks at
the number of events, not the number of alerts.

## The limits of detection

- A detection system only looks at what it **sees**: it cannot see inside
  encrypted traffic or a system that keeps no logs.
- Every rule rests on an assumption; when the assumption changes (a new
  application, new working hours), the rule is reviewed too.
- Detection does not replace prevention: first the doors are closed, then
  the doors are watched.
