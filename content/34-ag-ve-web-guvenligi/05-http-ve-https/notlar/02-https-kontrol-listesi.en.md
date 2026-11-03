What to look at on the HTTP and HTTPS side before putting a website live.

## Transport

- [ ] The site is served only over HTTPS; plain HTTP only redirects to
  HTTPS with a `301`.
- [ ] The redirect keeps the path and query and does not lead to another
  domain.
- [ ] There is a `Strict-Transport-Security` header; `max-age` is at least
  a year. `includeSubDomains` if all subdomains are ready for HTTPS.
- [ ] The certificate is valid and renewed before it expires (automatic
  renewal).
- [ ] Every script, stylesheet and image on the page loads over `https://`.

## Requests

- [ ] No work that changes state is done with `GET`.
- [ ] The server trusts no field in the request (hidden form field, header,
  cookie) without validating it.
- [ ] Secret values such as passwords and tokens are **not** carried in the
  URL: addresses are written into browser history, server logs and the
  `Referer` header sent to other sites. They go in the body or a header.

## Responses

- [ ] Error pages show no stack trace, file path or SQL query.
- [ ] Headers such as `Server` give no version number.
- [ ] When a resource belonging to someone else is requested, 404 is
  returned so as not to reveal that it exists.

## Common misconceptions

- **"There is a padlock, so it is safe":** the padlock describes the
  connection; a phishing site has a padlock too.
- **"The login page is HTTPS, the rest can be HTTP":** the session cookie
  is read on the way on plain HTTP pages. The whole site is HTTPS.
- **"We tried HSTS for a minute":** a short `max-age` does not protect; it
  is tried with a short time first and then extended.
