A disaster recovery plan becomes trustworthy only once it is tested. A plan
that looks flawless on paper may get stuck at the first drill on a missing
password, an old phone number or a restore that takes far longer than
expected.

## Kinds of drill

| Kind | What is done? | Cost |
|---|---|---|
| Tabletop | The team walks through a scenario step by step by talking | Low; systems are not touched |
| Partial restore | One system or data set is restored to a separate environment | Medium |
| Full failover | The service is really moved to the standby site or region | High; risk of downtime |

Most organisations start with tabletop drills, do partial restores
regularly and try a full failover less often.

## What is looked at in a drill?

- Did the restore really finish within the **RTO**? The time is measured,
  not estimated.
- How old is the data that came back? Was the **RPO** met?
- Could the needed passwords, keys and documents be found? (The secrets
  vault may be unreachable in a disaster too.)
- Did everyone know what to do? Was the contact list up to date?
- Dependencies: the database came back, but was the configuration of the
  service that connects to it forgotten?

## Availability during a disaster

The plan itself and the information it needs are also kept **outside** the
systems the disaster will affect: if the plan is only a document on the
crashed server, it cannot be reached when it is needed most. Likewise,
backup encryption keys are not kept in the same place as the backups, but
are kept somewhere reachable; an encrypted backup whose key is lost is the
same as no backup.

## After the drill

Every drill ends like a post-incident review: what went well, what got
stuck, which fix is owned by whom and by when (the Incident Response
section). The plan is updated with these findings, and the next drill
checks whether the fixes worked.
