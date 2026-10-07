The file `users.json` has been placed next to your code: a list of users.
Some of them have **no** `email` field, some have no `age`.

**What to do:**

1. Read the file into a list called `users`.
2. For each user, print the name and the email; if there is no email, write
   `-` instead.
3. Count the users without an email in the variable `no_email`.
4. Work out the mean age of the users who **have** an age, with **integer
   division**, in the variable `average_age`.
5. Print `no_email` and `average_age`, in order.

**Expected output:**

```text
Ada ada@example.com
Alan -
Grace grace@example.com
Linus linus@example.com
Margaret -
2
35
```

If you ask for a missing field with square brackets you get a `KeyError`.
The second argument of `get` is what comes back when the field is missing;
without it, `None` comes back.
