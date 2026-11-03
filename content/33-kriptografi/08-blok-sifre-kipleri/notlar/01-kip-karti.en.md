## Four modes

| Mode | How it works | Same block → same output | Padding | Status |
|---|---|---|---|---|
| ECB | Each block encrypted separately | Yes | Needed | **Not used** |
| CBC | Block XORed with the previous ciphertext block, then encrypted | No | Needed | In older systems |
| CTR | Nonce + counter encrypted, XORed with the message | No | Not needed | With integrity |
| GCM | CTR + an authentication tag | No | Not needed | **Recommended** |

## Why ECB leaks

- Same key, same plaintext block → same ciphertext block.
- Repeated data (the same header, the same field, the flat-colored areas of
  an image) repeats in the ciphertext too.
- Even with a strong key the pattern shows; the problem is the mode, not
  the cipher.

## CBC

- The first block is XORed with the IV, every later block with the previous
  ciphertext block.
- Decryption runs the other way: the block is decrypted, then XORed with
  the previous ciphertext block.
- The IV must be random and unpredictable; it is sent at the start of the
  ciphertext.

## CTR

- What gets encrypted is not the plaintext but `nonce + counter`; the
  output is the keystream.
- Encryption and decryption are the same operation; a block decryption
  function is never needed.
- Blocks are independent and can be processed in parallel.
- If the nonce is repeated with the same key, it falls into the one-time
  pad's key-reuse mistake.

## What they all lack

ECB, CBC and CTR give **confidentiality** only. If one bit of the
ciphertext is changed, the receiver does not notice. Integrity needs an
authenticated mode (GCM) or encryption + a MAC.
