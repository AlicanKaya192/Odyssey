# Arama

Bir listede bir değeri bulmanın en basit yolunu biliyoruz: **doğrusal
arama**, baştan sona bakmak, `O(n)`. Liste karışıksa daha iyisi de yok;
her elemana bakmadan "yok" diyemezsin. Ama liste **sıralıysa** durum
tamamen değişir.

## Sıralı listede aramak: ikili arama

Sözlükte "kitap" kelimesini ararken ilk sayfadan başlamazsın. Ortadan
açarsın: "m" harfine denk geldiysen kelime **daha önde**; sözlüğün arka
yarısını bir daha açmazsın. Sonra kalan yarının ortasını açarsın. Her
bakışta kalan yerin **yarısı** elenir.

Buna **ikili arama (binary search)** denir. Sözde kodu:

```text
lo ← 0, hi ← son indeks
lo ≤ hi olduğu sürece:
    mid ← (lo + hi) // 2
    eğer liste[mid] = hedef: sonuç: mid
    eğer liste[mid] < hedef: lo ← mid + 1     (hedef sağda)
    değilse: hi ← mid - 1                      (hedef solda)
sonuç: yok (-1)
```

`lo` ve `hi` aradığımız bölgenin iki ucu. Her turda ortadaki elemana
bakıp bölgenin yarısını atıyoruz. Python'da, her turda bölgeyi de
yazdırarak:

```python
def binary_search(items, target):
    lo, hi = 0, len(items) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        print(lo, hi, mid, items[mid])
        if items[mid] == target:
            return mid
        elif items[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1

data = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
print(binary_search(data, 23))
print(binary_search(data, 40))
```

```text
0 9 4 16
5 9 7 56
5 6 5 23
5
0 9 4 16
5 9 7 56
5 6 5 23
6 6 6 38
-1
```

23'ü üç bakışta bulduk (sütunlar: `lo`, `hi`, `mid`, ortadaki değer). 40
için dört bakıştan sonra bölge boşaldı (`lo > hi`) ve `-1` döndü: 40 listede
yok.

<figure class="fig">
  <div class="versus">
    <div><h4>Doğrusal arama</h4>
      <p>Baştan sona her elemana bakar.</p>
      <p>Liste sıralı olmak zorunda değil.</p>
      <p>1 000 000 elemanda en kötü <b>1 000 000</b> bakış: <code>O(n)</code></p></div>
    <div class="ok"><h4>İkili arama</h4>
      <p>Her bakışta kalan bölgenin yarısını atar.</p>
      <p>Liste <b>sıralı</b> olmalı.</p>
      <p>1 000 000 elemanda en kötü <b>20</b> bakış: <code>O(log n)</code></p></div>
  </div>
  <figcaption>Sıralı olmanın getirisi: arama doğrusal olmaktan çıkıp logaritmik oluyor.</figcaption>
</figure>

Her turda bölge yarıya indiği için ikili arama `O(log n)`: bir milyon
elemanda en fazla 20 bakış, bir milyarda 30. Doğrusal arama aynı listede bir
milyar bakış isteyebilir.

**Ön koşul:** liste sıralı olmalı. Karışık listede ikili arama yanlış cevap
verir, hata vermez; bu yüzden tehlikeli.

## Tek karakterlik hata

İkili aramanın fikri basit ama sınırları zor. Döngü koşulunu `lo <= hi`
yerine `lo < hi` yazmak masum görünür:

```python
def binary_search_wrong(items, target):
    lo, hi = 0, len(items) - 1
    while lo < hi:                     # <= olmalıydı
        mid = (lo + hi) // 2
        if items[mid] == target:
            return mid
        elif items[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1

data = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
print([binary_search_wrong(data, x) for x in data])
```

```text
[-1, 1, 2, -1, 4, 5, -1, 7, 8, -1]
```

Listedeki 10 değerin **4'ü bulunamadı**. Bölge tek elemana indiğinde
(`lo == hi`) döngü o elemana bakmadan bitiyor. Böyle hatalar sıradan bir
örnekte görünmeyebilir; listedeki **her** değeri arayarak denemek onları
yakalar.

İkili aramada üç şeyin birbirine uyması gerekir:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>Başlangıç</span><span><code>lo = 0</code>, <code>hi = len(items) - 1</code>: iki uç da aranan bölgeye <b>dahil</b>.</span></div>
    <div class="anat-row"><span>Döngü koşulu</span><span><code>lo &lt;= hi</code>: tek elemanlı bölgeye de bakılır.</span></div>
    <div class="anat-row"><span>Bölgeyi daraltma</span><span><code>lo = mid + 1</code> ya da <code>hi = mid - 1</code>: bakılan <code>mid</code> bir daha bölgede kalmaz, bölge her turda küçülür.</span></div>
  </div>
  <figcaption>Üçü birlikte "iki ucu dahil" aralığı anlatıyor. Birini değiştirirsen öbürlerini de ona uydurman gerekir.</figcaption>
