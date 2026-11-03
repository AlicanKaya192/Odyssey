Certificate errors are often seen as "an annoying warning" and switched
off. Yet each one says that a step of verification failed.

| Error | Which step failed | What to do |
|---|---|---|
| Expired | Date | Renew the certificate (set up automatic renewal) |
| Name mismatch | Name | Get a certificate for the right name; check the address being connected to |
| Untrusted root | Trust store | Check whether the root really is trustworthy; do not add random roots |
| Incomplete chain | Chain | The server must send the intermediate certificate too |
| Revoked | Revocation | New key, new certificate |

## What not to do

- **Turning verification off.** A setting such as `verify=False` in code
  turns TLS into a connection that encrypts but does not know whom it is
  talking to; someone in the middle can present their own certificate. Even
  for a test environment, the right way is to add your own root to the
  trust store, not to turn verification off.
- **Leaving the error to the user with a "continue" button.** Users click
  past warnings without reading them (the Social Engineering section).
- **Putting the private key next to the certificate where anyone can read
  it.** The certificate is public; the private key is not.

## A self-signed certificate

A self-signed certificate can be used in a development environment. The
right way to use it: add that certificate's root only to the development
machine's trust store. The wrong way: a self-signed certificate in
production with verification turned off.
