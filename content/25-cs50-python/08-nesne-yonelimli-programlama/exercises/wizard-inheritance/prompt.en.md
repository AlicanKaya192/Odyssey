Write three classes with inheritance:

- `Wizard(name)`: if the name is empty, `ValueError("Missing name")`; otherwise it stores it in `name`; `__str__` returns the name.
- `Student(Wizard)`: `Student(name, house)`; it leaves the name to the superclass with **`super().__init__(name)`** and stores `house` itself; `__str__` is `Harry from Gryffindor`.
- `Professor(Wizard)`: `Professor(name, subject)`; the same way, `__str__` is `Severus teaches Potions`.

The name check lives only in `Wizard`; it is not repeated in the subclasses.

Odyssey checks your class by really creating it and calling its methods; you may write test code at the end of the file.
