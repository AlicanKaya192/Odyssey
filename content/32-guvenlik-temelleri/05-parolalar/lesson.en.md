# Passwords

The password is the oldest and still the most common authentication
method. It is cheap, works everywhere and needs no special device. Its weak
side is people: memorable passwords get guessed, unguessable ones get
forgotten. This section explains how to measure how strong a password is,
how passwords get broken and what a good password rule looks like.

## How are passwords taken?

- **Online guessing:** trying one by one on the login page. Every try goes
  to the server; limits on tries and lockouts slow this down a lot.
- **Offline guessing:** in a leak the attacker has got hold of the
  passwords' **hashes** and makes billions of tries per second on their own
  computer. There is no limit on tries at all. We will see why storing
  passwords matters so much in the next section (Storing Passwords).
- **Dictionary attack:** instead of every possibility, first trying the
  passwords real people choose. Lists compiled from leaks contain millions
  of real passwords. Rules are added to them: start with a capital letter,
  add a year at the end, write `@` instead of `a`.
- **Credential stuffing:** trying username and password pairs leaked from
  one site on other sites. Everyone who uses the same password in more than
  one place is at risk because of this.
- **Phishing and shoulder surfing:** getting the password by asking for it
  or by looking over someone's shoulder (Social Engineering section).

## A password's strength: entropy

A password's strength is decided by the question "out of how many
possibilities was it chosen?". Because this number is large, it is given in
**bits**: an `n`-bit password is one of `2^n` possibilities. This is called
**entropy**.

If the password was chosen **at random**, the calculation is easy: if the
alphabet has `a` characters and the length is `n`, there are `a^n`
possibilities and the entropy is `n × log2(a)` bits.

```python
import math

alphabets = [("digits", 10), ("lower", 26), ("letters+digits", 62), ("printable", 94)]
for name, size in alphabets:
    bits = [round(n * math.log2(size)) for n in (8, 12, 16)]
    print(f"{name:<15} {size:>3}  8:{bits[0]:>3} 12:{bits[1]:>3} 16:{bits[2]:>3}")
```

```text
digits           10  8: 27 12: 40 16: 53
lower            26  8: 38 12: 56 16: 75
letters+digits   62  8: 48 12: 71 16: 95
printable        94  8: 52 12: 79 16:105
```

Read the table across: in the same alphabet every character adds the same
number of bits. Read it down: a larger alphabet also adds bits, but fewer.
16 lower-case letters (75 bits) almost catch up with 12 characters of every
kind (79 bits). **Length gains more than complexity.**

## How many years does it take?

To find a random password you have to try, on average, half of the
possibilities: `2^(n-1)` tries. How long that takes depends on the
attacker's speed. The two speeds below are **examples**: 10 per second for
a login page with a limit on tries, ten billion per second for an offline
attack on passwords stored with a fast hash function. The real speed
depends on the hardware and on how the password is stored.

```python
def years(bits, guesses_per_second):
    seconds = 2 ** (bits - 1) / guesses_per_second
    return seconds / (365 * 24 * 3600)


for bits in [40, 60, 80]:
    print(bits, f"online {years(bits, 10):.1e}", f"offline {years(bits, 1e10):.1e}")
```

```text
40 online 1.7e+03 offline 1.7e-06
60 online 1.8e+09 offline 1.8e+00
80 online 1.9e+15 offline 1.9e+06
```

`1.7e+03` means "1.7 × 10³", about 1700 years. A 40-bit password holds out
for more than a thousand years against an online attack, but takes less
than a minute in an offline attack. 80 bits is enough in both cases. The
difference comes from how the password is stored and from the limit on
tries; both are in the defender's hands.

## Passwords that people choose

The entropy formula is only right for **random** passwords. People do not
choose at random. `Summer2024!` has eleven characters; it contains upper
case, lower case, digits and a symbol; by the formula it has 72 bits. But
the pattern "season + year + exclamation mark" is among the first things a
dictionary attack tries; its real strength is far below what the formula
says.

That is why password rules check against known and leaked passwords:

```python
common = {"123456", "password", "qwerty", "summer2024!", "iloveyou"}
for pw in ["Summer2024!", "lamp-river-cloud-tiger", "Qwerty"]:
    print(f"{pw:<23}", "common" if pw.lower() in common else "not in list")
```

```text
Summer2024!             common
lamp-river-cloud-tiger  not in list
Qwerty                  common
```

Real systems keep this list not with five passwords but with millions
compiled from leaks.

## Passphrases

A good way to get a long and memorable password is to put a few
**randomly chosen** words side by side: a **passphrase**. Every word chosen
at random from a list of 7776 words (enough to pick with five dice) adds
this many bits:

```python
import math

per_word = math.log2(7776)
print(round(per_word, 2))
for words in [4, 5, 6]:
    print(words, "words:", round(words * per_word), "bits")
```

```text
12.92
4 words: 52 bits
5 words: 65 bits
6 words: 78 bits
```

Six words give about 78 bits: as much as a completely random
13-character letters-and-digits password (77 bits), but much
easier to remember. The condition is that **randomness** chooses the words,
not you; "mymothersname-mybirthyear" is not a passphrase.

## Letting the computer make the password

In Python, random passwords are made with the **`secrets`** module, not
`random`. The numbers the `random` module produces can be predicted; it was
written for games and simulations. `secrets` uses the operating system's
secure source of randomness (the details are in the Randomness section of
the Cryptography module).

```python
import secrets
import string

alphabet = string.ascii_letters + string.digits
password = "".join(secrets.choice(alphabet) for _ in range(16))
print(len(password), all(c in alphabet for c in password))
```

```text
16 True
```

We did not write the password produced here: it is different on every
run. The output of this code only shows that the length is 16 and every
character comes from the alphabet.

## A good password rule

For many years password rules forced complexity: "at least one capital
letter, one digit, one symbol; change it every 90 days". Measurements
showed this backfired: people wrote `Password1!`, then `Password2!`.
Today's guidelines say:

| Do | Do not |
|---|---|
| Base it on length (at least 8, preferably 12+ characters) | Impose rules on required character types |
| Allow long passwords and spaces (at least 64 characters) | Cut the password at a short limit |
| Reject known and leaked passwords | Force changes at fixed intervals |
| Ask for a change only when a leak is suspected | Use hints or security questions |
| Allow pasting and password managers | Block pasting |
| Limit the number of tries | Allow unlimited tries |

A **password manager** is a program that creates a separate, long, random
password for every site and keeps them in an encrypted vault. The user
remembers one strong master password. It is the most practical solution to
the reuse problem.

## Summary

- Passwords are taken by online and offline guessing, dictionary attacks,
  trying passwords leaked from other sites, and phishing.
- A random password's entropy is `length × log2(alphabet)` bits; length
  gains the most.
- Passwords people choose are weaker than the formula says; they are
  checked against a list of known passwords.
- A passphrase made of random words is both strong and memorable.
- To make passwords use `secrets`, not `random`.
- A good rule: length, a check for leaked passwords, a limit on tries; no
  forced complexity and no regular changes.
