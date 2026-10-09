# Öncelik Kuyruğu ve Heap

Hastanenin acil servisinde hastalar geliş sırasıyla değil **aciliyete** göre
alınır. Bilgisayarda da aynı ihtiyaç sık çıkar: işletim sistemi önce önemli
görevi çalıştırır, bir harita uygulaması en kısa yolu ararken hep "şimdiye
kadarki en yakın" noktayı açar, bir model en iyi `k` tahmini tutar. Bunun
adı **öncelik kuyruğu (priority queue)**: istediğin sırayla eleman ekle,
her seferinde **en küçüğü** (en öncelikliyi) al.

İki basit yol da bir yerde tıkanır:

| Yapı | Ekle | En küçüğü al |
|---|---|---|
| Sırasız liste | `O(1)` | `O(n)` (hepsine bak) |
| Sıralı liste | `O(n)` (kaydırma) | `O(1)` |
| **Heap** | `O(log n)` | `O(log n)` |

## Heap nedir?

**Heap (yığın ağacı)**, iki kuralı olan bir ikili ağaç:

1. **Şekil:** ağaç seviye seviye, soldan sağa **boşluksuz** dolar (tam ikili
   ağaç). Bu yüzden yüksekliği her zaman `≈ log₂ n`; BST'deki zincir sorunu
   hiç çıkmaz.
2. **Sıra:** her düğüm **çocuklarından küçük ya da eşit** (min-heap). Böylece
   en küçük değer hep **kökte**.

BST'den farkı: kardeşler arasında sıra yok. Heap tam sıralı değil, yalnızca
"en küçüğü hemen bulacak kadar" sıralı. O kadarı da ucuz.

## Diziye gömülü ağaç

Şekil kuralı boşluk bırakmadığı için heap'i düğüm nesneleriyle değil **düz bir
listeyle** tutabiliriz. Seviyeler soldan sağa sırayla yazılır:

<figure class="fig">
<svg viewBox="0 0 350 180" width="350" xmlns="http://www.w3.org/2000/svg">
<line class="line" x1="79.0" y1="89.0" x2="23.0" y2="153.0"/>
<line class="line" x1="79.0" y1="89.0" x2="135.0" y2="153.0"/>
<line class="line" x1="303.0" y1="89.0" x2="247.0" y2="153.0"/>
<line class="line" x1="191.0" y1="25.0" x2="79.0" y2="89.0"/>
<line class="line" x1="191.0" y1="25.0" x2="303.0" y2="89.0"/>
<circle class="box" cx="23.0" cy="153.0" r="17"/>
<circle class="curve4" cx="23.0" cy="153.0" r="17"/>
<text class="ink" x="23.0" y="157.9" font-size="14" text-anchor="middle">5</text>
<circle class="box" cx="79.0" cy="89.0" r="17"/>
<circle class="curve" cx="79.0" cy="89.0" r="17"/>
<text class="ink" x="79.0" y="93.9" font-size="14" text-anchor="middle">3</text>
<circle class="box" cx="135.0" cy="153.0" r="17"/>
<circle class="curve4" cx="135.0" cy="153.0" r="17"/>
<text class="ink" x="135.0" y="157.9" font-size="14" text-anchor="middle">9</text>
<circle class="box" cx="191.0" cy="25.0" r="17"/>
<text class="ink" x="191.0" y="29.9" font-size="14" text-anchor="middle">1</text>
<circle class="box" cx="247.0" cy="153.0" r="17"/>
<text class="ink" x="247.0" y="157.9" font-size="14" text-anchor="middle">8</text>
<circle class="box" cx="303.0" cy="89.0" r="17"/>
<text class="ink" x="303.0" y="93.9" font-size="14" text-anchor="middle">2</text>
</svg>
<svg viewBox="0 0 350 66" width="350" xmlns="http://www.w3.org/2000/svg">
<text class="dim" x="4" y="18" font-size="12">indeks</text>
<text class="dim" x="93.0" y="18" font-size="12" text-anchor="middle">0</text>
<rect class="box" x="70" y="26" width="46" height="36"/>
<text class="ink" x="93.0" y="48.9" font-size="14" text-anchor="middle">1</text>
<text class="dim" x="139.0" y="18" font-size="12" text-anchor="middle">1</text>
<rect class="box" x="116" y="26" width="46" height="36"/>
<rect class="curve" x="118" y="28" width="42" height="32" rx="4"/>
<text class="ink" x="139.0" y="48.9" font-size="14" text-anchor="middle">3</text>
<text class="dim" x="185.0" y="18" font-size="12" text-anchor="middle">2</text>
<rect class="box" x="162" y="26" width="46" height="36"/>
<text class="ink" x="185.0" y="48.9" font-size="14" text-anchor="middle">2</text>
<text class="dim" x="231.0" y="18" font-size="12" text-anchor="middle">3</text>
<rect class="box" x="208" y="26" width="46" height="36"/>
<rect class="curve4" x="210" y="28" width="42" height="32" rx="4"/>
<text class="ink" x="231.0" y="48.9" font-size="14" text-anchor="middle">5</text>
<text class="dim" x="277.0" y="18" font-size="12" text-anchor="middle">4</text>
<rect class="box" x="254" y="26" width="46" height="36"/>
<rect class="curve4" x="256" y="28" width="42" height="32" rx="4"/>
<text class="ink" x="277.0" y="48.9" font-size="14" text-anchor="middle">9</text>
<text class="dim" x="323.0" y="18" font-size="12" text-anchor="middle">5</text>
<rect class="box" x="300" y="26" width="46" height="36"/>
<text class="ink" x="323.0" y="48.9" font-size="14" text-anchor="middle">8</text>
</svg>
<figcaption>Aynı heap ağaç ve liste olarak. 1 indeksindeki 3'ün (mor) çocukları 2·1 + 1 = 3 ve 2·1 + 2 = 4 indekslerinde: 5 ve 9 (yeşil).</figcaption>
</figure>

