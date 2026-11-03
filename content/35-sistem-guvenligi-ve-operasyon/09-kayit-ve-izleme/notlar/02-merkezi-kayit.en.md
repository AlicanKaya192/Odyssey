Looking at the logs of a single server is easy. But an organisation has
hundreds of servers, applications and network devices, and an attack
touches several of them at once. That is why logs are collected in one
place.

## Central logging

Besides keeping its logs locally, every system sends them to a **central
logging system**. The benefits:

- **The whole picture:** which systems a user touched in the same minute is
  seen with a single query.
- **Resilience:** even if an attacker deletes one server's logs, a copy
  stays in the centre.
- **A common format:** logs are converted to the same field names and to
  UTC time; comparing becomes easy.
- **Access control:** who may read the logs is managed from one place.

Systems that collect logs, correlate them and produce alerts according to
rules are generally called a **SIEM** (Security Information and Event
Management).

## From alerts to fatigue

The most common failure of monitoring is not too few alerts but **too
many**. In a system producing hundreds of unimportant alerts a day, the
real alert gets missed; this is called **alert fatigue**. To reduce it:

| Method | What does it do? |
|---|---|
| Tuning thresholds by measuring | Separates ordinary noise from alerts |
| Grouping alerts | Turns a hundred alerts from one source into one event |
| Assigning severity | The critical one is looked at first |
| Writing a response for every alert | "What is done when this alert comes?" is clear |
| Removing an alert nobody looks at | Noise drops |

This topic is covered in detail, with measurements, in the Intrusion
Detection section.

## Logs are protected too

Logs are among a system's most sensitive data: who connected, when, from
where. That is why the logging system is opened with least privilege too,
logs are encrypted in transit, very few people can delete or change logs,
and those operations are themselves logged.

## Measuring monitoring

How well a monitoring setup works is measured by two durations:

- **Time to detect:** the time between an event starting and it being
  noticed.
- **Time to respond:** the time between it being noticed and it being
  stopped.

Both are measures used in incident response (the Incident Response
section); the better the monitoring, the shorter the first one.
