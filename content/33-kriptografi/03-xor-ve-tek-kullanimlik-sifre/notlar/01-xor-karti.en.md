## XOR rules

| Rule | Meaning |
|---|---|
| `a ^ b ^ b == a` | Encryption and decryption are the same operation |
| `a ^ a == 0` | If the same key is used twice, the key cancels out |
| `a ^ 0 == a` | XOR with zero changes nothing |
| `a ^ b == b ^ a` | Order does not matter |

## Python patterns

- XORing two byte strings: `bytes(x ^ y for x, y in zip(a, b))`.
- Text to bytes: `"PAY".encode()`, back: `b"PAY".decode()`.
- Bytes to hex: `data.hex()`, back: `bytes.fromhex(text)`.
- A real key: `secrets.token_bytes(len(message))`.
- `zip` stops at the shorter one: if the key is short, the end of the
  message is cut off **silently**. Check the length first.

## The four conditions of the one-time pad

1. A truly random key.
2. A key as long as the message.
3. Used only once.
4. Secret.

## Leaks

| Mistake | What the attacker gets |
|---|---|
| Reusing the key | `c1 ^ c2 = m1 ^ m2`; knowing one reveals the other |
| No integrity check | Changing a message of known format bit by bit |
| A short key repeated | Vigenère's weakness comes back |
