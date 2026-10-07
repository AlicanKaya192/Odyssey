The signup API in `main.py` is ready (read-only): it lower-cases the email,
gives `409` for the same email, `422` for under 13, and `201` on success.

**What to do:** tests that try all of these behaviours (at least 4). They'll
be run against four broken versions: at least one must fail in each.
