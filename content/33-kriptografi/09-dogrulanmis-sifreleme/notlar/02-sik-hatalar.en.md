Mistakes with authenticated encryption are usually not in the algorithm
but in the code around it.

| Mistake | Why it is a problem | The right way |
|---|---|---|
| Decrypting without checking the tag | Changed data gets processed | `compare_digest` first, then decrypt |
| Comparing the tag with `==` | The comparison time can leak information | `hmac.compare_digest` |
| Taking the tag over the ciphertext only, leaving out the nonce | A changed nonce goes unnoticed | The tag is over nonce + ciphertext |
| Using the same key for encryption and the MAC | The two operations can weaken each other | Separate keys, derived from one master secret |
| Leaving the AAD out of the tag | The header can be changed | The AAD goes into the tag with its length |
| Swallowing the library's "tag mismatch" error | All the protection is wasted | On error the data is thrown away, not used |
| Repeating a nonce | In GCM confidentiality and authentication break | A unique nonce for every message |
| Writing your own combination | Ordering and boundary mistakes are easy | A well-tested AEAD library |

## What to say when rejecting

- When the tag does not match, do not tell the user or the sender in
  detail **why** it was rejected ("the tag differs at this byte"). One
  general "invalid message" is enough.
- Do not write the rejected package's content to the logs; but do log the
  rejection itself (fail securely from the Security Principles section).

## What this lesson left out

The toy cipher and the hand-built encrypt-then-MAC were only for showing
the idea. In a real program, AES-GCM or ChaCha20-Poly1305 is used from a
well-tested library, in a single call.
