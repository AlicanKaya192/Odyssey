Dört kalıp; dördünde de işaretçiler **geri gitmez**, bu yüzden toplam iş
`O(n)`.

## 1. İki uçtan içeri (sıralı liste)

```text
left, right = 0, len(items) - 1
while left < right:
    if şart sağlandı:
        return ...
    if daha büyük bir şey lazım:
        left += 1
    else:
        right -= 1
```

Örnekler: toplamı `target` olan ikili, palindrom denetimi (iki uçtaki
harfler eşit mi?), en çok su tutan iki duvar.

## 2. Hızlı ve yavaş (aynı yön)

```text
slow = 0
for fast in range(len(items)):
    if items[fast] tutulacaksa:
        items[slow] = items[fast]
        slow += 1
# items[:slow] sonuç
```

Örnekler: sıralı listede tekrarları atmak, sıfırları sona taşımak, belli bir
değeri silmek; hepsi yerinde, `O(1)` ek bellek.

## 3. Sabit pencere

```text
total = sum(values[:k])
for i in range(k, len(values)):
    total += values[i] - values[i - k]     # giren - çıkan
```

Örnekler: hareketli ortalama, `k` günlük en büyük toplam, son `k` olayda
eşik aşımı.

## 4. Değişken pencere

```text
start = 0
for end in range(len(items)):
    items[end]'i pencereye ekle
    while pencere şartı bozuyor:
        items[start]'ı pencereden çıkar
        start += 1
    cevabı end - start + 1 ile güncelle
```

Örnekler: tekrarsız en uzun parça, toplamı en az `target` olan en kısa parça,
en fazla `k` farklı değer içeren en uzun parça.

## Kontrol soruları

- **Sıralı mı?** Değilse iki uçtan işaretçi yanlış çalışır.
- **Değerler negatif olabilir mi?** "Toplamı en az `target`" gibi değişken
  pencere problemlerinde pencereyi küçültmek toplamı azaltır varsayımı
  yalnızca **negatif olmayan** sayılarda doğru. Negatif sayılarla önek
  toplamları (bir sonraki bölüm) gerekir.
- **Boş girdi ve `k > n`?** Pencere hiç kurulamıyorsa ne döneceğine karar ver.
