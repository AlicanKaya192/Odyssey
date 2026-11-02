However strong a password is, it loses its value if it has been used
**somewhere else**. Someone who uses the same password on ten sites is only
as safe as the worst-protected of those ten sites.

## How does it happen?

1. A small site that stores passwords badly suffers a leak.
2. Username (often an e-mail address) and password pairs end up in a list
   that gets shared.
3. Automated tools try those pairs on e-mail, banking and shopping sites.
   The success rate is small, but the list has millions of lines.

The attacker does not "break" anything; they only try a key that was left
open somewhere else. This is called **credential stuffing**.

## As a user

- A separate password for every site. The only practical way to do this is
  a **password manager**: it creates the passwords, keeps them in an
  encrypted vault and fills them in on login pages.
- The password manager's **master password** should be a long passphrase,
  and its account should have MFA turned on.
- Protect your e-mail account in particular: the "forgot my password"
  links of your other accounts go there.

## As someone building a system

- At sign-up and password change, check the password against **known leak
  lists**. Methods that check without sending the password to anyone are
  used for this (only the first few characters of the hash are asked
  about).
- If a user's password has appeared in another leak, ask them to change it.
- Many login attempts for different usernames from the same source are a
  sign of a stuffing attack; record it and slow it down.
- MFA is the most effective control against stuffing: the correct password
  alone is not enough.

## Isn't a password manager a single point?

Yes, all the passwords are in one vault. But the vault is encrypted, the
master password is used nowhere else and it is protected with MFA. The
alternative is the same password sitting in ten places; then there is a
single point anyway, and it is in the hands of ten different sites.
