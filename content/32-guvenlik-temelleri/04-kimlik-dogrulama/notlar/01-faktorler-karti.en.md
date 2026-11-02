## Four steps

| Step | Question | Example |
|---|---|---|
| **Identification** | Who do they say they are? | A username |
| **Authentication** | Do they prove it? | Password + a code on the phone |
| **Authorization** | What may they do? | May see the grades, may not change them |
| **Accounting** | What did they do? | "Looked at the grades at 10:05" |

## Factors

| Factor | Example | Watch out |
|---|---|---|
| **Knowledge** (know) | Password, PIN | May have been reused on other sites |
| **Possession** (have) | Code app, hardware key, SMS | SMS is the weakest (SIM swap) |
| **Inherence** (are) | Fingerprint, face | Cannot be changed; false accept / false reject |

**MFA = at least two different factors.** Password + PIN is not MFA;
password + hardware key is MFA.

## How strong the methods are (weakest to strongest)

1. Password only
2. Password + SMS code
3. Password + a one-time code from an app (TOTP) or a push approval
4. Password + a phishing-resistant method (such as a hardware key)

## The parts of TOTP

- A shared **secret**: shared once when the account is set up, never sent
  again.
- The **counter**: `time // 30`.
- **HMAC-SHA1** → dynamic truncation → `% 10**6` → `zfill(6)`.
- Against clock drift the server may also accept the previous and the next
  step.

## Attacks and answers

| Attack | Answer |
|---|---|
| Guessing the code | A limit on tries, growing wait times |
| Real-time phishing | Phishing-resistant authentication |
| SIM swap | An app or a hardware key instead of SMS |
| MFA fatigue | Typing the number shown on screen into the phone, a limit on notifications |
| A weak recovery path | Backup codes, a second device |
