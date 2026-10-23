In an episode of *Seinfeld*, Kramer visits a bank that promises to give $100 to anyone who is not greeted with a "hello". Kramer is greeted with a "hey", insists it is not a "hello", and asks for $100. The manager proposes a compromise: "You got a greeting that starts with an 'h', how does $20 sound?" Kramer accepts.

Implement a program that prompts the user for a greeting. If the greeting starts with `hello`, output `$0`. If it starts with an `h` (but not `hello`), output `$20`. Otherwise, output `$100`. Ignore any leading whitespace and treat the greeting case-insensitively. Greetings like `hello there` and `hello, Newman` also get `$0`. (In CS50 the file is `bank.py`.)

## How to test

The cases CS50 gives; Odyssey runs each one separately and compares your output. Your prompt can say anything you like; only your output is checked.

- Input `Hello` → output `$0`
- Input `Hello, Newman` → output `$0`
- Input `How you doing?` → output `$20`
- Input `What's happening?` → output `$100`
- Input `   hey` → output `$20`
