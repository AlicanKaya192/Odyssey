Ask the user for a time in 24-hour form (`09:30`) and validate it with `re.fullmatch`: two-digit hours, `00`–`23`; two-digit minutes, `00`–`59`. Print `Valid` or `Invalid`. `9:30` is invalid (the hour must have two digits).

Example run (the prompt can say anything you like; only your output is checked):

```text
$ python cozum.py
Time: 09:30
Valid
```
