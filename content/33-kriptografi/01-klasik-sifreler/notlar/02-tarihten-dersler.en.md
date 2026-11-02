The history of classical ciphers shows three lessons again and again that
still hold today.

## 1. "Nobody can break it" is not a measurement

Vigenère was believed unbreakable for centuries. In the 19th century
Charles Babbage and Friedrich Kasiski showed that a repeating key leaves
traces in the ciphertext; Kasiski published his method in 1863. Those who
used the cipher did not know this and went on thinking they were safe.

The lesson: trust in an algorithm does not come from "nobody has broken it
yet" but from **having been published openly and having withstood attacks
for a long time** (Kerckhoffs's principle in the What Is Cryptography?
section).

## 2. What breaks is often not the algorithm but its use

In the Second World War the German army's Enigma machine had a far larger
key space than hand ciphers. Its breaking owed as much to **mistakes in
use** as to the machine's design: repeated message headers, predictable
words, the same setting used more than once.

The lesson: a strong algorithm becomes weak when used wrongly. The Common
Cryptography Mistakes section at the end of this module covers today's
versions: reusing the same key (XOR and the One-Time Pad), predictable
randomness (Randomness), a repeated starting value.

## 3. The attacker does not come the way you expect

Whoever builds a substitution cipher thinks brute-forcing 26! keys is
impossible, and is right. But the attacker does not use brute force: they
look at letter frequency. Security is measured not by the hardest way the
defender calculated, but by the **easiest** way the attacker finds.

## Where are classical ciphers today?

- In puzzles, games and teaching.
- ROT13 on forums to hide an answer.
- **Nowhere to protect real data.** If you see Caesar, XOR with a fixed key
  or "our own cipher" in a program, that is a vulnerability.