`i` indeksindeki düğümün çocukları `2i + 1` ve `2i + 2`, ebeveyni `(i - 1) // 2`.
İşaretçi yok, ek bellek yok. Python'un `heapq` modülü tam olarak bunu yapar.

## `heapq` ile

```python
import heapq

heap = []
for x in [5, 3, 8, 1, 9, 2]:
    heapq.heappush(heap, x)
print(heap)
print(heapq.heappop(heap), heapq.heappop(heap), heap)
```

```text
[1, 3, 2, 5, 9, 8]
1 2 [3, 5, 8, 9]
```

Liste **sıralı değil** (`[1, 3, 2, ...]`), ama `heap[0]` hep en küçük ve
`heappop` her seferinde sıradaki en küçüğü veriyor.

## İçeride ne oluyor?

**Ekleme (yukarı kaydırma, sift up):** yeni değer listenin sonuna konur, yani
ağacın en alt boş yerine. Ebeveyninden küçük olduğu sürece onunla yer
değiştirerek yukarı çıkar:

```python
def push(heap, x):
    heap.append(x)
    i = len(heap) - 1
    while i > 0:
        parent = (i - 1) // 2
        if heap[i] >= heap[parent]:     # kural sağlandı
            break
        heap[i], heap[parent] = heap[parent], heap[i]
        i = parent

h = []
for x in [5, 3, 8, 1, 9, 2]:
    push(h, x)
print(h)
```

```text
[1, 3, 2, 5, 9, 8]
```

`heapq` ile aynı liste çıktı. En fazla ağacın yüksekliği kadar adım:
`O(log n)`.

**En küçüğü almak (aşağı kaydırma, sift down):** kök alınır, yerine listenin
**son** elemanı konur. Bu eleman büyükse kural bozulur; **küçük çocuğuyla**
yer değiştirerek aşağı iner, iki çocuğundan da küçük olunca durur. Yine
`O(log n)`. Bunu alıştırmada kendin yazacaksın.

## heapify ve heap sort

Elinde hazır bir liste varsa elemanları tek tek eklemek gerekmez:
`heapq.heapify` listeyi **yerinde** heap'e çevirir ve bunu `O(n)`'de yapar.
Sonra `n` kez `heappop` değerleri sıralı verir: **heap sort**, `O(n log n)`.

```python
data = [5, 3, 8, 1, 9, 2]
heapq.heapify(data)
print(data)
print([heapq.heappop(data) for _ in range(len(data))])
```

```text
[1, 3, 2, 5, 9, 8]
[1, 2, 3, 5, 8, 9]
```

Python'da sıralamak için `sorted` daha hızlı (C ile yazılmış ve veri
içindeki sıralı parçaları kullanıyor). Heap sort'un değeri, ek bellek
istemeden yerinde yapılabilmesi ve en kötü durumda da `O(n log n)` kalması.

## En büyük k eleman

Bir milyon sayının en büyük 10'u için bütün listeyi sıralamak gereksiz.
`heapq.nlargest` boyu `k` olan bir heap tutar:

```text
same result      : True
sorted(...)[:10] : 141.7 ms
heapq.nlargest   : 10.7 ms
```

