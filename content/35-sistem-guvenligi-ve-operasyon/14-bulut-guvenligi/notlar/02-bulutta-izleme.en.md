In the cloud, resources open and close within minutes. That speed is both
an opportunity and a challenge for security: a wrong configuration spreads
just as fast. This note collects visibility in the cloud and the
protection of accounts.

## The account is the key to everything

An account with access to the management console or programmatic access
in the cloud is like the key to the data centre. That is why:

- The **root account** is not used for daily work; it is protected with
  multi-factor authentication and waits in the vault.
- Every person and every application works with **their own** account,
  with least privilege.
- Where possible, short-lived credentials are used instead of long-lived
  **access keys** (the Secrets Management section); old keys are rotated or
  removed regularly.
- Keys are not written into code or repositories: repositories leaking
  cloud keys are what leak scanners look for most.

## Visibility

Cloud providers offer **audit logs** that record every management
operation in the account (who changed which resource, when). These logs:

- should be on and cover every region,
- should be kept unchangeable, in a separate account or area,
- should be sent to the central logging system, as in the Logging and
  Monitoring section.

Some events to watch in the cloud:

| Event | Why does it matter? |
|---|---|
| The root account being used | It should almost never be used |
| The audit log being switched off | An attacker may want to erase traces |
| A storage area being made public | A possible leak |
| A new administrator privilege | May be privilege escalation |
| Resources opened in an unusual region | A sign of a taken-over account |

## Continuous checking

Because cloud configuration changes constantly, checking once is not
enough. Tools that scan the configuration continuously against set rules
raise an alert when a non-compliant change happens, or roll it back
automatically. This is the cloud version of the security baseline from the
Operating System Security section.

## The exit plan

Depending on one provider is a risk too: an outage, a price change or the
end of a contract. Backing data up in a form that can be taken out (the
Backup and Disaster Recovery section) and being able to move critical
systems to another region reduce this risk.
