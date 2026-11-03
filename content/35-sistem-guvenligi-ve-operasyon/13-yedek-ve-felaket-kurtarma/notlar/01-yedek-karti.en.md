## Concepts

| Concept | Meaning |
|---|---|
| 3-2-1 | 3 copies, 2 different media, 1 outside |
| Offline / immutable backup | A copy not reachable over the network, or not changeable once written |
| RPO | The longest acceptable data loss |
| RTO | The longest acceptable downtime |
| Full backup | A copy of all the data |
| Incremental backup | What changed since the last backup |
| Grandfather-father-son | Keeping daily, weekly and monthly backups for different periods |

## Kinds of backup

| Kind | Backing up | Restoring |
|---|---|---|
| Full | Slow, much space | Fast: one copy is enough |
| Incremental | Fast, little space | Slow: the last full + every incremental |
| Differential | Medium | The last full + the last differential |

## Python patterns

- The longest gap: `max((b - a) for a, b in zip(times, times[1:]))`.
- Hours: `delta.total_seconds() / 3600`.
- Restore time: `setup + size / speed`.
- Comparing: `sha256(restored) == sha256(original)`.
- Is it Sunday: `d.weekday() == 6`; the first of the month: `d.day == 1`.

## Keep in mind

- A backup reachable over the network does not protect against ransomware.
- The RPO sets how often backups run, the RTO how fast restores must be.
- A backup whose restore has never been tried is not trusted.
- Backups are encrypted too and access to them is limited with least
  privilege: a backup is a copy of the data and needs the same protection.
