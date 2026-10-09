Sözde kodun tek bir standardı yok; kitaplar ve mülakatlar farklı yazar.
Bu patikada kullandığımız yazım ve Python karşılıkları:

| Sözde kod | Python |
|---|---|
| `x ← 5` | `x = 5` |
| `listedeki her a için:` | `for a in items:` |
| `i ← 0'dan n-1'e kadar:` | `for i in range(n):` |
| `eğer a > b ise: … değilse: …` | `if a > b: … else: …` |
| `koşul doğru olduğu sürece:` | `while condition:` |
| `sonuç: x` | `return x` |
| `liste[i]` | `items[i]` (ilk eleman `0`) |
| `uzunluk(liste)` | `len(items)` |
| `boş liste` | `[]` |

## Bir örnek: ilk tekrar eden harf

Problem: bir kelimede **ilk tekrar eden** harfi bul; yoksa `None`.

Elle: "banana" → b (ilk kez), a (ilk kez), n (ilk kez), a (**gördüm!**) →
cevap `a`.

Sözde kod:

```text
görülen ← boş küme
kelimedeki her harf için:
    eğer harf görülen içinde ise:
        sonuç: harf
    görülene harfi ekle
sonuç: yok
```

Python:

```python
def first_repeated(word):
    seen = set()
    for letter in word:
        if letter in seen:
            return letter
        seen.add(letter)
    return None
```

Dikkat: sözde koddaki iki `sonuç:` satırı Python'da iki ayrı `return` oldu.
İlki döngünün **içinde**, cevabı bulur bulmaz çıkıyor; ikincisi döngü hiç
cevap bulamadan bittiğinde çalışıyor.

## Sözde kodu ne zaman atlayabilirsin?

Problem küçükse doğrudan Python yazmak sorun değil. Ama şu durumlarda önce
sözde kod yaz:

- Birden fazla iç içe döngü ya da koşul varsa,
- Bir mülakatta, kodu yazmadan önce fikrini anlatman bekleniyorsa,
- Algoritmayı başkasına (ya da üç ay sonraki kendine) açıklaman gerekecekse.
