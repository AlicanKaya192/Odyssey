Alıştırmanın klasöründe bir modül hazır duruyor, `shapes.py`:

```python
def square(n):
    return n * n


def cube(n):
    return n * n * n
```

Ondan `square` ve `cube`'u içe aktar (`from shapes import ...`). Komut satırından tam bir tam sayı al ve karesini ve küpünü aynı satıra yaz. Argüman sayısı yanlışsa `sys.exit("Usage: python cozum.py NUMBER")`.

Örnek çalıştırma (soru metnini istediğin gibi yazabilirsin, yalnızca çıktın denetlenir):

```text
$ python cozum.py 3
9 27
```
