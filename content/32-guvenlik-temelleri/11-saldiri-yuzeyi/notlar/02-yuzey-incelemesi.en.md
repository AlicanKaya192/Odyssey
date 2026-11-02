A step-by-step way to review the attack surface of a web application. You
do this on a system you wrote or are responsible for; scanning someone
else's system without permission is unethical and unlawful (Ethics and Law
section).

## 1. Make the list

Gather it from several sources, do not rely on just one:

- The application's own route definitions.
- The services open in the server and network settings.
- The addresses seen in the last three months of access logs.
- The ones the team knows about but that are not in the code (old servers,
  test environments).

An address that shows up in the logs but not in the code is a door someone
forgot or opened without telling anyone.

## 2. Fill in every row

| Entry point | Who reaches it? | Login required? | What does it take? | Is it used? | Owner |
|---|---|---|---|---|---|
| `/login` | Internet | No (login page) | Username, password | A lot | Ayşe |
| `/search` | Internet | No | Search text | Some | Can |
| `/admin` | Internet | Yes | Everything | Little | Ayşe |
| `/legacy-upload` | Internet | Yes | A file | Never | Unknown |

## 3. Decide

- **Not used and no owner:** remove it (`/legacy-upload`).
- **Rarely used but powerful:** narrow who can reach it (`/admin` →
  internal network only).
- **No login and takes outside data:** input validation and rate limiting
  come first (`/search`, `/login`).

## 4. Repeat

A review is not done once and finished. In every release the list of new
endpoints is drawn up, and every quarter it is compared with the logs.
When the difference list is small, the review is short too.
