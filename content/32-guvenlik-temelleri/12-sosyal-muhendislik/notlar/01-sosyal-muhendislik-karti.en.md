## Kinds

| Kind | Channel | In short |
|---|---|---|
| **Phishing** | E-mail | Fake messages in bulk |
| **Spear phishing** | E-mail | Prepared for one person |
| **Whaling** | E-mail | Aimed at senior managers |
| **Smishing** | SMS | Phishing by text message |
| **Vishing** | Phone | By voice call |
| **Pretexting** | Any channel | A believable story |
| **Business email compromise** (BEC) | E-mail | Redirecting a payment to another account |
| **Baiting** | Physical | A USB stick left behind |
| **Tailgating** | Physical | Walking through a card door behind someone |
| **Shoulder surfing** | Physical | Looking at a screen or keyboard |

## Levers

Authority, urgency, fear, curiosity, helpfulness, social proof, scarcity.
They all want the same thing: act **now**.

## Reading an address

- An address is read **from right to left**: `a.b.school.example` belongs
  to the school, `school.example.b.test` does not.
- The part before an `@` sign is not the server.
- Watch out for tricks with hyphens, dots, digits and similar letters:
  `school-example`, `examp1e`, `rn` → `m`.
- Python: `urlsplit(url).hostname`; for belonging, `host == domain or
  host.endswith("." + domain)`.

## What to do?

1. Stop: is the message rushing you?
2. Check: call the registered number, type the address yourself.
3. Report: the "report phishing" button or the security team.
4. If you clicked, say so at once: change the password, close the
   sessions.

## Layers of defence

People (training, a no-blame culture) · process (calling back, identity
checks) · technical (filters, SPF/DKIM/DMARC, external sender labels,
phishing-resistant MFA) · reporting.
