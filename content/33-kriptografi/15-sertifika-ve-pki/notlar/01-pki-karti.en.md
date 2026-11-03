## The parts

| Part | Its job |
|---|---|
| Certificate | Binds a public key to a name; a CA signs it |
| CA (certificate authority) | Checks the name's owner and signs the certificate |
| Root CA | A self-signed authority already in the trust store |
| Intermediate CA | An authority signed by the root that signs sites |
| Trust store | The roots the operating system or browser trusts |
| CRL / OCSP | Announce revoked certificates |
| Transparency logs | A public record of every issued certificate |

## Verification order

1. Build the chain: site → intermediate CA → root.
2. At every link: is `issuer` the `subject` of the one above, and does the
   signature match the public key of the one above?
3. Is the root in the trust store?
4. Is today between `not_before` and `not_after`?
5. Does the name (the SAN list) match the name being connected to? A
   wildcard covers only one label: `*.example.test` → `shop.example.test`
   yes, `a.b.example.test` no.
6. Has it been revoked?

If even one fails, the connection is **not made**.

## The signed bytes

The signature is over the fields of the certificate other than `signature`,
encoded **the same way every time**. Real certificates use ASN.1 DER
encoding for this; in the lesson `json.dumps(..., sort_keys=True)` did the
same job.
