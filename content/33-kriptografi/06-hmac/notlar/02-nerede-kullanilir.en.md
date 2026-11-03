HMAC is used wherever two sides share a key, to verify that a message has
not changed and came from the other side.

## Tokens and sessions

A session token or API token issued by a server is signed with HMAC. Even
if the user changes the values inside the token (such as making their own
role "admin"), the tag does not match and the token is rejected. The toy
JWT in the Identity Management and Single Sign-On section was a small
example of this: signature first, then the claims.

## Webhooks

When one service notifies another of an event (payment received, order
placed), it HMACs the request body with a shared key and sends the tag in a
header. The receiver must not process the request without verifying the
tag; otherwise anyone could send a fake "payment received" notification.

## API requests

Some APIs HMAC every request (method + path + body + timestamp). The
timestamp makes it harder to **replay** a captured request later: the
server rejects a request with a timestamp that is too old.

## File and configuration integrity

If a configuration file or a log is stored next to an HMAC tag, someone who
changes the file but does not know the key is caught. A plain hash is not
enough here (the attacker updates the hash too); the key makes the
difference.

## Things to watch

- The key must be truly secret and long enough (at least 128 bits, random).
- A separate key for each purpose: the encryption key and the MAC key must
  not be the same.
- Always compare the tag with `compare_digest`.
- If verification fails, the message is not processed at all; the error
  message does not say "why" it failed (so as not to give the attacker a
  hint).
