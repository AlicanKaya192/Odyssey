# Verimli Sıralamalar

Basit sıralamalar `O(n²)`: bir milyon elemanda yaklaşık 500 milyar
karşılaştırma. Bu bölümde aynı işi `O(n log n)`'de, yani yaklaşık 20 milyon
karşılaştırmada yapan iki algoritmayı yazacağız: **merge sort** ve **quick
sort**. İkisi de bir önceki bölümün özyinelemesini kullanıyor ve ikisi de
aynı fikre dayanıyor: **böl ve fethet**. Problemi iki küçük parçaya böl, her
parçayı (kendinle) çöz, sonuçları birleştir.

## Merge sort: böl, sırala, birleştir

Merge sort'un kalbi bir **birleştirme (merge)** işlemi: iki **sıralı** listeyi
tek bir sıralı listeye çevirmek. İki listenin başına birer parmak koy;
hangisinin altındaki küçükse onu sonuca al ve o parmağı ilerlet. Liste biri
bitince öbürünün kalanını olduğu gibi ekle.

```python
def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:            # <=: eşitlerde soldaki önce (kararlı)
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])                # biri bitti, öbürünün kalanı
    result.extend(right[j:])
    return result
```

Her karşılaştırmada sonuca bir eleman giriyor; iki listenin toplam boyu `n`
ise birleştirme `O(n)`.

Merge sort: liste tek elemanlıysa zaten sıralı (temel durum). Değilse ortadan
ikiye böl, her yarıyı **kendisiyle** sırala, iki sıralı yarıyı birleştir.

```python
def merge_sort(items):
    if len(items) <= 1:
        return items
    mid = len(items) // 2
    return merge(merge_sort(items[:mid]), merge_sort(items[mid:]))
```

Her çağrıyı girintiyle yazdırınca bölünme ve birleşme görünüyor:

```text
[38, 27, 43, 3, 9, 82, 10]
  [38, 27, 43]
    [38]
    [27, 43]
      [27]
      [43]
    -> [27, 43]
  -> [27, 38, 43]
  [3, 9, 82, 10]
    [3, 9]
      [3]
      [9]
    -> [3, 9]
    [82, 10]
      [82]
      [10]
    -> [10, 82]
  -> [3, 9, 10, 82]
-> [3, 9, 10, 27, 38, 43, 82]
```

Önce liste tek elemanlara kadar bölündü (her satır bir çağrı), sonra yukarı
doğru `->` satırlarında birleşti.

**Neden `O(n log n)`?** Liste her katta ikiye bölünüyor: tek elemana inmek
`log₂ n` kat sürer. Her katta bütün elemanlar bir kez birleştiriliyor: kat
başına `O(n)`. Toplam `n × log n`.

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>Kat 0</span><span>1 liste, 8 eleman → birleştirmede 8 eleman yerleşir</span></div>
    <div class="anat-row"><span>Kat 1</span><span>2 liste × 4 eleman → yine 8 eleman</span></div>
    <div class="anat-row"><span>Kat 2</span><span>4 liste × 2 eleman → yine 8 eleman</span></div>
    <div class="anat-row"><span>Kat 3</span><span>8 liste × 1 eleman → temel durum, birleştirme yok</span></div>
  </div>
  <figcaption>8 elemanlı liste 3 katta (log₂ 8 = 3) tek elemanlara iner; her katta toplam 8 eleman birleştirilir: 3 × 8 = n log n.</figcaption>
</figure>

Merge sort'un bedeli: birleştirme yeni listeler kuruyor, **`O(n)` ek bellek**.
Artısı: en kötü durumu da `O(n log n)` ve **kararlı**.

## Quick sort: pivotun etrafında ayır

Quick sort işi tersinden yapar: birleştirmek yerine **önce ayırır**. Listeden
bir eleman seç (**pivot**); ondan küçükleri bir yana, büyükleri öbür yana
koy. Pivot artık kesin olarak doğru yerinde: solundakilerin hepsi küçük,
sağındakilerin hepsi büyük. Sonra iki yanı kendisiyle sırala; birleştirmeye
gerek yok, yan yana koymak yeter.

```python
def quick_sort(items):
    if len(items) <= 1:
        return items
    pivot = items[-1]                     # son elemanı pivot seç
    smaller = [x for x in items[:-1] if x < pivot]
    larger = [x for x in items[:-1] if x >= pivot]
    return quick_sort(smaller) + [pivot] + quick_sort(larger)
```

Bu sürüm anlaşılır olsun diye yeni listeler kuruyor; gerçek uygulamalar aynı
fikri liste **yerinde** (elemanları yer değiştirerek) yapar (notta var).

Pivot listeyi iki eşit yarıya bölerse merge sort gibi `log n` kat ve kat başına
`n` iş: `O(n log n)`. Rastgele veride pivot çoğunlukla "yeterince ortada"
düşer.

## Saydık: gerçekten n log n mi?

Rastgele listelerde iki algoritmanın karşılaştırmalarını sayıp `n log₂ n`
ile karşılaştırdık:

