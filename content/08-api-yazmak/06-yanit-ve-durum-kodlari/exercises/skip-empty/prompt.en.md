The `profiles` dictionary is ready; the records also have a hidden field
called `secret_note`.

**What to do:** a `Profile` model (`name`; `bio` and `website` optional,
default `None`) and `GET /profiles/{profile_id}`. In the answer:

- no `secret_note`,
- fields whose value is `None` aren't written at all.

- `GET /profiles/1` → `{"name": "Ada", "bio": "Mathematician"}`
- `GET /profiles/2` → `{"name": "Alan", "website": "https://example.com"}`
