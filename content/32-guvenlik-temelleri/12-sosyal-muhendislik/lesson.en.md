# Social Engineering

Every control we have talked about so far locked a door: passwords, MFA,
privileges. **Social engineering** does not bother breaking the lock; it
**persuades someone inside** to open the door. Instead of a technical
vulnerability, it uses people's trust, helpfulness or haste. This is the
human side of the attack surface.

The aim of this section is to **recognise and stop** these attacks. Sending
fake e-mails to others, even as a "test" without permission, is both
unethical and a crime; organisations run phishing exercises only with
written permission and in order to protect their staff.

## Why does it work?

Social engineering uses the shortcuts people take when making decisions.
The most common levers:

| Lever | How it looks in a message |
|---|---|
| **Authority** | "Urgent instruction from the general manager" |
| **Urgency** | "Your account will be closed within 1 hour" |
| **Fear** | "There is a complaint about you, see the attached document" |
| **Curiosity** | "Salary rise list attached" |
| **Helpfulness** | "My presentation won't open, can you look right now?" |
| **Social proof** | "The rest of the team has filled in the form" |
| **Scarcity** | "Only for the first 50 people" |

What they all have in common is **leaving no time to think**. That is why
the best defence is also the simplest: stop, and check another way.

## Kinds

- **Phishing:** fake e-mail sent in bulk; the aim is a password, card
  details, or getting a harmful attachment opened.
- **Spear phishing:** a message prepared for one person or team, knowing
  their name, job and manager. Fewer of them, but far more successful.
- **Whaling:** spear phishing aimed at senior managers.
- **Smishing** (by SMS) and **vishing** (by phone): the same idea through
  another channel. "We are calling from the bank, could you read out the
  code you just received?"
- **Pretexting:** building a believable story. "I'm calling from IT, we
  are moving your account."
- **Business email compromise:** writing as a manager or a supplier and
  redirecting a payment to another account. Often there is nothing harmful
  attached, only a new bank account number.
- **Baiting:** leaving a USB stick labelled "salaries" in the car park.
- **Tailgating:** walking through a card-controlled door together with
  someone whose hands are full of boxes.
- **Shoulder surfing:** looking over someone's shoulder while they type a
  password.

## Where does the link really go?

Most phishing e-mails try to get you to click a link. A link's **visible
text** and the **address it goes to** can be different, and the address
itself can be written to mislead. `urllib.parse.urlsplit` tells which
server an address really goes to:

```python
from urllib.parse import urlsplit


def real_host(url):
    return urlsplit(url).hostname or ""


def belongs_to(url, domain):
    host = real_host(url)
    return host == domain or host.endswith("." + domain)


urls = ["https://login.school.example/reset",
        "https://school.example.account-check.test/login",
        "https://school-example.test/login",
        "https://school.example@evil.test/login"]
for url in urls:
    print(f"{real_host(url):<34}", belongs_to(url, "school.example"))
```

```text
login.school.example               True
school.example.account-check.test  False
school-example.test                False
evil.test                          False
```

All four addresses contain `school.example`, but only the first goes to the
school's server:

- In the second, `school.example` is only a **subdomain**; the real domain
  is `account-check.test` at the end. An address is read **from right to
  left**.
- In the third there is a hyphen instead of a dot; it is a different domain
  altogether.
- In the fourth, the part before the `@` sign counts as a user name; the
  server visited is `evil.test`.

It matters that `belongs_to` checks for an ending of `"." + domain`: had we
written only `endswith(domain)`, `notschool.example` would also look like
the school's.

On top of these come **lookalike domains**: `examp1e` (1 instead of l), an
`m` written as `rn`, or letters from another alphabet that look the same.
The eye misses these easily; that is why typing the address yourself or
using a bookmark is safer than clicking the link.

## Warning signs

One sign alone does not make an e-mail fake, but when signs pile up it is
time to stop and check. Organisations sometimes teach this with a simple
score:

```python
SIGNS = {"urgent": 2, "asks_password": 3, "link_mismatch": 3,
         "unknown_sender": 1, "attachment": 1}
mail = {"urgent": True, "asks_password": True, "link_mismatch": True,
        "unknown_sender": False, "attachment": False}
score = sum(points for sign, points in SIGNS.items() if mail[sign])
print("score:", score, "-> report it" if score >= 4 else "-> probably fine")
```

```text
score: 8 -> report it
```

This score is a teaching tool, not a filter: a targeted message may show
none of the signs. The real rule is: **every message that asks for a
password, a code, a payment or a change of account details is checked
through another channel.**

## Defence

No single control is enough against social engineering; defence in depth
applies here too:

- **People:** regular, short training with real examples. A culture that
  does not blame the person who made a mistake: someone who reports at
  once that they clicked has given the most valuable warning.
- **Process:** jobs such as changing a bank account are confirmed by
  calling back a registered number (not the number in the message). The
  help desk checks identity before resetting a password.
- **Technical:** e-mail filters; e-mail authentication records that verify
  the sender's domain (SPF, DKIM, DMARC); an "external sender" label on
  mail from outside; phishing-resistant MFA (so that a stolen password is
  useless on its own).
- **Reporting:** a one-click "report phishing" button. A message reported
  by one person can be removed from everyone's mailbox.

## Summary

- Social engineering targets people, not locks; with levers such as
  authority, urgency, fear and curiosity it leaves no time to think.
- Kinds: phishing, spear phishing, whaling, smishing, vishing, pretexting,
  business email compromise, baiting, tailgating, shoulder surfing.
- An address is read from right to left; `urlsplit(...).hostname` tells the
  real server. Check that it belongs to a domain with `== domain` or
  `endswith("." + domain)`.
- The rule: a sensitive request is always checked through another channel.
- Defence is people, process and technical controls working together;
  reporting a mistake is rewarded.
