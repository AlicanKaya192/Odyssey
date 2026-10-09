## Üç karşılaştırmasız sıralama

| | Sayarak (counting) | Radix | Kova (bucket) |
|---|---|---|---|
| Şart | tam sayılar, aralık `k` küçük | sabit sayıda basamak | değerler aralığa düzgün dağılmış |
| Maliyet | `O(n + k)` | `O(d × (n + taban))` | ortalama `O(n)` |
| Ek bellek | `O(k)` | `O(n + taban)` | `O(n)` |
| Kararlı mı? | sayaçla değer yazan sürüm: değer dışında bilgi taşımaz; kayıt sıralayan sürüm kararlı yazılır | her tur kararlı olmalı | kova içindeki sıralamaya bağlı |
| Örnek | sınav notu, yaş, saat (0–23) | posta kodu, telefon, tarih (YYYYMMDD) | 0–1 arası rastgele sayılar |

## Negatif değerler

Aralık `[min_value, max_value]` ise sayaç indeksini kaydır:

```python
counts = [0] * (max_value - min_value + 1)
for x in items:
    counts[x - min_value] += 1
# geri yazarken: value = index + min_value
```

## Kayıtları kararlı sıralamak (yalnızca sayı değil)

Sayılar yerine `[ad, not]` kayıtları sıralanacaksa sayaç yetmez; ya her not
için bir **kova listesi** tutulur (kovaya ekleme sırası korunur, kararlı):

```python
def sort_by_grade(records, max_grade):
    buckets = [[] for _ in range(max_grade + 1)]
    for record in records:
        buckets[record[1]].append(record)
    return [r for bucket in buckets for r in bucket]
```

ya da sayaçların **önek toplamlarıyla** her kaydın son yeri hesaplanır (bu
yöntemi Önek Toplamları bölümünde göreceğiz).

## Ne zaman karşılaştırmalı sıralamaya dön?

- Aralık `n`'den çok büyükse (`k >> n`)
- Değerler ondalıklı ya da metinse ve basamak yapısı yoksa
- Kısa bir liste sıralanıyorsa: `sorted` zaten hızlı ve tek satır
