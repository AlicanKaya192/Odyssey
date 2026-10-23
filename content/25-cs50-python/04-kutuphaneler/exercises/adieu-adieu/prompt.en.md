In *The Sound of Music* there is a song, *So Long, Farewell*, in which the children say goodbye in turn; "adieu" means "goodbye" in French.

Implement a program that prompts the user for names, one per line, until the user ends the input (`Ctrl+D`, `EOFError`); assume there will be at least one name. Then bid adieu to those names, joining two names with one `and`, three names with two commas and one `and`, and `n` names with `n - 1` commas and one `and`:

- `Adieu, adieu, to Liesl`
- `Adieu, adieu, to Liesl and Friedrich`
- `Adieu, adieu, to Liesl, Friedrich, and Louisa`

(In CS50 the file is `adieu.py`.)

Hint (from CS50): the `inflect` package does this: `p = inflect.engine()`, `p.join(names)`.

## How to test

The cases CS50 gives; Odyssey runs each one separately and compares your output. Your prompt can say anything you like; only your output is checked.

- Input `Liesl` → output `Adieu, adieu, to Liesl`
- Input `Liesl`, `Friedrich` → output `Adieu, adieu, to Liesl and Friedrich`
- Input `Liesl`, `Friedrich`, `Louisa` → output `Adieu, adieu, to Liesl, Friedrich, and Louisa`
- Input `Liesl`, `Friedrich`, `Louisa`, `Kurt`, `Brigitta`, `Marta`, `Gretl` → output `Adieu, adieu, to Liesl, Friedrich, Louisa, Kurt, Brigitta, Marta, and Gretl`
