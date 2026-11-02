## Terms

| Term | One line |
|---|---|
| IAM | Identity and access management: who, to what, until when |
| Directory | The single source of people, groups and roles; access standard LDAP |
| SSO | Log in once, use many applications |
| IdP | Identity provider: where the login happens, only it sees the password |
| SP | Service provider: the application used, trusts the signed token |
| Federation | Different organisations trusting each other's identities |
| SAML 2.0 | Enterprise SSO, XML assertion |
| OAuth 2.0 | Delegation, access token |
| OpenID Connect | Identity on top of OAuth, ID token (JWT) |

## The order of token checks

1. Is the format right? (number of parts)
2. Is the **signature** right? The server decides the algorithm; `none`
   is not accepted.
3. `iss`: is it an IdP we trust?
4. `aud`: is it for our application?
5. `exp`: has it not expired?
6. `nbf`: has validity started?
7. Only after these is the role or permission in the content used.

## To remember

- A signature **does not hide**, it only proves nothing changed; no secrets
  go into a token.
- Access tokens are short-lived; a revocable refresh token for long
  sessions.
- Signature comparison in constant time: `hmac.compare_digest`.
- The IdP is a single target: strong multi-factor authentication and close
  monitoring.
- "Log in with OAuth" usually means OpenID Connect.
