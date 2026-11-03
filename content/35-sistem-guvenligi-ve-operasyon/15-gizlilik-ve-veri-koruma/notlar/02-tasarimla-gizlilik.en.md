Privacy is not a setting added after a product is finished but a design
decision made from the start. This is called **privacy by design** and
**privacy by default**. It is the privacy counterpart of the secure
defaults from the Secure Software Development section.

## Questions to ask in design

| Question | Why? |
|---|---|
| Why are we collecting this data? | Data with no purpose is not collected |
| Would less do? | Instead of a birth date, is "is the person over 18?" enough? |
| How long will we keep it? | The period is written down from the start |
| Who will have access? | Least privilege |
| Will it be shared with anyone else? | A contract with the processor, information to the person |
| What will we do if the person wants to see or erase their data? | The inventory and the erasure path must be ready |

## Privacy by default

If a setting is left to the user, its default value is the **most
private** one: a profile starts closed, not public; optional data sharing
is off; location is used only if the person turns it on. The person can
knowingly turn more on; but the person who does nothing is protected.

## Data protection impact assessment

High-risk work (health data of many people, continuous location tracking,
automated decisions) goes through a **data protection impact assessment**
before it starts: which data, which risk, which measure. It is the
threat modelling from the Threat Modelling and STRIDE section, done from
the point of view of people.

## Logs and personal data

The logs we saw in the Logging and Monitoring section contain personal
data too: IP addresses, user names, who entered where and when. That is why
logs are purpose-limited too, have retention periods and access to them is
limited with least privilege. Using logs kept for security for another
purpose (such as monitoring employees) goes against purpose limitation.

## Transfers across borders

A cloud service may mean data being stored in another country. Transferring
personal data abroad is subject to extra conditions under both KVKK and the
GDPR. That is why choosing a provider in the Cloud Security section is not
only a technical decision but a legal one too.
