## Questions for every endpoint

1. **Who?** Did the request pass authentication (session, token, API
   key)? Are the endpoints that must stay open without identity open on
   purpose?
2. **Is this object theirs?** An ownership check for every id in the
   address or the body. Otherwise `404`.
3. **May they do this job?** Do administrator endpoints
   (`DELETE /users/7`) check the role? Hiding an endpoint from the
   interface does not protect it.
4. **Which fields come in?** An allow list of changeable fields.
5. **Which fields go out?** An allow list of showable fields.
6. **How much?** Limits on the number of requests, body size, page size.
7. **What does the error say?** A short code and message; details in the
   log.

## API Security Top 10 (2023) headings

| Heading | In this section |
|---|---|
| Broken Object Level Authorization | Ownership check, `404` |
| Broken Authentication | The Authentication Failures section |
| Broken Object Property Level Authorization | Allow lists on the way in and out |
| Unrestricted Resource Consumption | Bucket, size and page limits |
| Broken Function Level Authorization | Role check (question 3) |
| Unrestricted Access to Sensitive Business Flows | Extra limits for flows such as purchase or sign-up |
| Server Side Request Forgery | The SSRF section |
| Security Misconfiguration | Defaults, headers, error texts |
| Improper Inventory Management | Old versions (`/v1`) and test endpoints must not stay open |
| Unsafe Consumption of APIs | Data from another API is input too |

## Short rules

- Ownership is checked even when the id cannot be guessed.
- The record object is not turned into JSON as it is.
- `429` for a request over the limit, optionally `Retry-After`.
- Old versions are closed or go through the same checks as the new one.
