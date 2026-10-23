As you saw in the lesson, validating email addresses with your own pattern is hard. This time leave the job to a popular library: `validators` (installed in Odyssey). `response.py` asks the user for an email address (removing leading and trailing spaces) and prints `Valid` if it is valid, otherwise `Invalid`. `validators.email(address)` returns `True` for a valid address and an error object that counts as false for an invalid one; you can ask with `if`. Do not write your own regular expression; you do not need `re`.

Example run (the prompt can say anything you like; only your output is checked):

```text
$ python cozum.py
Email: malan@harvard.edu
Valid
```

## How to test

- Input `malan@harvard.edu` → output `Valid`
- Input `  malan@cs50.harvard.edu ` → output `Valid`
- Input `malan@@@harvard.edu` → output `Invalid`
- Input `malan@harvard` → output `Invalid`
- Input `malan.harvard.edu` → output `Invalid`
