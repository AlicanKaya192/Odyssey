## Ne hash'lenebilir?

| Tür | Hash'lenir mi? | Not |
|---|---|---|
| `int`, `float`, `bool` | evet | `hash(1) == hash(1.0) == hash(True)`: eşit değerler eşit hash |
| `str` | evet | her çalıştırmada farklı tohum (süreç içinde sabit) |
| `tuple` | içi hash'lenebiliyorsa evet | `(1, [2])` hash'lenemez |
| `frozenset` | evet | kümenin değiştirilemeyen hâli; kümeler kümesi için |
| `list`, `dict`, `set` | hayır | değiştirilebilir; `TypeError: unhashable type` |
| Kendi sınıfın | varsayılan: kimliğe göre | içeriğe göre için `__eq__` + `__hash__` |

## Maliyetler

| İşlem | Ortalama | En kötü |
|---|---|---|
| `d[k]`, `k in d`, `d[k] = v`, `del d[k]` | `O(1)` | `O(n)` (her şey aynı kovaya düşerse) |
| `s.add(x)`, `x in s` | `O(1)` | `O(n)` |
| Kurmak (`set(items)`) | `O(n)` | |

## Tasarım soruları

- **Anahtar ne olmalı?** Aynı grupta olması gerekenler aynı anahtarı,
  farklılar farklı anahtarı üretmeli. Anagram için sıralı harfler; büyük-küçük
  harf farkı önemsizse `w.lower()`; iki alanlı anahtar için demet.
- **Sayı mı indeks mi saklanacak?** "Kaç kez" için sayaç; "nerede" için ilk
  ya da son indeks; "hangileri" için liste.
- **Bellek yetecek mi?** Her kalıp `O(n)` ek bellek ister. Milyarlarca
  değerde yaklaşık yapılar (Bloom filtresi, Count-Min) Algoritma Teknikleri modülünde.

## `__hash__` yazarken

```python
class Card:
    def __init__(self, rank, suit):
        self.rank, self.suit = rank, suit
    def __eq__(self, other):
        return (self.rank, self.suit) == (other.rank, other.suit)
    def __hash__(self):
        return hash((self.rank, self.suit))    # eşitlikte kullanılan alanların demeti
```

Hash'e giren alanlar sonradan **değişmemeli**: nesne sözlükteyken alanı
değişirse yanlış kovada kalır ve bulunamaz. `@dataclass(frozen=True)` bunu
kendiliğinden doğru yapar.
