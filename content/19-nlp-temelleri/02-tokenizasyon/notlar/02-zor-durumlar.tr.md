Dersteki `TOKEN` deseni destek taleplerinde iyi çalışıyordu. Başka bir
metne götürünce ne oluyor?

```python
import re

TOKEN = re.compile(r"""
    [\w.+-]+@\w+\.\w+      # e-posta
  | \$\d+(?:\.\d+)?        # para
  | [A-Z]+-\d+             # sipariş numarası
  | \w+(?:'\w+)?           # kelime; can't tek parça
  | [^\w\s]                # tek bir noktalama işareti
""", re.VERBOSE)

for text in ["see https://example.com/help", "only $1,299.00", "on 14.03.2026",
             "state-of-the-art", "thanks :)"]:
    print("|".join(TOKEN.findall(text)))
```

```text
see|https|:|/|/|example|.|com|/|help
only|$1|,|299|.|00
on|14|.|03|.|2026
state|-|of|-|the|-|art
thanks|:|)
```

Beşi de dağıldı:

| Metin | Ne oldu | Ne yapılabilir |
|---|---|---|
| Adres (URL) | 9 parçaya bölündü | `https?://\S+` kuralını en başa koy |
| `$1,299.00` | Binlik virgülünde koptu: `$1` | Para desenine `(?:[.,]\d+)*` |
| `14.03.2026` | Beş parça | Tarih kuralı ya da tarihi yer tutucuya çevirmek |
| `state-of-the-art` | Yedi parça | Tireli kelime kuralı; ama "e-mail" ile "email" yine farklı kalır |
| `:)` | İki noktalama | Duygu analizinde ifade (emoticon) listesi |

## Ders

Bir parçalayıcı yazıldığı veriye göre iyidir. Yeni bir kaynağa geçince:

1. Rastgele 20–30 metni parçala ve elle bak.
2. Dağılan kalıpları not et (adres, tarih, para, ifade).
3. Her biri için kuralı **genel kuralların önüne** ekle.
4. Kelime dağarcığının nasıl değiştiğini ölç.

Türkçe metinde ayrıca: ondalık virgül ("3,75"), tarih biçimi (14.03.2026),
kesme işaretli ekler ("Ankara'ya"). Hazır parçalayıcılar çoğu zaman İngilizce
kurallarla gelir; Türkçe veride mutlaka dene.
