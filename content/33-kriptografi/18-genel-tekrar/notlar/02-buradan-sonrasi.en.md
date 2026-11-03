This module showed how cryptography works with small, measured toy
examples. Two modules come next in the path; both use the tools from here
inside real systems.

## Network and Web Security

HTTPS is the applied form of this module's The TLS Handshake section. The
Network and Web Security module looks around the connection: network
layers, firewalls, VPNs, DNS; sessions and cookies (signed cookies are one
use of HMAC), common web flaws and security headers. The "do not turn
verification off" rule from the Certificates and PKI section will meet you
there when writing secure APIs.

## System Security and Operations

The key itself is an asset too: where it is stored, who can reach it, what
is done when it leaks. The System Security and Operations module covers
managing secrets and dependencies, logging, incident response and backups;
the "leaked secret" steps from the Common Cryptography Mistakes section are
part of an incident response plan there.

## Working with real libraries

- Do not use the toy ciphers, keys and curves from the lessons in a real
  program; they were only for showing the idea.
- Pick the library's **high-level** functions (AEAD in one call, a
  ready-made password hash). Combining low-level parts (mode, padding,
  nonce) by hand is the source of most mistakes in this module.
- If the library gives a warning or a "deprecated" message, do not ignore
  it; it is often the sign of an old algorithm.
- Question the defaults: iteration counts, key sizes and TLS versions change
  over time; the table in the Quick Reference note is today's advice.

## While you work

- Open the certificate of a site you use in the browser: read its chain,
  dates and SAN list with the names from this module.
- Go over the settings of one of your projects with the Review Checklist
  note.