Aynı sonuç, kat kat hızlı. Fikir şu: en büyük `k`'yı bulmak için
boyu `k` olan bir **min-heap** tut. Kökte, şimdiye kadarki en büyük `k`'nın
**en küçüğü** durur; yeni sayı ondan büyükse kökü atıp yeni sayıyı koy:

```python
def top_k(stream, k):
    heap = []
    for x in stream:
        if len(heap) < k:
            heapq.heappush(heap, x)
        elif x > heap[0]:                  # kökten büyükse yer aç
            heapq.heapreplace(heap, x)     # pop + push tek adımda
    return sorted(heap, reverse=True)

print(top_k([4, 1, 7, 3, 9, 2, 8], 3))
```

```text
[9, 8, 7]
```

Maliyet `O(n log k)` ve bellek yalnızca `O(k)`: veri bir dosyadan ya da
akıştan satır satır gelse bile çalışır.

## Öncelikli görevler: demetler

Heap'e `(öncelik, değer)` demetleri koyunca demetler ilk elemana göre
karşılaştırılır:

```python
tasks = []
heapq.heappush(tasks, (2, "write report"))
heapq.heappush(tasks, (1, "fix bug"))
heapq.heappush(tasks, (3, "lunch"))
while tasks:
    print(heapq.heappop(tasks))
```

```text
(1, 'fix bug')
(2, 'write report')
(3, 'lunch')
```

Bir tuzak: iki görevin önceliği **eşitse** Python ikinci elemanları
karşılaştırır. Onlar karşılaştırılamayan şeylerse (sözlük gibi) hata alırsın:

```python
jobs = []
heapq.heappush(jobs, (1, {"name": "a"}))
heapq.heappush(jobs, (1, {"name": "b"}))
```

```text
TypeError: '<' not supported between instances of 'dict' and 'dict'
```

Çözüm, araya artan bir sayaç koymak: `(öncelik, sıra_no, değer)`. Eşitlikte
sayaç karar verir, üstelik eşit öncelikliler **geliş sırasıyla** çıkar.
`itertools.count()` bu sayacı verir.

## Max-heap

`heapq` min-heap'tir. En büyüğü almak için iki yol var: değerleri **eksiyle**
koymak (`heappush(h, -x)`, alırken yine eksi) ya da Python 3.14 ile gelen
max-heap fonksiyonları:

```python
m = [5, 3, 8, 1, 9, 2]
heapq.heapify_max(m)
print(m, heapq.heappop_max(m))
```

```text
[8, 5, 2, 1, 3] 9
```

## Sıralı listeleri birleştirmek

`k` tane sıralı listeyi tek sıralı listede birleştirmek için her listenin
**ilk** elemanını bir heap'e koy, en küçüğü al, o listenin sıradakini ekle.
`heapq.merge` bunu tembel (lazy) yapar, elemanları istedikçe üretir:

```python
print(list(heapq.merge([1, 4, 9], [2, 3, 10], [5])))
```

```text
[1, 2, 3, 4, 5, 9, 10]
```

Belleğe sığmayan bir dosyayı sıralamanın klasik yolu bu: parça parça sırala,
diske yaz, sonra parçaları `merge` ile birleştir (dış sıralama, external
sort). Büyük Veri patikasındaki parça parça işleme fikrinin aynısı.

## Veri biliminde

- **k-en yakın komşu:** bir noktaya en yakın `k` örnek, mesafeler üzerinde
  `top_k`'nın aynısı (en küçük `k`).
- **Öneri sistemleri:** milyonlarca ürünün puanından en iyi 20'si; sıralama
  değil heap.
- **En kısa yol:** ALG 2'deki Dijkstra algoritması "en yakın açılmamış
  düğümü" bir öncelik kuyruğundan alır.

## Özet

- Öncelik kuyruğu: istediğin sırayla ekle, hep en küçüğü al. Heap ikisini de
  `O(log n)`'de yapar; en küçüğe bakmak `O(1)`.
- Heap: boşluksuz ikili ağaç + ebeveyn ≤ çocuk. Düz listede: çocuklar `2i+1`,
  `2i+2`, ebeveyn `(i-1)//2`.
- Ekleme yukarı, alma aşağı kaydırma. `heapify` `O(n)`, heap sort `O(n log n)`.
- En büyük `k`: boyu `k` olan min-heap, `O(n log k)`; `heapq.nlargest`.
- Demetlerde eşitlik için sayaç: `(öncelik, sıra_no, değer)`.
- Max-heap: eksiyle ya da `heapify_max` / `heappop_max`.
- `heapq.merge`: sıralı listeleri tembelce birleştirir.
