## Three questions to tell them apart

1. **Does it spread by itself?** Yes → worm. Does it attach to a file and
   wait for a user to open it? → virus.
2. **Does it present itself as a useful program?** → trojan.
3. **What does it do?** Encrypts and asks for money → ransomware; collects
   information → spyware; records keys → keylogger; hides → rootkit;
   receives remote commands → bot.

## The kinds in one line

| Kind | One line |
|---|---|
| Virus | Needs a carrier file + a user |
| Worm | Spreads by itself over the network |
| Trojan | Gets installed by deception |
| Ransomware | Encrypts, asks for money |
| Spyware | Secretly collects information |
| Keylogger | Records the keys |
| Adware | Unwanted adverts |
| Rootkit | Hides itself |
| Backdoor | A hidden way back in |
| Bot / botnet | Remotely controlled machines |
| Cryptojacking | Steals the processor |
| Fileless malware | In memory, leaving no file |

## Detection

| Approach | Strong side | Weak side |
|---|---|---|
| Signature-based | Fast, few false alarms | Misses new kinds or kinds that change themselves |
| Behaviour-based | Catches the new | Can raise false positives |

**Indicator of compromise** (IOC): the hash of a known bad file, a
suspicious domain, an unexpected service.

## Backups

**3-2-1:** 3 copies, 2 different media, 1 somewhere else; plus at least 1
offline or immutable copy. Backups are restored and tested regularly.
