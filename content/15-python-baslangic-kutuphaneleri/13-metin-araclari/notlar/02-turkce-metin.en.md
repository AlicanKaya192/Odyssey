Python's text operations **know no language**: they follow Unicode's general
rules. That is enough for English; for Turkish it falls short in two places:
upper/lower case and alphabetical order.

## Sorting

```python
words = ["çay", "zeytin", "ıhlamur", "ispanak", "elma", "şeker", "Üzüm", "armut"]
print(sorted(words))
ALPHABET = "abcçdefgğhıijklmnoöprsştuüvyz"


def tr_key(word):
    lowered = word.replace("I", "ı").replace("İ", "i").lower()
    return [ALPHABET.find(ch) for ch in lowered]


print(sorted(words, key=tr_key))
print("ILIK".lower(), "ILIK".replace("I", "ı").lower())
```

```text
['armut', 'elma', 'ispanak', 'zeytin', 'Üzüm', 'çay', 'ıhlamur', 'şeker']
['armut', 'çay', 'elma', 'ıhlamur', 'ispanak', 'şeker', 'Üzüm', 'zeytin']
ilik ılık
```

- `sorted` orders letters by their **Unicode numbers**: `ç`, `ı`, `ş`, `Ü`
  come after all English letters, and uppercase before lowercase (`Üzüm`
  before `çay`). The result looks jumbled to a Turkish reader.
- **Your own sort key:** write the alphabet as a string and use each letter's
  position in it (`find`) as the key. The function given with `key=` is
  called once per word, and the lists of numbers are compared.
- The key starts with a Turkish lowercase conversion: first `I` → `ı`,
  `İ` → `i`, then `lower()`. `lower()` alone turned `ILIK` into `ilik`.

The `locale` module, which uses the operating system's language setting, can
sort Turkish too, but the result depends on the settings of the computer the
program runs on; the key above gives the same result on every computer.

## "Folding" for search

A user typing `sisli` on an English keyboard should be able to find `Şişli`.
For that you **fold** both texts to the same plain form: lowercase, no
accents, `ı` → `i`.

```python
import unicodedata


def fold(text):
    text = text.replace("I", "ı").replace("İ", "i").lower().replace("ı", "i")
    decomposed = unicodedata.normalize("NFD", text)
    return "".join(ch for ch in decomposed if unicodedata.category(ch) != "Mn")


places = ["Şişli", "Kadıköy", "Üsküdar", "Beşiktaş", "IĞDIR"]
query = "sisli"
print([p for p in places if fold(query) in fold(p)])
print([fold(p) for p in places])
```

```text
['Şişli']
['sisli', 'kadikoy', 'uskudar', 'besiktas', 'igdir']
```

First the Turkish lowercase, then `ı` → `i`, then dropping accents with NFD.
This is what search boxes do (this program's `Ctrl+K` search too): the query
and the searched text are brought to the same form and compared, while the
user is shown the original text.

## Checklist

- Turkish lowercase: first `I` → `ı`, `İ` → `i`, then `lower()`.
- Turkish uppercase: first `i` → `İ`, `ı` → `I`, then `upper()`.
- Your own key function for alphabetical order.
- Fold both sides when searching; show the original text on screen.
