# Randomness

In the XOR and the One-Time Pad section, the first condition of the
one-time pad was "the key is truly random". In the Passwords section we
made passwords with `secrets`, not `random`, and left the details for
here. This section explains why randomness matters so much in
cryptography, the two kinds of random number generators, how to use the
right source in Python, and a quiet mistake people make when using a
random number.

## Why does cryptography rest on randomness?

Remember Kerckhoffs's principle from the What Is Cryptography? section:
the algorithm is public, only the **key** is secret. If the key can be
predicted, even the strongest algorithm protects nothing. Keys are not the
only values in a system that must be made at random:

| Value | What it is for | Typical size |
|---|---|---|
| Key | The secret input of encryption and HMAC | 128 or 256 bits |
| Nonce / IV | Encrypting every message differently under the same key | 96 or 128 bits |
| Salt | Making the hashes of equal passwords different | 128 bits |
| Token | Session ids, password reset links, API keys | 128 bits and up |

What these values share is that they **cannot be predicted**. "Looking
random" is not enough: someone watching from outside must not be able to
work out the next value from the earlier ones.

## Two kinds of generator

A computer does nothing random on its own; every step follows a rule.
Random numbers come from two places:

- A **pseudo-random number generator** (PRNG) makes a sequence of numbers
  from a starting value, the **seed**, with a mathematical rule. The
  sequence looks random and passes statistical tests, but the same seed
  gives the same sequence. Python's `random` module works like this (an
  algorithm called Mersenne Twister); it is written for simulations, games
  and sampling.
- A **cryptographically secure PRNG** (CSPRNG) is fed by noise the
  operating system collects from hardware and events, and seeing its
  output does not help predict the next value. In Python the `secrets`
  module and `os.urandom` use it (`BCryptGenRandom` on Windows, `getrandom`
  on Linux).

## Same seed, same sequence

To see that the `random` module is **deterministic**, give it the same
seed twice:

```python
import random

random.seed(42)
first = [random.randint(0, 99) for _ in range(5)]
random.seed(42)
second = [random.randint(0, 99) for _ in range(5)]
print(first)
print(first == second)
```

```text
[81, 14, 3, 94, 35]
True
```

The same five numbers come out on this computer and on yours. For a
simulation this is a feature: you can repeat the experiment. For security
it is the opposite: the output of a predictable generator is predictable
too. The defence is simple: a key, token, salt or password is **never**
made with `random`; leaving out the seed is not enough either, because the
generator itself is not cryptographic. These jobs are done with `secrets`.

## The `secrets` module

`secrets` is written for exactly this job and has a few short functions:

```python
import secrets

token = secrets.token_hex(16)
link = secrets.token_urlsafe(16)
print(len(token), all(c in "0123456789abcdef" for c in token))
print(len(link))
print(secrets.token_hex(16) == secrets.token_hex(16))
code = secrets.randbelow(1_000_000)
print(0 <= code < 1_000_000)
print(secrets.choice(["red", "green", "blue"]) in ["red", "green", "blue"])
```

```text
32 True
22
False
True
True
```

We printed the tokens' **properties**, not the tokens themselves, because
the values change on every run; their properties are the only thing that
can be measured.

- `token_hex(16)`: 16 random bytes, 32 characters in hex.
- `token_urlsafe(16)`: the same 16 bytes, 22 characters in a Base64 form
  that can go into a link. Both carry 128 bits; the difference in length
  comes only from the writing.
- Two separate `token_hex(16)` calls did not come out equal.
- `randbelow(n)`: a whole number from `0` to `n - 1` (for example a
  six-digit verification code).
- `choice(seq)`: one item from the sequence (for example a password
  character).

When raw bytes are needed (key, nonce, salt), use `secrets.token_bytes(n)`
or `os.urandom(n)`; both read from the same source:

```python
import os
import secrets

key = os.urandom(32)
nonce = secrets.token_bytes(12)
salt = secrets.token_bytes(16)
print(len(key) * 8, len(nonce) * 8, len(salt) * 8)
```

```text
256 96 128
```

A 256-bit key, a 96-bit nonce, a 128-bit salt: the sizes in the table
above.

## How many bits are enough?

The formula from the Passwords section works for tokens too: if the
alphabet has `a` different characters and each character is chosen
independently at random, an `n`-character token carries `n × log2(a)`
bits.

```python
import math


def entropy_bits(alphabet_size, length):
    return length * math.log2(alphabet_size)


cases = [("6 digits", 10, 6), ("16 of 62 chars", 62, 16), ("32 hex chars", 16, 32)]
for name, size, length in cases:
    print(f"{name:<15} {entropy_bits(size, length):6.1f} bits")
```

```text
6 digits          19.9 bits
16 of 62 chars    95.3 bits
32 hex chars     128.0 bits
```

