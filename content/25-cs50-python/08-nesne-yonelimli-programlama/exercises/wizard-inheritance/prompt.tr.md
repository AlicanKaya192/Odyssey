Kalıtımla üç sınıf yaz:

- `Wizard(name)`: ad boşsa `ValueError("Missing name")`, değilse `name`'de saklar; `__str__` adı döndürür.
- `Student(Wizard)`: `Student(name, house)`; adı **`super().__init__(name)`** ile üst sınıfa bırakır, `house`'u kendisi saklar; `__str__` `Harry from Gryffindor`.
- `Professor(Wizard)`: `Professor(name, subject)`; aynı şekilde, `__str__` `Severus teaches Potions`.

Ad denetimi yalnızca `Wizard`'da olsun; alt sınıflarda tekrarlanmasın.

Odyssey sınıfını gerçekten kurup metotlarını çağırarak denetliyor; dosyanın sonunda deneme kodu yazabilirsin.
