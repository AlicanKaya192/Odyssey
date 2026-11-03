A forensic examination looks for evidence-based answers to a series of
questions: what happened, when, how, which data was affected? This note
covers how an examination proceeds from start to finish.

## Steps

1. **Identification:** which systems, which accounts, which logs are
   relevant? The incident response timeline and indicators of compromise
   guide this.
2. **Preservation:** the evidence is kept unchanged: a write blocker, a
   hash, the chain of custody, a locked cabinet. Copies of logs are taken
   before their retention period runs out.
3. **Collection:** in order of volatility; for everything collected, its
   hash and who collected it, when and with which tool are written down.
4. **Examination and analysis:** on copies; file times, logs and network
   connections are combined into a timeline.
5. **Reporting:** findings, method, limits; a short summary for the
   non-technical reader and detail for the expert.

## The legal side

The findings of digital forensics may be used in court, a disciplinary
process or an insurance claim. That is why:

- How the evidence was collected matters at least as much as what was
  found; evidence not collected by the rules may be ruled invalid.
- Access to personal data and correspondence is subject to legal limits;
  the examination is done by authorised people within their authority.
- In serious incidents the legal team is involved from the first moment.

## Common mistakes

| Mistake | Result |
|---|---|
| Opening files on the suspect machine "just to look" | Access times change, traces are damaged |
| Switching the machine off and on | The traces in memory are lost |
| Taking the hash later | A change between collection and hash cannot be ruled out |
| Not writing down handovers | A gap in the chain of custody |
| Basing a finding on a single source | A changed trace can mislead |

## Preparation pays off here too

The quality of the examination depends on which logs were kept before the
incident. In an organisation without central logging, synchronised clocks
and a long enough retention period (the Logging and Monitoring section),
even the best examination may end with "we cannot know".
