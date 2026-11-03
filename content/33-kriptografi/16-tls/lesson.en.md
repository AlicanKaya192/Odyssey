# The TLS Handshake

The `https` in the browser's address bar uses almost every section of this
module at once: key exchange, key derivation, the certificate, the
signature, HMAC and authenticated encryption. The protocol that combines
them is called **TLS** (Transport Layer Security). In this section we
build the TLS 1.3 handshake step by step, never touching the network, with
a small in-memory simulation.

## What TLS provides

| Property | Which part |
|---|---|
| Confidentiality | Key exchange + authenticated encryption (AES-GCM, ChaCha20-Poly1305) |
| Integrity | Authenticated encryption; HMAC in the handshake (Finished) |
| The server's identity | Certificate chain + the server's signature (CertificateVerify) |
| Forward secrecy | Ephemeral Diffie-Hellman on every connection |

## The flow of the handshake

<figure class="fig">
<div class="flow">
<span class="node">ClientHello</span>
<span class="arrow">→</span>
<span class="node">ServerHello</span>
<span class="arrow">→</span>
<span class="node acc">Certificate + signature</span>
<span class="arrow">→</span>
<span class="node acc">Finished</span>
<span class="arrow">→</span>
<span class="node ok">Encrypted data</span>
</div>
<figcaption>TLS 1.3: the client sends its key share in its first message; after the server's reply the traffic is encrypted.</figcaption>
</figure>

1. **ClientHello:** the supported versions, cipher suites and the client's
   Diffie-Hellman **key share**.
2. **ServerHello:** the chosen version and suite, the server's key share.
   At this point both sides can compute the shared secret; everything after
   is encrypted.
3. **Certificate + CertificateVerify:** the server's certificate chain and
   its signature over the hash of the messages so far.
4. **Finished:** both sides send an HMAC over the hash of the whole
   handshake; if a single byte changed on the way, it is caught here.

## Key shares and the transcript hash

We build the messages as dictionaries. Both sides add every message that
goes back and forth, in order, into a hash: this **transcript hash** is
used to prove that both sides saw the handshake the same way.

```python
import hashlib
import hmac
import json

p, g = 4294967291, 5
client_secret, server_secret = 1234567, 7654321
client_hello = {"type": "client_hello", "versions": ["TLSv1.3"],
                "suites": ["TLS_AES_128_GCM_SHA256", "TLS_CHACHA20_POLY1305_SHA256"],
                "key_share": pow(g, client_secret, p)}
server_hello = {"type": "server_hello", "version": "TLSv1.3",
                "suite": "TLS_AES_128_GCM_SHA256",
                "key_share": pow(g, server_secret, p)}


def transcript_hash(messages):
    h = hashlib.sha256()
    for m in messages:
        h.update(json.dumps(m, sort_keys=True).encode())
    return h.digest()


client_shared = pow(server_hello["key_share"], client_secret, p)
server_shared = pow(client_hello["key_share"], server_secret, p)
th = transcript_hash([client_hello, server_hello])
print(client_shared == server_shared)
print(len(th))
```

```text
True
32
```

Two messages went back and forth and both sides reached the same shared
secret (the Diffie-Hellman and Elliptic Curves section). In real TLS the key
share is mostly done with the X25519 curve.

## Deriving the keys

The shared secret goes through the HKDF from the Key Derivation section.
The transcript hash is added to the label too, so the keys belong to this
handshake only. Traffic from client to server and from server to client is
encrypted with **separate** keys.

```python
def hkdf_extract(salt, secret):
    return hmac.new(salt, secret, hashlib.sha256).digest()


def hkdf_expand(prk, info, length=32):
    out, block, counter = b"", b"", 1
    while len(out) < length:
        block = hmac.new(prk, block + info + bytes([counter]), hashlib.sha256).digest()
        out += block
        counter += 1
    return out[:length]


prk = hkdf_extract(b"toy-tls", client_shared.to_bytes(4, "big"))
client_key = hkdf_expand(prk, b"c hs traffic" + th)
server_key = hkdf_expand(prk, b"s hs traffic" + th)
print(client_key != server_key)
print(len(client_key), len(server_key))
```

```text
True
32 32
```

## The server's identity

Key exchange alone does not say who the server is. The server sends its
certificate, verified as in the Certificates and PKI section, and **signs
the transcript hash with the key in that certificate**. The client
verifies the signature with the certificate's public key: that is how it
learns that whoever sent the key share owns that certificate's private key.

```python
n, e = 104717 * 104743, 65537
d = pow(e, -1, (104717 - 1) * (104743 - 1))
signed = int.from_bytes(th, "big") % n
cert_verify = pow(signed, d, n)
print(pow(cert_verify, e, n) == signed)
```

```text
True
```

## Finished: a changed handshake is caught

What happens if someone in the middle tries to replace the cipher suite
list in the ClientHello with a weak suite (a **version or suite
downgrade**)? The server sees the changed message and computes its own
transcript hash from it. The HMAC in Finished requires both sides' hashes
to be the same:

```python
finished_key = hkdf_expand(prk, b"finished")
client_finished = hmac.new(finished_key, th, hashlib.sha256).digest()

changed = dict(client_hello, suites=["TLS_WEAK_SUITE"])
server_view = transcript_hash([changed, server_hello])
server_expects = hmac.new(finished_key, server_view, hashlib.sha256).digest()
same = hmac.new(finished_key, th, hashlib.sha256).digest()
print(hmac.compare_digest(client_finished, same))
print(hmac.compare_digest(client_finished, server_expects))
```

```text
True
False
```

For the unchanged handshake, Finished matched; for the changed one it did
not, and the connection is not made. (In the simulation both sides use the
same `finished_key`; in real TLS each direction's Finished key is derived
separately.)

## Versions and cipher suites

- **TLS 1.3** defines only five cipher suites; three are common:
  `TLS_AES_128_GCM_SHA256`, `TLS_AES_256_GCM_SHA384`,
  `TLS_CHACHA20_POLY1305_SHA256`. All are authenticated encryption.
- **TLS 1.2** is still used, but only with strong suites (AEAD and
  ephemeral keys).
- **SSL 3.0, TLS 1.0 and 1.1** are no longer used; they are turned off on
  servers and clients.
- The **HSTS** header tells the browser "connect to this site only over
  `https`"; after the first connection there is no fallback to an
  unencrypted one.

## Summary

- TLS combines key exchange, the KDF, the certificate, the signature, HMAC
  and authenticated encryption into one protocol.
- **ClientHello / ServerHello** carry the key shares; the shared secret is
  turned into **separate per-direction** keys with HKDF.
- The server **signs the transcript hash** with the key in its certificate.
- The **Finished** HMAC catches a handshake changed on the way.
- Only TLS 1.3, and TLS 1.2 with strong suites; old versions are turned off.
