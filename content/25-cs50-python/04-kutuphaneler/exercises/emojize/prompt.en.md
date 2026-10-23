Because emoji are not as easy to type as text, at least on laptops and desktops, some programs support **codes**: typing `:thumbs_up:` gives 👍. Some also support shorter **aliases**: `:thumbsup:` is 👍 too.

Implement a program that prompts the user for a string in English and outputs the "emojized" version as `Output: ...`, converting any codes (or aliases) in it to their emoji. (In CS50 the file is `emojize.py`.)

Hint (from CS50): the `emoji` package's `emojize` function does the job; aliases need the argument `language="alias"`.

## How to test

The cases CS50 gives; Odyssey runs each one separately and compares your output. Your prompt can say anything you like; only your output is checked.

- Input `:1st_place_medal:` → output `Output: 🥇`
- Input `:money_bag:` → output `Output: 💰`
- Input `:smile_cat:` → output `Output: 😸`
- Input `hello, :earth_africa:` → output `Output: hello, 🌍`
- Input `I :thumbsup: it` → output `Output: I 👍 it`
