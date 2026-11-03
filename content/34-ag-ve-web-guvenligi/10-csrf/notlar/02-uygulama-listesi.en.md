The steps to follow when adding CSRF defence to a web application, and
common mistakes.

## Steps

1. **List the endpoints that change state.** Money, settings, passwords,
   e-mail, deleting, adding: all of them. If any changes state with `GET`,
   turn it into `POST` first.
2. **Make a token and tie it to the session.** When the session opens or
   the form is made, `secrets.token_urlsafe(32)`.
3. **Send it as a hidden field in every form.** For requests made by
   script, the token is sent in a special header.
4. **Check it on the server on every request that changes state.** If the
   token is missing or does not match, the request is refused; no detailed
   error message is given.
5. **Write `SameSite=Lax` (or `Strict`) on the session cookie.**
6. **Check the `Origin` header against an allow list.**
7. **Re-authenticate for important actions** (password or MFA).

## Common mistakes

- **Putting the token only in some forms:** the attacker finds the
  unprotected one. The check is applied in one place to all requests that
  change state.
- **Accepting a missing token:** if "check the token if there is one" is
  written, a request without a token passes unchecked.
- **Comparing the token with `==`:** a timing side channel;
  `compare_digest`.
- **The same token for everyone:** the token must be tied to the session; a
  fixed token works everywhere once it is seen.
- **Carrying the token in the address:** it ends up in logs and the
  `Referer` header.
- **"We are a JSON API, CSRF does not concern us":** it does if the API
  authenticates with a cookie. If authentication is done not with a cookie
  but with a token sent explicitly in a header, the browser does not attach
  it by itself and the CSRF risk drops (the Secure APIs section).

## Test

- Is a request without a token refused?
- Is a request with another session's token refused?
- Can state be changed with `GET`? (It must not.)
- Does the session cookie have `SameSite`?
