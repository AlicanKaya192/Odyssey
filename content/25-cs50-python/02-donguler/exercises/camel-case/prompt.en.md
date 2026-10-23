In some languages, variable names made of several words are written in **camel case**: the first letter of the first word is lowercase and the first letter of each later word is uppercase: `name`, `firstName`, `preferredFirstName`. Python instead recommends **snake case**: words separated by underscores, all lowercase: `name`, `first_name`, `preferred_first_name`.

Implement a program that prompts the user for the name of a variable in camel case and outputs the corresponding name in snake case. Assume the input will indeed be in camel case. (In CS50 the file is `camel.py`.)

Hint (from CS50): you can go over a string letter by letter with `for c in s:`; `c.isupper()` is `True` if the letter is uppercase.

## How to test

The cases CS50 gives; Odyssey runs each one separately and compares your output. Your prompt can say anything you like; only your output is checked.

- Input `name` → output `name`
- Input `firstName` → output `first_name`
- Input `preferredFirstName` → output `preferred_first_name`
- Input `isHttpRequestOk` → output `is_http_request_ok`
