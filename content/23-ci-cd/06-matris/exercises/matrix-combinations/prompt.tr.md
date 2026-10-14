`combinations(matrix)` fonksiyonunu yaz. Matrisin bütün birleşimlerini, her biri bir sözlük olarak, bir listede döndürsün. `itertools` kullanma.

Sıra GitHub'daki gibi: ilk anahtar en dışta. `{"os": [A, B], "python": [X, Y]}` için:

- `{"os": A, "python": X}`, `{"os": A, "python": Y}`, `{"os": B, "python": X}`, `{"os": B, "python": Y}`

Fikir: `[{}]` (tek, boş birleşim) ile başla. Her anahtarda, eldeki her birleşimi o anahtarın her değeriyle genişlet.

**Beklenen çıktı:**

```
{'os': 'ubuntu-latest', 'python': '3.12'}
{'os': 'ubuntu-latest', 'python': '3.13'}
{'os': 'windows-latest', 'python': '3.12'}
{'os': 'windows-latest', 'python': '3.13'}
12
```
