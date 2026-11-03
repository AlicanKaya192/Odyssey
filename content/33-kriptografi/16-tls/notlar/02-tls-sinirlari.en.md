TLS protects the connection; but it is just as important to know what it
does not protect.

| TLS protects | TLS does not protect |
|---|---|
| The confidentiality and integrity of data on the way | How data is stored after it reaches the server |
| That the server connected to belongs to that name | That the site itself is trustworthy (a fake site can get a certificate too) |
| Catching a changed handshake | Flaws in the application (SQL injection, authorization mistakes) |
| Forward secrecy of old sessions | Malware on the endpoint |

## What stays visible

- The **domain name** being connected to is mostly in the clear at the
  start of the handshake (the SNI field); only the content is encrypted.
- The **amount and timing** of the traffic can be seen.
- IP addresses are always visible.

## 0-RTT

TLS 1.3 allows sending data with the very first message to a server
connected to before (0-RTT). It is fast, but that first data **can be
replayed**: the same request may be processed twice. That is why 0-RTT is
used only for requests that are harmless to repeat (such as reading a
page), not for operations such as sending money.

## What the "padlock" means

The padlock in the browser says that the connection is encrypted and that
the certificate was issued for that domain. It does not say the site is
honest: the look-alike fake sites from the Social Engineering section can
get a valid certificate too. What matters is the domain name itself.
