# Basit Sıralamalar

Sıralama, algoritmaların en çok çalışılan konusudur: bir önceki bölümde
gördüğümüz gibi sıralı bir listede arama `O(log n)`'e iner; tekrarları
bulmak, ortancayı almak, iki listeyi karşılaştırmak hep kolaylaşır. Python'da
sıralama tek satır (`sorted(items)`), ama içindeki fikirleri bilmeden hangi
veride neden hızlı ya da yavaş olduğunu anlayamayız.

Bu bölümde üç **basit** sıralamayı kendimiz yazacağız. Üçü de `O(n²)`; büyük
listelerde yavaş. Ama çok önemli fikirler taşıyorlar ve biri (eklemeli
sıralama) bugün bile Python'un kendi sıralamasının içinde çalışıyor.

Örneklerde fonksiyonlar listenin bir **kopyasını** (`items[:]`) sıralayıp
döndürüyor; asıl liste değişmiyor.

## Kabarcık sıralaması (bubble sort)

Fikir: komşu iki elemanı karşılaştır, yanlış sıradaysa yer değiştir. Listenin
başından sonuna böyle bir **geçiş** yapınca en büyük eleman, suyun yüzeyine
çıkan bir kabarcık gibi en sona taşınır. Sonra aynı işi kalan kısım için
tekrarla.

```python
def bubble_sort(items):
    items = items[:]
    n = len(items)
    passes = 0
    for end in range(n - 1, 0, -1):
        swapped = False
        for i in range(end):
            if items[i] > items[i + 1]:
                items[i], items[i + 1] = items[i + 1], items[i]
                swapped = True
        passes += 1
        print(passes, items)
        if not swapped:          # bu geçişte hiç değişim yoksa liste sıralı
            break
    return items

bubble_sort([5, 1, 4, 2, 8])
```

```text
1 [1, 4, 2, 5, 8]
2 [1, 2, 4, 5, 8]
3 [1, 2, 4, 5, 8]
```

İlk geçişte 8 zaten sondaydı, 5 sona doğru ilerledi. İkinci geçişten sonra
liste sıralıydı; üçüncü geçiş hiç değişim yapmadı ve `swapped` sayesinde
döngü erken bitti. Bu küçük kontrol olmasa algoritma sıralı listede de bütün
geçişleri yapardı.

`a, b = b, a` Python'da iki değişkenin değerini yer değiştirmenin kısa
yolu: sağdaki demet önce kurulur, sonra sola dağıtılır.

## Seçmeli sıralama (selection sort)

Fikir: listenin geri kalanındaki **en küçüğü bul**, başa koy. Sonra ikinci
yerden itibaren aynısını yap. Bir önceki bölümlerde yazdığımız "en küçüğün
yeri" fonksiyonunu tekrar tekrar çalıştırmak gibi.

```python
def selection_sort(items):
    items = items[:]
    for start in range(len(items) - 1):
        smallest = start
        for i in range(start + 1, len(items)):
            if items[i] < items[smallest]:
                smallest = i
        items[start], items[smallest] = items[smallest], items[start]
        print(start, items)
    return items

selection_sort([29, 10, 14, 37, 13])
```

```text
0 [10, 29, 14, 37, 13]
1 [10, 13, 14, 37, 29]
2 [10, 13, 14, 37, 29]
3 [10, 13, 14, 29, 37]
```

Her turda tek bir yer değiştirme yapılıyor; bu yüzden seçmeli sıralama,
yazmanın pahalı olduğu durumlarda (yer değiştirmenin maliyetli olduğu
belleklerde) tercih edilirdi. Ama karşılaştırma sayısı **her zaman** aynı:
liste zaten sıralı olsa bile en küçüğü bulmak için kalan her elemana bakıyor.

## Eklemeli sıralama (insertion sort)

Fikir: elindeki iskambil kâğıtlarını sıralarken yaptığın şey. Soldaki kısım
hep sıralı; sıradaki kâğıdı alıp sıralı kısımda **doğru yerine kadar sola
kaydırırsın**.

```python
def insertion_sort(items):
    items = items[:]
    for i in range(1, len(items)):
        current = items[i]
        j = i - 1
        while j >= 0 and items[j] > current:
            items[j + 1] = items[j]      # büyük olanı bir sağa kaydır
            j -= 1
        items[j + 1] = current           # boşalan yere yerleştir
        print(i, items)
    return items

insertion_sort([12, 11, 13, 5, 6])
```

```text
1 [11, 12, 13, 5, 6]
2 [11, 12, 13, 5, 6]
3 [5, 11, 12, 13, 6]
4 [5, 6, 11, 12, 13]
```

İkinci turda 13 zaten yerindeydi; `while` döngüsü hiç dönmedi. Eklemeli
sıralamanın gücü bu: **neredeyse sıralı** bir listede her eleman yalnızca
birkaç adım sola kayar.

## Üçünü karşılaştırmak

Aynı 1000 elemanlı listeleri üç algoritmayla sıralayıp karşılaştırma ve
yer değiştirme (eklemelide kaydırma) sayılarını saydık:

