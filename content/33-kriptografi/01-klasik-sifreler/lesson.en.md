# Classical Ciphers

Long before computers, people wanted to hide their messages. The
**classical ciphers** in this section are done by hand with letters, and
none of them is secure today. They are still worth learning: the two basic
moves of modern cryptography, **substitution** and **transposition**, first
appear here, and seeing why they were broken explains why today's
algorithms are needed. The next section, Breaking Classical Ciphers, will
break every one of them.

## The Caesar cipher

The simplest cipher, said to have been used by Julius Caesar: every letter
is **shifted** a fixed number of places in the alphabet. With a shift of 3,
`A` → `D`, `B` → `E`, `Z` → `C` (at the end it wraps to the start). The key
is the shift.

We shift using the letter's position in the alphabet with `% 26`, and leave
everything that is not a letter alone:

```python
def caesar(text, shift):
    result = ""
    for ch in text:
        if ch.isalpha() and ch.isascii():
            base = ord("A") if ch.isupper() else ord("a")
            result += chr((ord(ch) - base + shift) % 26 + base)
        else:
            result += ch
    return result


secret = caesar("Attack at dawn!", 3)
print(secret)
print(caesar(secret, -3))
print(caesar("Hello", 13), caesar(caesar("Hello", 13), 13))
```

```text
Dwwdfn dw gdzq!
Attack at dawn!
Uryyb Hello
```

Decrypting is shifting the other way (`-3`). **ROT13** on the last line is
a special case: it shifts by exactly half of the 26 letters, so applying it
twice gets you back, and encrypting and decrypting are the same operation.
Today ROT13 is only used for jokes like "don't see the puzzle answer
straight away"; like Base64 in the What Is Cryptography? section, it gives
no confidentiality.

The Caesar cipher's weakness is plain: there are only **26 keys** (counting
0). Trying all of them by brute force takes less than a second.

## The substitution cipher

To make the key space larger, instead of shifting by a fixed number we can
pick a **random** letter for every letter. The key is then an ordering of
the 26 letters:

```python
import math
import string

plain = string.ascii_lowercase
key = "qwertyuiopasdfghjklzxcvbnm"
table = str.maketrans(plain, key)
back = str.maketrans(key, plain)

secret = "attack at dawn".translate(table)
print(secret)
print(secret.translate(back))
keys = math.factorial(26)
print(f"{keys:.2e} keys, {math.log2(keys):.1f} bits")
```

```text
qzzqea qz rqvf
attack at dawn
4.03e+26 keys, 88.4 bits
```

A key space of about 88 bits: by the calculation in the What Is
Cryptography? section, brute force would take millions of years. Yet this
cipher is broken in a few minutes, because brute force is not needed: the
same letter **always** becomes the same letter, and the language's letter
frequencies stay in the ciphertext as they were. The lesson: **a large key
space alone is not security.** We will measure this in the next section.

**Atbash** is one of the oldest members of this family: the alphabet is
reversed (`a` ↔ `z`, `b` ↔ `y`). It has no key at all; it is even weaker
than Caesar.

## The Vigenère cipher

The **Vigenère** cipher, which spread in the 16th century, is an answer to
the letter-frequency problem: instead of a single shift, the letters of a
**keyword** are used as shifts in turn. With the key `lemon` the first
letter is shifted by `l` (11), the second by `e` (4), and when the key runs
out it starts again. So the same plaintext letter becomes different letters
in different places.

```python
def vigenere(text, key, sign=1):
    result = ""
    i = 0
    for ch in text:
        if ch.isalpha() and ch.isascii():
            shift = ord(key[i % len(key)].lower()) - ord("a")
            base = ord("A") if ch.isupper() else ord("a")
            result += chr((ord(ch) - base + sign * shift) % 26 + base)
            i += 1
        else:
            result += ch
    return result


secret = vigenere("attack at dawn", "lemon")
print(secret)
print(vigenere(secret, "lemon", -1))
```

```text
lxfopv ef rnhr
attack at dawn
```

Note: the key position (`i`) only moves on **letters**; a space does not
use up a key letter. Look at the two `a`s on the first line (the first and
fourth letters of `attack`): one became `l`, the other `o`.

Vigenère was believed unbreakable for three hundred years and was called
"the indecipherable cipher". Its weakness is that the key **repeats**: once
the key length is known, the text splits into a separate Caesar cipher per
key letter and each is broken on its own. We will see how in the next
section.

## Transposition ciphers

The ciphers so far **changed** the letters. **Transposition** ciphers do
not touch the letters; they only change their **order**. The simplest is
the **rail fence** cipher: the letters are written in a zigzag over a few
rows, then the rows are read one after another.

```python
def rail_fence(text, rails):
    if rails == 1:
        return text
    rows = [""] * rails
    row, step = 0, 1
    for ch in text:
        rows[row] += ch
        if row == 0:
            step = 1
        elif row == rails - 1:
            step = -1
        row += step
    return "".join(rows)


print(rail_fence("WEAREDISCOVERED", 3))
print(rail_fence("WEAREDISCOVERED", 1))
```

```text
WECRERDSOEEAIVD
WEAREDISCOVERED
```

The letter frequencies in the ciphertext **do not change at all**: there
are just as many `E`s as before. So counting letters gives transposition
away at once; the key space is small too (the number of rows).

## Two basic moves

<figure class="fig"><div class="versus">
  <div><h4>Substitution</h4>Every letter becomes another letter: Caesar, substitution, Vigenère. The ancestor of <b>confusion</b> in modern ciphers.</div>
  <div><h4>Transposition</h4>The letters stay the same, their places change: the rail fence. The ancestor of <b>diffusion</b> in modern ciphers.</div>
</div><figcaption>Modern block ciphers apply both, one over the other, for many rounds.</figcaption></figure>

On its own each is weak. Modern ciphers (such as AES in the Symmetric
Encryption section) apply both together for many rounds with a computer, so
neither letter frequencies nor order carry over from plaintext to
ciphertext.

## Summary

- **Caesar:** a fixed shift, 26 keys; **ROT13** is its own inverse.
- **Substitution:** 26! (≈ 88 bits) keys, but because the same letter always
  becomes the same letter it is broken by letter frequency. A large key
  space alone is not security.
- **Vigenère:** a shift that changes with a keyword; its weakness is that
  the key repeats.
- **Transposition:** the letters stay, the order changes; letter frequency
  is left as it was.
- Substitution and transposition are the ancestors of confusion and
  diffusion in modern ciphers.