16 characters from a 62-character alphabet (letters and digits) are worth
95.3 bits. A six-digit code is only 19.9 bits: that is why verification
codes are kept short-lived and the number of tries is limited.

For long-lived tokens the common target is **128 bits**: on average that
takes `2^127` tries. How many characters does an alphabet need to reach
the target?

```python
import math

for size in [10, 16, 62, 64]:
    print(size, "->", math.ceil(128 / math.log2(size)), "chars for 128 bits")
```

```text
10 -> 39 chars for 128 bits
16 -> 32 chars for 128 bits
62 -> 22 chars for 128 bits
64 -> 22 chars for 128 bits
```

The result is rounded up (`math.ceil`): with 62 characters the sum comes
out at 21.5, and 21 characters fall below the target. The 64-character
Base64 alphabet also needs 22 characters; that is where the length of
`token_urlsafe(16)` comes from.

## Modulo bias

Choosing the right source is not enough; **how you use** the random number
matters too. A byte gives every value from 0 to 255 with equal
probability. Someone who wants a number from 0 to 99 might write
`byte % 100`. Let us count every possible byte once:

```python
from collections import Counter

counts = Counter(b % 100 for b in range(256))
print("value 7: ", counts[7], "of 256")
print("value 70:", counts[70], "of 256")
print("values seen 3 times:", sum(1 for v in range(100) if counts[v] == 3))
```

```text
value 7:  3 of 256
value 70: 2 of 256
values seen 3 times: 56
```

256 is not divisible by 100: the bytes up to 200 give every result twice,
and the 56 bytes left over (200–255) give 0–55 once more. Results from
0–55 come out **one and a half times** as often as results like 70. This
is called **modulo bias**. The number is no longer evenly spread; part of
a code or key space becomes more likely than the rest.

The right way is to **throw away** the leftover part that does not divide
evenly and draw again. Let us see the rule by counting every byte again:

```python
from collections import Counter


def fair_values(n):
    limit = 256 - 256 % n
    return [b % n for b in range(256) if b < limit]


counts = Counter(fair_values(100))
print(len(counts), set(counts.values()))
print(256 - 256 % 100, "kept,", 256 % 100, "thrown away")
```

```text
100 {2}
200 kept, 56 thrown away
```

In the remaining 200 bytes every result comes out exactly twice. Do not
write this rule yourself every time: `secrets.randbelow(n)` does the same
thing correctly for you.

## Do not write your own generator

In the What Is Cryptography? section we saw that you do not write your own
encryption algorithm; the same holds here: **do not write your own random
number generator.** Taking a seed from the clock, hashing the time, mixing
a few variables or copying a formula from a textbook gives numbers that
**look** random but can be predicted. The operating system's source has
been studied for years and is used with a single call:

| Job | Use | Do not use |
|---|---|---|
| Token, session id | `secrets.token_urlsafe(32)` | `random.random()`, the clock |
| Key, nonce, salt | `secrets.token_bytes(n)`, `os.urandom(n)` | `random.randbytes(n)` |
| A number in a range | `secrets.randbelow(n)` | `byte % n`, `random.randint` |
| Picking from a list | `secrets.choice(seq)` | `random.choice(seq)` |
| Simulation, games, sampling | `random` (repeatable with a seed) | — |

`random` is not a bad module; it is just not written for security. If you
want a repeatable experiment, it is the right tool.

## Finding the wrong source in code

In code review (the Code Review and Static Analysis section of the System
Security and Operations module), one of the first things looked for is
security values made with `random`. A simple checker can search the lines
for uses of `random.`:

```python
SOURCE = """import random
import secrets
token = secrets.token_hex(16)
reset_code = random.randint(100000, 999999)
session_id = str(random.random())
color = secrets.choice(["a", "b"])
"""


def find_weak(lines):
    return [i for i, line in enumerate(lines, 1) if "random." in line]


print(find_weak(SOURCE.splitlines()))
```

```text
[4, 5]
```

The checker found that the password reset code (line 4) and the session
id (line 5) are made with `random`. Both are rewritten with `secrets`. A
search this simple also raises false alarms: `random.` in a comment line,
or the safe `random.SystemRandom`, is caught too. In the exercise you will
improve the checker enough to tell these apart.

## Summary

- What a key, nonce, salt and token share is that they **cannot be
  predicted**.
- `random` is **pseudo-random** and deterministic: the same seed gives the
  same sequence. Good for simulations, not used for security.
- For security, `secrets` (`token_hex`, `token_urlsafe`, `token_bytes`,
  `randbelow`, `choice`) or `os.urandom`.
- Entropy is `n × log2(a)` bits; the target for a long-lived token is 128
  bits, and the length is rounded up with `math.ceil`.
- `byte % n` does not spread results evenly (**modulo bias**); use
  `randbelow`.
- Do not write your own random generator; use the operating system's
  source.
