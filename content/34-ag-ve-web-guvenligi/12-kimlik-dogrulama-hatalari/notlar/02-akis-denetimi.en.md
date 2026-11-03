Authentication is not a single page but several flows. Each is checked
separately; the attacker picks the weakest.

## Login

- [ ] One message on a failed login; the same timing for an unknown user.
- [ ] Attempt limits per account and per source, increasing delay.
- [ ] The session ID is renewed on a successful login (Sessions and
  Cookies).
- [ ] Successful and failed logins are logged (not the password).

## Sign-up

- [ ] A "this user name is taken" message leads to enumeration; if sign-up
  is confirmed by e-mail, the message is "we sent a confirmation link".
- [ ] Password rule: length and known bad passwords.
- [ ] Rate limits against automated mass sign-up.

## Password reset

- [ ] The same message whether the address is registered or not.
- [ ] The token is random, short-lived, single-use and hashed on the
  server.
- [ ] If the token is carried in the address, it is used as soon as the
  page opens and does not go to another site through `Referer`.
- [ ] After a reset, the other sessions are closed and the user is
  notified.

## MFA

- [ ] The session is not considered fully authorised before the second
  step is completed.
- [ ] There is a rate limit on code attempts too (a 6-digit code has
  1000000 possibilities; with unlimited attempts that is not many).
- [ ] Backup codes are single-use and stored hashed.

## Password change

- [ ] The old password or MFA is asked (so someone who took over the
  session cannot change it alone).
- [ ] After the change, the other sessions are closed.
