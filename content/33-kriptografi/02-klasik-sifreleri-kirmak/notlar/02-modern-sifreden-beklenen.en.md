Every attack in this section used the same thing: the ciphertext said
something about the plaintext. That is why what we expect from a modern
cipher is listed like this.

## 1. Output indistinguishable from random

Someone who does not know the key must not be able to look at the
ciphertext and say whether it is a cipher or random bytes. Letter
frequency, index of coincidence, repeated pieces: none may leave a trace.

## 2. Diffusion: one bit, everything

When a single bit of the plaintext changes, about half of the ciphertext
should change. In classical ciphers changing one letter changed only one
letter, which taught the attacker which piece matched what. (We saw the
same effect for a hash function in the What Is Cryptography? section.)

## 3. Resistance to known plaintext

Even if the attacker knows some plaintext–ciphertext pairs (such as knowing
that an e-mail starts with "Hello"), they must not learn the key or the
other messages. In real life the attacker almost always knows something.

## 4. Same message, different ciphertext

Encrypting the same message twice must not give the same ciphertext;
otherwise the attacker learns "these two messages are the same". The
starting value (IV, nonce) that provides this is in the Block Cipher Modes
and IVs section.

## 5. Security only in the key

The algorithm may be known to everyone (Kerckhoffs) and the key space must
be large enough to make brute force impossible (128 bits or more).

## Where do classical ciphers fail on this list?

| Expectation | Caesar | Substitution | Vigenère |
|---|---|---|---|
| Indistinguishable from random | No | No | No (IoC) |
| Diffusion | No | No | No |
| Known plaintext | One letter is enough | A few letters are enough | As many letters as the key length |
| Same message, different output | No | No | No |
| Large key space | No (26) | Yes (2⁸⁸) | Depends on the key length |
