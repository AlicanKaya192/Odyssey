Apply the Social Engineering section. Each e-mail has `id`, `from` and
the optional fields `links`, `urgent`, `asks_password`. `belongs` is ready.

`triage_mail(mails, domain, threshold)` should score every e-mail:

- +3 if the sender's domain after `@` does not belong to `domain`,
- +2 (once) if at least one link's host (`urlsplit(url).hostname`) does not
  belong to `domain`,
- +2 if `urgent`, +3 if `asks_password`.

Return those with a score equal to or greater than `threshold` as
`[id, score]`, by score from high to low, ties in `id` order.

**Expected output:**

```
m2 10
m4 5
```
