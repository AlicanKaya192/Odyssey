A login page is the place in authentication that gets attacked most.
Check the following on a login page you write or review.

## Error messages

- Do not give **two different messages** such as "user not found" and
  "wrong password". With that difference an attacker learns which
  usernames exist; this is called **user enumeration**.
- One message is enough: "Wrong username or password."
- The same difference must not show in the response time either: if no
  calculation is done for a user who does not exist, the answer comes back
  faster and gives away the same information.

## Limiting tries

- Count wrong tries in a row both **per account** and **per source**.
- Instead of a permanent lock, use growing waits (1 s, 2 s, 4 s...); then
  an attacker cannot lock the real user out.
- Record accounts that get locked or receive many wrong tries; a detective
  control.

## Password reset

- The reset link should be single-use and short-lived.
- Do not say "this e-mail is not registered"; say "if it is registered, a
  link has been sent".
- When the password changes, close the open sessions.

## MFA

- Ask for MFA not only at login but also for sensitive actions such as
  changing the e-mail address or the password.
- Show backup codes once, store them as hashes and make each one
  single-use.
- Turning MFA off should also require authenticating again.

## Transport

- The login page should only be served over an encrypted connection
  (HTTPS). A password sent over a plain connection can be read by anyone on
  the way (Network and Web Security module).
