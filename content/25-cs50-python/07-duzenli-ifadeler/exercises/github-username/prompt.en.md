Ask the user for the address of their GitHub profile and extract the username: `Username: octocat`. The address may start with `https://` or `http://` or have no protocol, may or may not have `www.`, and case does not matter. A username is made of letters, digits and hyphens; a `/` or `?tab=...` after it is not part of the username. If the address is not a GitHub profile (another site, or inside a sentence), print `Not a GitHub profile`.

Example run (the prompt can say anything you like; only your output is checked):

```text
$ python cozum.py
URL: https://github.com/davidjmalan
Username: davidjmalan
```
