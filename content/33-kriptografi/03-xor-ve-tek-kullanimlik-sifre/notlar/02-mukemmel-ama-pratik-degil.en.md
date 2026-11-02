The one-time pad is the only method that gives perfect secrecy; even so it
is almost never seen in everyday use. The reasons explain why modern
cryptography chose "secure enough".

## The key distribution problem

Because the key is as long as the message, for every byte you will send you
must first get one byte of key to the other side **by a safe route**. That
is why paper pads carried in diplomatic bags were used. A website cannot
send that much key to every visitor in advance.

## Storage and destruction

A used key page must be destroyed at once, unused ones kept secret. Both
sides must stay in step on the key order; if a page is skipped, every later
message is unreadable.

## True randomness

If the key is made with a program's `random` module, condition 1 is broken
and the proof no longer holds. In the Randomness section we will see why
`random` is predictable.

## The modern answer: computational security

Modern ciphers do not claim perfect secrecy. Instead they give
**computational security**: with a short (128- or 256-bit) key, every known
attack takes longer than the lifetime of the universe. The brute-force
calculation in the What Is Cryptography? section is its measure. This way a
single short key can encrypt gigabytes of data, and the key can be agreed
even over an insecure network with asymmetric methods (the Diffie-Hellman
and Elliptic Curves section).

| | One-time pad | Modern symmetric cipher |
|---|---|---|
| Security | Perfect (proven) | Computational |
| Key length | As long as the message | 128–256 bits |
| Can the key be reused? | Never | Yes (with a new nonce for each message) |
| Integrity | None | In authenticated modes |
| Practical? | Very special cases | Everywhere |
