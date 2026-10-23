Ask the user for an email address and validate it with the lesson's final pattern: a username of word characters (`\w`), `@`, an optional subdomain (like `cs50.`), a domain and a literal `.edu` at the end. Case should not matter, and leading and trailing spaces should be removed. Print `Valid` or `Invalid`.

Example run (the prompt can say anything you like; only your output is checked):

```text
$ python cozum.py
What's your email? malan@harvard.edu
Valid
```
