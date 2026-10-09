# Sayarak Sıralama

Bir önceki bölümde, karşılaştırarak sıralayan hiçbir algoritmanın en kötü
durumda `n log n`'den iyi yapamayacağını gördük. Bu sınırın bir şartı var:
**karşılaştırmak**. Elemanları birbirleriyle karşılaştırmadan, değerlerine
bakarak doğrudan yerlerine koyabilirsek `O(n)`'e inebiliriz. Bunun için
verinin bir özelliği gerekiyor: değerlerin **küçük bir aralıkta** olması ya
da **basamaklara** ayrılabilmesi.

## Sayarak sıralama (counting sort)

Bir sınıfın sınav notlarını (0–100) sıraladığını düşün. Notları birbirleriyle
karşılaştırmana gerek yok: 101 kutu aç, her nota bakıp kendi kutusuna bir
çentik at. Sonra kutuları 0'dan 100'e kadar sırayla gez ve her nottan kaç
çentik varsa o kadar yaz.

```python
def counting_sort(items, max_value):
    counts = [0] * (max_value + 1)      # her değer için bir sayaç
    for x in items:
        counts[x] += 1
    print(counts)
    result = []
    for value, count in enumerate(counts):
        result.extend([value] * count)  # değeri, sayısı kadar yaz
    return result

print(counting_sort([4, 1, 3, 4, 0, 1, 4], 4))
```

```text
[1, 2, 0, 1, 3]
[0, 1, 1, 3, 4, 4, 4]
```

İlk satır sayaçlar: 0'dan 1 tane, 1'den 2 tane, 2'den hiç, 3'ten 1, 4'ten 3.
Hiçbir karşılaştırma yapılmadı.

**Maliyet:** elemanları bir kez gez (`n`), sayaçları bir kez gez (`k`, değer
aralığının büyüklüğü): `O(n + k)`. Ek bellek `O(k)`.

Gerçekten hızlı mı? Bir milyon kişinin yaşını (0–100) sıraladık:

```text
same result  : True
counting_sort: 54 ms
sorted       : 107 ms
```

Python ile yazılmış sayarak sıralama, C ile yazılmış `sorted`'dan bile hızlı
çıktı ve sonuçlar aynı. Değer aralığı küçükken karşılaştırmamak gerçekten
kazandırıyor.

## Ne zaman işe yaramaz?

`k` büyükse sayarak sıralama kötüleşir. Değerler 0 ile bir milyar arasındaysa
bir milyarlık sayaç listesi gerekir: hem bellek hem süre `n`'den çok büyük
olur. Değerler negatifse kaydırmak gerekir (`x - min_value`), ondalıklı
sayılarda ise doğrudan kullanılamaz.

<figure class="fig">
  <div class="versus">
    <div class="ok"><h4>Sayarak sıralama uygun</h4>
      <p>Sınav notu (0–100), yaş, ay (1–12), saat (0–23)</p>
      <p>Aralık <code>k</code> küçük; <code>O(n + k)</code> ≈ <code>O(n)</code></p></div>
    <div class="no"><h4>Uygun değil</h4>
      <p>Maaş, nüfus, kimlik numarası, ondalıklı ölçüm</p>
      <p>Aralık devasa ya da değer tam sayı değil; karşılaştırmalı sıralama</p></div>
  </div>
  <figcaption>Karar sorusu: değerlerin alabileceği farklı sonuç sayısı, eleman sayısına göre küçük mü?</figcaption>
</figure>

## Radix sort: basamak basamak

Değerler büyük ama **basamaklara** ayrılabiliyorsa (telefon numaraları,
posta kodları, tarihler) **radix sort** işe yarar. Fikir: önce **birler**
basamağına göre, sonra **onlar**, sonra **yüzler** basamağına göre sırala. Her
turda 10 kovaya (0–9) dağıt ve kovaları sırayla topla.

```python
def radix_sort(items):
    place = 1
    largest = max(items)
    while largest // place > 0:
        buckets = [[] for _ in range(10)]
        for x in items:
            buckets[(x // place) % 10].append(x)   # o basamağın rakamı
        items = [x for bucket in buckets for x in bucket]
        print(place, items)
        place *= 10
    return items

radix_sort([170, 45, 75, 90, 802, 24, 2, 66])
```

```text
1 [170, 90, 802, 2, 24, 45, 75, 66]
10 [802, 2, 24, 45, 66, 170, 75, 90]
100 [2, 24, 45, 66, 75, 90, 170, 802]
```

Birinci turdan sonra liste yalnızca son basamağa göre sıralı (170, 90, 802,
2…). Üçüncü turdan sonra tamamen sıralı. Neden doğru çalışıyor? Çünkü her tur
**kararlı**: aynı kovaya düşenler önceki sıralarını koruyor. Yüzler basamağı
eşit olan 24 ile 45 ilk iki turun kurduğu sırayı koruyarak yan yana kalıyor.
Kovalar kararlı olmasaydı önceki turların emeği bozulurdu.

**Maliyet:** `d` basamak, her turda `n` eleman ve 10 kova: `O(d × (n + 10))`.
Basamak sayısı sabitse (ör. 6 haneli posta kodu) `O(n)`.

## Kova sıralaması (bucket sort)

Değerler bir aralığa **düzgün dağılmışsa** (0 ile 1 arasında rastgele
sayılar gibi), aralığı `n` kovaya bölüp her sayıyı kovasına atarsın; her
kovada ortalama bir-iki eleman olur, onları basit bir sıralamayla sıralayıp
kovaları birleştirirsin. Ortalama `O(n)`. Veri bir kovada yığılırsa avantaj
kaybolur.

## Kovalarla gruplamak: sıralamadan önemlisi

Sayarak sıralamanın asıl fikri, değeri doğrudan **adres** olarak kullanmak,
sıralamanın ötesinde çok sık işe yarar:

- **Histogram:** her değerden kaç tane var? (`counts` listesinin kendisi)
- **Gruplama:** notu aynı olan öğrencileri birlikte listelemek
  (`buckets[grade].append(name)`)
- **k'inci en büyük:** sayaçları büyükten küçüğe gezip `k`'ye ulaşınca
  durmak; bütün listeyi sıralamaya gerek yok.

## Özet

- Karşılaştırmadan sıralamak `n log n` sınırının altına iner.
- Sayarak sıralama: değer aralığı `k` küçükse `O(n + k)`; `k` büyükse
  kullanılmaz.
- Radix sort: basamak basamak, her turda **kararlı** kovalarla;
  `O(d × (n + taban))`.
- Kova sıralaması: düzgün dağılmış veride ortalama `O(n)`.
- Değeri adres olarak kullanmak (histogram, gruplama) sıralamanın dışında da
  çok kullanılır.
