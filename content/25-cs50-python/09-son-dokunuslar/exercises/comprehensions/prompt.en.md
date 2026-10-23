Write three short functions; each can be a single `return` line:

- `shout(*words)`: takes any number of words and returns their uppercase forms as a **list** (`map` or a list comprehension)
- `gryffindors(students)`: from dictionaries with the keys `name` and `house`, returns the names of only those whose house is `Gryffindor`, in alphabetical order
- `ranks(names)`: returns a dictionary giving each name its position, starting from **1**: `ranks(["Hermione", "Harry"])` → `{"Hermione": 1, "Harry": 2}`. Write it with a **dictionary comprehension** and `enumerate`.

Odyssey calls your functions with different inputs and checks what they return.
