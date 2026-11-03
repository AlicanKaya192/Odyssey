What session mistakes have in common is forgetting that a session ID is as
valuable as a password.

## A predictable ID

Sequential IDs such as `s1001`, `s1002`... or IDs made from the time give
away the next one. IDs are made only with `secrets`.

## An ID not renewed at login

If the ID given before login is used after login too, the session is open
to fixation. Login, privilege escalation and password changes renew the
ID.

## A session that never ends

A "remember me" option does not mean a session ID valid for months. For
long-lived login a separate, revocable token is kept, and for important
operations (changing the password, paying) the password is asked again.

## A logout that ends only in the browser

If the logout button deletes the cookie but leaves the record on the
server, someone with a copy of the cookie carries on. The record is deleted
on the server side.

## A missing attribute

- Without `Secure`, the cookie is read on the way over plain HTTP.
- Without `HttpOnly`, a script that leaks into the page reads and sends the
  cookie.
- Without `SameSite`, the cookie is attached to a request started from
  another site.

## Carrying the ID in the wrong place

- In the URL (`/cart?sid=...`): it ends up in history, server logs and the
  `Referer` header sent to other sites.
- In a log file: anyone who can read the logs takes over the session.

## An unsigned state cookie

Keeping a value such as `role=user` in an unsigned cookie lets the user
choose their own role. It is either kept on the server or signed.

## Quick check

- [ ] The ID is made with `secrets`, at least 128 bits.
- [ ] The ID is renewed at login.
- [ ] There is an idle and an absolute timeout.
- [ ] Logout deletes the record on the server.
- [ ] The cookie has `Secure`, `HttpOnly`, `SameSite`.
- [ ] The ID is not in URLs or logs.