</figure>

`mid + 1` yerine `lo = mid` yazmak daha kötüsünü yapabilir: bölge hiç
küçülmez ve döngü **sonsuza kadar** döner.

## İlk geçişi bulmak

Liste tekrar eden değerler içeriyorsa ikili arama değerin **herhangi bir**
geçişini bulur. Çoğu zaman ise **ilkini** isteriz: "puanı 55 olan ilk
öğrenci". Bunun için eşleşmeyi bulunca durmayız; cevabı not edip **solda
aramaya devam ederiz**:

```python
def first_occurrence(items, target):
    lo, hi = 0, len(items) - 1
    answer = -1
    while lo <= hi:
        mid = (lo + hi) // 2
        if items[mid] == target:
            answer = mid          # buldum, ama daha solda olabilir
            hi = mid - 1
        elif items[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return answer
```

Hâlâ `O(log n)`: her turda bölge yine yarıya iniyor.

## Hazırı: `bisect` modülü

Python'un standart kütüphanesinde ikili aramanın hazır, hatasız hâli var.
`bisect` modülü bir değerin sıralı listede **nereye girmesi gerektiğini**
bulur:

- `bisect_left(items, x)`: `x`'in girebileceği **en soldaki** yer (yani `x`
  varsa ilk geçişi).
- `bisect_right(items, x)`: `x`'in girebileceği **en sağdaki** yer (son
  geçişin bir sağı).
- `insort(items, x)`: `x`'i sırayı bozmadan ekler.

```python
import bisect

scores = [40, 55, 55, 55, 70, 85, 90]
print(bisect.bisect_left(scores, 55), bisect.bisect_right(scores, 55))
print(bisect.bisect_right(scores, 55) - bisect.bisect_left(scores, 55))
print(bisect.bisect_left(scores, 60))
bisect.insort(scores, 60)
print(scores)
```

```text
1 4
3
4
[40, 55, 55, 55, 60, 70, 85, 90]
```

İki sınırın farkı, değerin listede **kaç kez** geçtiğini `O(log n)`'de
verir: 55 üç kez var. 60 listede yok ama yerinin 4. indeks olduğunu
biliyoruz. Dikkat: `insort` yerini `O(log n)`'de bulsa da eklemek için
arkadakileri kaydırır, yani `O(n)`.

## Cevap üzerinde ikili arama

İkili arama yalnızca listelerde değil, **"evet/hayır" cevabı bir noktadan
sonra değişen** her soruda işe yarar. Örnek: `n`'nin tam sayı karekökü,
yani `k * k <= n` olan en büyük `k`. `k` büyüdükçe `k * k <= n` önce
doğru, sonra hep yanlış. Bu sınırı ikili aramayla buluruz: `0` ile `n`
arasındaki aralığı her turda yarıya indiririz. Alıştırmalarda bunu
yazacaksın. Aynı fikir "en az kaç sunucu yeter?", "en fazla kaç kişi
sığar?" gibi sorularda da çalışır.

## Ne zaman sıralamaya değer?

Karışık bir listede tek bir arama yapacaksan doğrusal arama (`O(n)`) en
iyisi: sıralamak zaten `O(n log n)`. Ama aynı listede **çok sayıda** arama
yapacaksan bir kez sıralayıp sonra her aramayı `O(log n)`'de yapmak kazanır.
Yalnızca "var mı?" soruluyorsa küme daha da iyi; ama küme "60'tan büyük ilk
değer" ya da "40 ile 70 arasında kaç değer var?" sorularını cevaplayamaz,
sıralı liste cevaplar.

## Özet

- Karışık listede arama `O(n)`; sıralı listede ikili arama `O(log n)`.
- İkili arama her turda bölgenin yarısını atar; ön koşulu liste sıralı
  olması.
- Sınırlar tutarlı olmalı: `lo <= hi`, `lo = mid + 1`, `hi = mid - 1`.
  Hatalar ancak her değer ve uç durumlar denenince görünür.
- İlk geçiş için bulunca durma, solda aramaya devam et.
- Hazırı `bisect`: `bisect_left`, `bisect_right`, `insort`.
- "Bir noktadan sonra cevabı değişen" her soruda ikili arama kullanılabilir.