| n | n log₂ n | Merge sort | Quick sort | Basit sıralama (n²/2) |
|---|---|---|---|---|
| 1 000 | 9 966 | 8 700 | 11 291 | 499 500 |
| 10 000 | 132 877 | 120 404 | 158 746 | 49 995 000 |
| 100 000 | 1 660 964 | 1 536 526 | 2 049 758 | 4 999 950 000 |

İkisi de `n log₂ n`'in çok yakınında; basit sıralamaların `n²/2`'si ise
yüz binde 5 milyara çıkıyor. Quick sort biraz daha fazla karşılaştırma
yapıyor ama pratikte yerinde çalışan sürümü bellek dostu olduğu için çok
hızlıdır.

## Quick sort'un kötü günü

Pivot hep **en küçük** ya da **en büyük** eleman çıkarsa bir taraf boş, öbür
taraf `n − 1` elemanlı kalır: liste her katta yalnızca bir küçülür. Son elemanı
pivot alan sürüm **zaten sıralı** bir listede tam bunu yapar:

```python
def quick_sort_counting(items, count):
    if len(items) <= 1:
        return items
    pivot = items[-1]
    smaller, larger = [], []
    for x in items[:-1]:
        count[0] += 1                    # pivotla bir karşılaştırma
        if x < pivot:
            smaller.append(x)
        else:
            larger.append(x)
    left = quick_sort_counting(smaller, count)
    right = quick_sort_counting(larger, count)
    return left + [pivot] + right

count = [0]
quick_sort_counting(list(range(900)), count)
print(900, count[0])

try:
    quick_sort_counting(list(range(5000)), [0])
except RecursionError as error:
    print("RecursionError -", error)
```

```text
900 404550
RecursionError - maximum recursion depth exceeded
```

Sıralı 900 elemanda `n²/2` karşılaştırma (en kötü durum `O(n²)`), 5000
elemanda ise özyineleme derinliği 5000'e çıktı ve Python durdurdu. Gerçek
hayatta veri sık sık **zaten sıralı** ya da neredeyse sıralı gelir; bu yüzden
pivot böyle seçilmez. Çözümler:

- **Rastgele pivot:** `random.choice(items)`. Hiçbir girdi sürekli kötü
  pivot üretemez; beklenen süre `O(n log n)`.
- **Üçün ortancası:** ilk, orta ve son elemanın ortancasını pivot almak.

## Daha iyisi mümkün mü?

Karşılaştırarak sıralayan hiçbir algoritma en kötü durumda `n log n`'den
anlamlı ölçüde iyi yapamaz. Kabaca sezgisi: `n` elemanın `n!` farklı dizilişi
var ve her karşılaştırma ("a mı b mi büyük?") olasılıkları en iyi ihtimalle
yarıya indirir; doğru dizilişe inmek için `log₂(n!)` karşılaştırma gerekir,
bu da yaklaşık `n log₂ n`. Bu sınırı aşmanın tek yolu **karşılaştırmamak**:
bir sonraki bölümdeki sayarak sıralama.

## Python'un sıralaması: Timsort

`sorted` ve `list.sort` **Timsort** kullanır: merge sort ile eklemeli
sıralamanın birleşimi. Veride zaten sıralı duran parçaları (**koşu**, run)
bulur, küçük parçaları eklemeli sıralamayla düzeltir ve koşuları merge sort
gibi birleştirir. En kötü durumu `O(n log n)`, sıralı ya da neredeyse sıralı
veride `O(n)`'e yaklaşır ve **kararlıdır**.

Kendi merge sort'umuzla 200 000 rastgele sayıyı sıraladık:

```text
merge_sort (random)  : 519.7 ms
sorted     (random)  : 35.8 ms
sorted     (sorted)  : 2.8 ms
```

`sorted` bizim merge sort'tan kat kat hızlı: algoritma benzer ama C ile
yazılmış ve iyi ayarlanmış. Zaten sıralı listede ise koşuyu tanıyıp neredeyse
hiç iş yapmadı. Bu yüzden gerçek kodda **her zaman** `sorted` kullanılır; kendi
sıralamanı yazmak, fikri anlamak ve benzer algoritmaları (dış bellek sıralama,
iki sıralı dosyayı birleştirme) kurabilmek içindir.

## Özet

- Böl ve fethet: parçala, parçaları kendinle çöz, birleştir.
- Merge sort: ortadan böl, iki yarıyı sırala, **birleştir**; her zaman
  `O(n log n)`, kararlı, `O(n)` ek bellek.
- Quick sort: pivotun etrafında **ayır**, iki yanı sırala; ortalama
  `O(n log n)`, en kötü `O(n²)` (sıralı veride kötü pivot); rastgele pivot
  bunu önler.
- Karşılaştırmayla sıralama `n log n`'den iyi olamaz.
- Python'un `sorted`'ı Timsort: merge + eklemeli, koşuları kullanır, kararlı;
  gerçek kodda her zaman o.
