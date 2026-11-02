# Authentication and MFA

When you log in to a system, you first say who you are, then you prove it.
Only after that does the system decide what you may do. These three steps
are often confused, but each one is a separate job and each one has its own
weaknesses.

<figure class="fig"><div class="flow">
  <span class="node">Identification</span><span class="arrow">→</span>
  <span class="node acc">Authentication</span><span class="arrow">→</span>
  <span class="node">Authorization</span><span class="arrow">→</span>
  <span class="node">Accounting</span>
</div><figcaption>"I am Ada" → "here is the proof" → "Ada may see the grades" → "Ada looked at the grades at 10:05".</figcaption></figure>

- **Identification:** **saying** who you are. A username, an e-mail
  address, a student number. Anyone can type any name; identification on
  its own proves nothing.
- **Authentication:** **proving** what you said. A password, a code on
  your phone, a fingerprint.
- **Authorization:** deciding **what** the authenticated person **may do**.
  It has its own sections (Authorization, Access Control Models).
- **Accounting:** writing down who did what; the basis of accountability.

This section is about the second step, authentication.

## Three kinds of proof: factors

There are three basic ways to prove who you are. Each one is called a
**factor**:

| Factor | Question | Examples | Weak side |
|---|---|---|---|
| **Knowledge** (something you know) | What do you know? | Password, PIN, security question | Guessed, stolen, already used on another site |
| **Possession** (something you have) | What do you have? | Phone, code-generating app, hardware key | Lost, stolen |
| **Inherence** (something you are) | What are you? | Fingerprint, face, voice | Cannot be changed; if it leaks there is no new one |

Biometric authentication has its own problem: it is not perfect. Sometimes
it accepts a stranger (**false accept**), sometimes it rejects the owner
(**false reject**). Lowering one raises the other. Also, a leaked password
can be changed; a fingerprint cannot. That is why biometrics are usually
used for local jobs such as unlocking a device, and together with another
factor rather than alone.

## Multi-factor authentication

**Multi-factor authentication** (MFA) means asking for at least two
factors **of different kinds**. With two factors it is also called **2FA**.
The important word is "different": asking for two passwords is not MFA,
because the same attack (for example a fake login page) can steal both. A
password and a phone need separate attacks.

```python
FACTORS = {"password": "know", "pin": "know", "sms_code": "have",
           "app_code": "have", "security_key": "have", "fingerprint": "are"}

for methods in [["password"], ["password", "pin"], ["password", "app_code"],
                ["security_key", "fingerprint"]]:
    kinds = {FACTORS[m] for m in methods}
    print(methods, "MFA" if len(kinds) >= 2 else "not MFA")
```

```text
['password'] not MFA
['password', 'pin'] not MFA
['password', 'app_code'] MFA
['security_key', 'fingerprint'] MFA
```

`kinds` is a set: adding the same kind a second time does not make the set
bigger. A password and a PIN are two different methods, but both are
"knowledge"; the set stayed at one element.

## How are one-time codes produced?

Code-generating apps on phones show a six-digit code that changes every 30
seconds. These codes are produced even without an internet connection. How
does the server know the same code? When the account is set up, the server
and the phone share a common **secret**. After that, both do the same
calculation.

This method is called **HOTP** (HMAC-based one-time password). HMAC is a
construction that produces a fixed-length value from a secret and a
message; we will see it in detail in the Cryptography module. Here let us
look at its steps. The secret is the standard's own test value:

```python
import hashlib
import hmac

secret = b"12345678901234567890"
counter = 0
digest = hmac.new(secret, counter.to_bytes(8, "big"), hashlib.sha1).digest()
offset = digest[-1] & 0x0F
number = int.from_bytes(digest[offset:offset + 4], "big") & 0x7FFFFFFF
print("digest bytes:", len(digest))
print("offset:", offset)
print("code:", str(number % 10**6).zfill(6))
```

```text
digest bytes: 20
offset: 0
code: 755224
```

Step by step:

1. The counter is turned into an 8-byte number and put through HMAC
   together with the secret; a 20-byte result comes out.
2. The last 4 bits of the last byte (`& 0x0F`) give a **position** between
   0 and 15. The 4 bytes starting at that position are taken; this is
   called "dynamic truncation".
3. Those 4 bytes are turned into a number, the top bit is dropped
   (`& 0x7FFFFFFF`) and the last six digits are taken. A code can start
   with `0`; `zfill(6)` keeps the leading zeros.

This code is the same as the value the standard gives for counter 0:
`755224`.

**TOTP** (time-based one-time password) is the same calculation with one
difference: the clock is used as the counter. The time (seconds since 1970)
is divided by 30 and the whole part is taken; so the counter goes up every
30 seconds:

```python
for seconds in [0, 29, 30, 59, 60]:
    print(seconds, "->", seconds // 30)
```

```text
0 -> 0
29 -> 0
30 -> 1
59 -> 1
60 -> 2
```

The phone's clock and the server's clock may differ a little. That is why
servers often also accept the code of the previous and the next step.

## Short codes need limited tries

A six-digit code has a million possible values. That does not look small,
but it becomes a problem if an attacker can try without limit. Trying for a
whole day against a system that allows 5 tries in every 30-second window:

```python
codes = 10**6
tries_per_window = 5
windows_per_day = 24 * 60 * 2
miss_all = (1 - tries_per_window / codes) ** windows_per_day
print(f"one day:  {1 - miss_all:.4f}")
print(f"one year: {1 - miss_all ** 365:.4f}")
```

```text
one day:  0.0143
one year: 0.9948
```

A little over one per cent in a day, but almost certain in a year. A code's
strength only means something together with a control that limits the
number of tries: **locking out** after a number of wrong tries in a row, or
slowing down (rate limiting).

Locking out has a price too: an attacker can deliberately try wrong codes
and lock the real user out (which is an availability attack). That is why,
instead of a permanent lock, waiting times that grow longer and longer are
often used.

## MFA can be bypassed too

MFA makes taking over an account much harder, but it is not magic:

- **Real-time phishing:** a fake login page takes both the password and
  the code and forwards them to the real site at once. The code is valid
  for 30 seconds, which is enough time.
- **SMS codes:** a phone number can be moved to another SIM card (SIM
  swap); the codes then go to the attacker.
- **MFA fatigue:** "approve this login?" notifications are sent to the
  phone again and again; a user who is fed up finally presses "approve".

The strongest answer to these is **phishing-resistant** authentication:
methods such as hardware keys do not show a code to the user, and they
include the address of the site being logged in to in the calculation. An
answer produced on a fake site is useless on the real one.

## The weak link: recovery

Someone who forgets their password or loses their phone must be able to
get back into their account. But if the **account recovery** path is
weaker than the login door, the attacker uses that path. Security questions
such as your mother's maiden name can often be found on social media. Good
recovery paths: **backup codes** given when the account is opened and kept
in a safe place, a second registered device, or checking identity in
person.

## Summary

- **Identification** is saying, **authentication** is proving,
  **authorization** is allowing.
- Three factors: **knowledge**, **possession**, **inherence**. MFA needs at
  least two **different** factors; two passwords are not MFA.
- HOTP/TOTP codes are made with HMAC from a shared secret and a counter (or
  the clock).
- Short codes are only strong when tries are limited; lockouts must be
  measured.
- MFA can be phished; phishing-resistant methods are the strongest. The
  recovery path must be as strong as the login.