| Liste (n = 1000) | Kabarcık karş. / değişim | Seçmeli karş. / değişim | Eklemeli karş. / kaydırma |
|---|---|---|---|
| Rastgele | 498 015 / 250 393 | 499 500 / 991 | 251 387 / 250 393 |
| Sıralı | 999 / 0 | 499 500 / 0 | 999 / 0 |
| Neredeyse sıralı (son 10 karışık) | 3 990 / 13 | 499 500 / 7 | 1 012 / 13 |
| Ters sıralı | 499 500 / 499 500 | 499 500 / 500 | 499 500 / 499 500 |

Tablodan çıkanlar:

- **Rastgele listede** üçü de yaklaşık `n²/4`–`n²/2` karşılaştırma yapıyor:
  `O(n²)`.
- **Seçmeli sıralama** girdiye hiç bakmıyor: sıralı listede de 499 500
  karşılaştırma. Ama yer değiştirmesi en az.
- **Eklemeli sıralama** sıralı listede yalnızca `n − 1` karşılaştırma
  yapıyor; en iyi durumu `O(n)`. Neredeyse sıralı listede de neredeyse aynı.
- **Kabarcık** erken çıkış sayesinde sıralı listede hızlı; rastgele listede
  ise karşılaştırması seçmeli kadar, yer değiştirmesi eklemelinin kaydırması
  kadar: ikisinin kötü yanını birden taşıyor. Pratikte nadiren tercih edilir;
  öğretmek için iyidir.

Pratikte basit sıralamalardan yalnızca **eklemeli sıralama** kullanılır:
küçük listelerde (birkaç düzine eleman) ve neredeyse sıralı veride çok
hızlıdır. Python'un sıralaması (Timsort) küçük parçaları zaten eklemeli
sıralamayla sıralar.

## Kararlılık (stability)

İki eleman sıralama anahtarına göre **eşitse** (aynı puan gibi), sıralama
sonrası **önceki sıralarını koruyorlarsa** algoritma **kararlıdır**. Neden
önemli? Bir öğrenci listesini önce ada göre, sonra puana göre sıralarsan,
kararlı bir sıralama aynı puandakilerin ad sırasını bozmaz.

Seçmeli sıralama kararlı değildir: uzak bir yer değiştirme, eşit iki elemanın
arasından atlayabilir.

```python
def selection_sort_by_score(records):
    records = records[:]
    for start in range(len(records) - 1):
        smallest = start
        for i in range(start + 1, len(records)):
            if records[i][1] < records[smallest][1]:
                smallest = i
        records[start], records[smallest] = records[smallest], records[start]
    return records

students = [("Bora", 2), ("Ada", 2), ("Cem", 1)]
print(selection_sort_by_score(students))
print(sorted(students, key=lambda r: r[1]))
```

```text
[('Cem', 1), ('Ada', 2), ('Bora', 2)]
[('Cem', 1), ('Bora', 2), ('Ada', 2)]
```

Puanı 2 olan Bora girdide Ada'nın önündeydi; seçmeli sıralama onları ters
çevirdi (Cem ile Bora'nın yer değiştirmesi Bora'yı Ada'nın arkasına attı).
Python'un `sorted`'ı **kararlı**: Bora önde kaldı. Kabarcık ve eklemeli
sıralama da kararlıdır, çünkü yalnızca komşu ve **kesin büyük** olanları
yer değiştirirler (`>` yazdık, `>=` değil).

## Python'da sıralama: `key=`

Kendi sıralamamızı yazmak öğretici, ama gerçek kodda `sorted` ve
`list.sort` kullanılır. İkisi de `key=` alır: her elemandan bir **anahtar**
çıkaran fonksiyon. Karşılaştırma bu anahtarlara göre yapılır.

```python
words = ["banana", "Kiwi", "apple", "fig", "pear"]
print(sorted(words))
print(sorted(words, key=str.lower))
print(sorted(words, key=len))
print(sorted(words, key=lambda w: (len(w), w.lower())))
```

```text
['Kiwi', 'apple', 'banana', 'fig', 'pear']
['apple', 'banana', 'fig', 'Kiwi', 'pear']
['fig', 'Kiwi', 'pear', 'apple', 'banana']
['fig', 'Kiwi', 'pear', 'apple', 'banana']
```

- Büyük harfler küçüklerden önce gelir (`"Kiwi"` başta), çünkü metinler
  karakter kodlarına göre karşılaştırılır. `key=str.lower` bunu düzeltir.
- `key=len` uzunluğa göre sıralar; eşit uzunluktaki `"Kiwi"` ile `"pear"`
  kararlılık sayesinde girdideki sıralarında kalır.
- Anahtar bir **demet** olunca önce ilk elemana, eşitse ikinciye bakılır:
  "önce uzunluk, sonra alfabe".

`reverse=True` büyükten küçüğe sıralar ve kararlılığı yine korur.

## Özet

- Kabarcık: komşuları yer değiştirerek büyüğü sona taşır; erken çıkışla
  sıralı listede hızlı.
- Seçmeli: kalanların en küçüğünü başa koyar; karşılaştırma her zaman
  `n²/2`, yer değiştirme en az; kararlı değil.
- Eklemeli: sıradaki elemanı sıralı kısımda yerine kaydırır; en iyi durum
  `O(n)`, neredeyse sıralı veride en iyisi; kararlı.
- Üçü de en kötü ve ortalama durumda `O(n²)`.
- Kararlı sıralama eşit anahtarlı elemanların sırasını korur; Python'un
  `sorted`'ı kararlı.
- Gerçek kodda `sorted(items, key=...)`; demet anahtarla çok ölçütlü
  sıralama.
