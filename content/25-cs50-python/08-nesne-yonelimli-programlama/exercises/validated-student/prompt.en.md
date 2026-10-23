Write the lesson's `Student` class: the constructor takes a name and a house. If the name is empty it raises `ValueError("Missing name")`; if the house is not one of `Gryffindor`, `Hufflepuff`, `Ravenclaw`, `Slytherin`, it raises `ValueError("Invalid house")`; otherwise it stores both. `__str__` returns `Harry from Gryffindor`. The program asks for the name and house and prints the student; with invalid input it does not catch the error, and the program ends with it.

Example run (the prompt can say anything you like; only your output is checked):

```text
$ python cozum.py
Name: Harry
House: Gryffindor
Harry from Gryffindor
```
