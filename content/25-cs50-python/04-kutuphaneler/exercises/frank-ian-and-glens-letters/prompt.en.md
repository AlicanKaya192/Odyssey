FIGlet, named after Frank, Ian and Glen's letters, is a program from the early 1990s for making large letters out of ordinary text, a form of ASCII art. It has since been ported to Python as the `pyfiglet` package.

Implement a program that:

- Expects **zero or two** command-line arguments. Zero if the user would like the text in a random font; two if in a specific font, in which case the first must be `-f` or `--font` and the second the name of the font.
- Prompts the user for a string of text.
- Outputs that text in the desired font: first `Output:`, then the drawing from the next line.

If the arguments break these rules (the first is not `-f` / `--font`, the second is not a font name, or there is the wrong number of them), the program exits via `sys.exit("Invalid usage")`. (In CS50 the file is `figlet.py`.)

Hint (from CS50): `from pyfiglet import Figlet`, `figlet = Figlet()`; `figlet.getFonts()` gives the list of fonts, `figlet.setFont(font=f)` picks one, `figlet.renderText(s)` returns the drawing as a string. `random.choice` for a random pick.

## How to test

The cases CS50 gives; Odyssey runs each one separately and compares your output. Your prompt can say anything you like; only your output is checked.

- Command `python cozum.py test` → output (nothing) (exit code 1)
- Command `python cozum.py -a slant` → output (nothing) (exit code 1)
- Command `python cozum.py -f invalid_font` → output (nothing) (exit code 1)
- Command `python cozum.py -f slant`, input `CS50` → output:

```text
Output:
   ___________ __________ 
  / ____/ ___// ____/ __ \
 / /    \__ \/___ \/ / / /
/ /___ ___/ /___/ / /_/ / 
\____//____/_____/\____/  
                          
```

- Command `python cozum.py -f rectangles`, input `Hello` → output:

```text
Output:
                   
 _____     _ _     
|  |  |___| | |___ 
|     | -_| | | . |
|__|__|___|_|_|___|
                   
```

- Command `python cozum.py --font alphabet`, input `Moo` → output:

```text
Output:
M   M         
MM MM         
M M M ooo ooo 
M   M o o o o 
M   M ooo ooo 
              
              
```

- Input `hi` → output:

```text
Output:
.%%..%%..%%%%%%.
.%%..%%....%%...
.%%%%%%....%%...
.%%..%%....%%...
.%%..%%..%%%%%%.
................
```

