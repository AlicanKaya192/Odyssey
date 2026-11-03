## What forward secrecy is

What happens if a server's long-lived private key is stolen years later?
The answer depends on how the session keys were set up.

<figure class="fig">
<div class="versus">
<div class="no">
<h4>Transport with a long-lived key</h4>
Each session's key is encrypted with the server's permanent public key and
sent. If that private key is stolen one day, the keys of every recorded old
session can be decrypted.
</div>
<div class="ok">
<h4>Ephemeral Diffie-Hellman</h4>
New secret numbers are made for every session, the shared secret is
computed, and the secret numbers are deleted. The long-lived key is used
only for signing; even if it is stolen, the secret of old sessions cannot
be computed again.
</div>
</div>
<figcaption>Forward secrecy: even if today's key is stolen, yesterday's sessions stay protected.</figcaption>
</figure>

## Why it matters

- Encrypted traffic can be recorded today and attacked years later.
- Ephemeral keys make that recording worthless: the secret numbers needed
  to decrypt it no longer exist anywhere.
- In TLS 1.3 key exchange is always done with ephemeral Diffie-Hellman
  (mostly on a curve); that is why forward secrecy is mandatory there.

## Together with authentication

Ephemeral DH alone does not authenticate the other side. The right order:

1. The sides send their ephemeral public values.
2. The server **signs** these values with its long-lived key.
3. The client verifies the signature with the public key in the server's
   **certificate**.
4. The shared secret goes through HKDF to derive the session keys.

The Digital Signatures, Certificates and PKI, and The TLS Handshake
sections open up the parts of this order one by one.
