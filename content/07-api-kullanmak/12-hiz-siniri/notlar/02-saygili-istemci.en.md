Habits for using an API smoothly, for yourself and for others.

## Send fewer requests

- **Leave filtering to the server:** `?author=Austen` needs far fewer
  requests than downloading the whole list and filtering it.
- **Ask for big pages:** raise `per_page` without going over the limit.
- **Keep the results:** do not ask for the same data five times in one day;
  get it once and write it to a file (Section 15).
- **Ask only for what changed:** if the API supports it, fetch only new
  records with parameters such as `?since=2024-03-01`.

## Set your pace

- Wait between requests as long as the limit requires.
- Go even slower for big overnight jobs; there is no hurry.
- If you send parallel requests (many at once), work out the total rate.

## Introduce yourself

- Put your program's name and a contact in the `User-Agent` header.
- If there is a problem, the API's owner can reach you instead of blocking
  you.

## Follow the rules

- Follow `Retry-After`; do not come back sooner.
- Read the API's terms of use: some APIs also limit how the data may be used
  and stored.
- Do not look for ways around the limit (several keys, hiding your identity);
  that breaks the terms and gets the key revoked.
