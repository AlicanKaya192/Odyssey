A domain's DNS records pile up over time: services tried and abandoned, old
servers, subnames nobody remembers any more. A regular review asks these
questions.

## For every record

- **Is this name still used?** An unused subname is deleted.
- **Is the CNAME target still ours?** If the target is on an outside
  service, do the account and the resource still exist there? If not, the
  record is dangling and is deleted at once (subdomain takeover).
- **Is the A record's address still ours?** An address left behind in the
  cloud may have been given to another customer.
- **Is the TTL sensible?** A very long TTL means a change or a wrong record
  is corrected late. The TTL is shortened before a move.

## For the domain itself

- Is **MFA** on in the account where the domain is registered, and who has
  access?
- Is the domain about to expire? An expired name can be taken by someone
  else; automatic renewal is kept on.
- Is DNSSEC on?

## On the company network

- Which resolver do the computers use? Queries going to an unexpected
  resolver can be a sign of hijacked settings.
- Many queries to very long, random-looking subnames (such as
  `x7f3k9q2.example`) can show DNS being used to smuggle data out; these queries are
  logged and examined.

## Example findings

| Record | Problem | Action |
|---|---|---|
| `shop.example.com` CNAME to an old shop service | The service account was closed | Delete the record |
| `test.example.com` A to an old cloud address | The address is no longer ours | Delete the record |
| `example.com` NS | No MFA on the domain account | Turn on MFA |
