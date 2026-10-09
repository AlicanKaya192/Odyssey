# Genel Tekrar

ALG 1'in sonuna geldin. "Algoritma nedir?" sorusuyla başladın; şimdi bir
kodun girdi büyüyünce nasıl davranacağını önceden söyleyebiliyor, Python'un
yapılarının gizli maliyetlerini biliyor, arayıp sıralayabiliyor ve sık
karşılaşılan problemleri tanıdık kalıplarla `O(n)`'e indirebiliyorsun. Bu
bölüm yolu baştan sona bir kez daha yürüyor: her durakta en önemli fikir ve
en çok kullanacağın kod.

<figure class="fig">
  <div class="flow">
    <span class="node">Temeller<br><small>00–02</small></span><span class="arrow">→</span>
    <span class="node">Arama, sıralama<br><small>03–07</small></span><span class="arrow">→</span>
    <span class="node">Kalıplar<br><small>08–10</small></span><span class="arrow">→</span>
    <span class="node">Yapılar<br><small>11–12</small></span><span class="arrow">→</span>
    <span class="node acc">Ağaçlar<br><small>13–15</small></span>
  </div>
  <figcaption>ALG 1'in yolu: önce maliyeti ölçmeyi, sonra arama ve sıralamayı, sonra kalıpları ve yapıları öğrendin.</figcaption>
</figure>

## 1. Algoritma ve karmaşıklık (Bölüm 0–1)

Algoritma; girdiyi çıktıya çeviren, sırası belli, açık ve biten adımlar.
Doğruluk örnekte çalışmak değil **her girdide** çalışmak: boş liste, tek
eleman, negatif sayı, hepsi aynı.

Algoritmalar saniyeyle değil, **girdi büyüdükçe adım sayısının nasıl
büyüdüğüyle** karşılaştırılır. Büyük O baskın terimi tutar:

| Sınıf | Örnek | n 1000 kat büyüyünce |
|---|---|---|
| `O(1)` | sözlükte arama, listede `items[i]` | aynı |
| `O(log n)` | ikili arama | yaklaşık 10 adım fazla |
| `O(n)` | listede `in`, tek geçiş | 1000 kat |
| `O(n log n)` | `sorted`, merge sort | 1000 katın biraz üstü |
| `O(n²)` | iç içe iki döngü | bir milyon kat |

İç içe döngüler çarpılır, art arda bloklar toplanır, her turda yarıya bölen
döngü `O(log n)`.

## 2. Python yapılarının maliyeti (Bölüm 2)

| İşlem | Liste | `deque` | Küme / sözlük |
|---|---|---|---|
| `x in ...` | `O(n)` | `O(n)` | ortalama `O(1)` |
| Sona ekle | `O(1)` amortize | `O(1)` | `O(1)` |
| Başa ekle / baştan çıkar | `O(n)` | `O(1)` | — |
| `[i]` ile erişim | `O(1)` | `O(n)` ortada | — |

En sık hata, döngünün içindeki **tek satırlık `O(n)`**: `in`, `index`,
`count`, `remove`, `insert(0, …)`. Döngüyle birleşince `O(n²)` olur. Derste
1000 aramada liste ile küme arasında binlerce kat fark ölçtük.

## 3. Arama (Bölüm 3)

Sıralı listede ikili arama her turda bölgenin yarısını atar, `O(log n)`:

```python
def binary_search(items, target):
    lo, hi = 0, len(items) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if items[mid] == target:
            return mid
        if items[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
```

Hazırı `bisect`: `bisect_left` (ilk uygun yer), `bisect_right`, `insort`.
"Bir noktadan sonra cevabı değişen" her soruda ikili arama kullanılabilir.

## 4. Sıralama (Bölüm 4–7)

| Algoritma | En iyi | Ortalama | En kötü | Ek bellek | Kararlı |
|---|---|---|---|---|---|
| Kabarcık, eklemeli | `O(n)` | `O(n²)` | `O(n²)` | `O(1)` | evet |
| Seçmeli | `O(n²)` | `O(n²)` | `O(n²)` | `O(1)` | hayır |
| Merge sort | `O(n log n)` | `O(n log n)` | `O(n log n)` | `O(n)` | evet |
| Quick sort | `O(n log n)` | `O(n log n)` | `O(n²)` | ort. `O(log n)` | hayır |
| Heap sort | `O(n log n)` | `O(n log n)` | `O(n log n)` | `O(1)` | hayır |
| Sayarak (aralık `k`) | `O(n + k)` | `O(n + k)` | `O(n + k)` | `O(k)` | — |

Karşılaştırmayla sıralama `n log n`'den iyi olamaz; sayarak ve radix sort
karşılaştırmadığı için altına iner. Gerçek kodda `sorted(items, key=...)`
(Timsort, kararlı); çok ölçüt için demet anahtar: `key=lambda p: (-p[1], p[0])`.

## 5. Özyineleme ve böl-fethet (Bölüm 5–6)

Özyinelemeli fonksiyon kendini **daha küçük** girdiyle çağırır; **temel
durum** şart, her adım ona yaklaşmalı. Çağrılar çağrı yığınında birikir,
Python'da derinlik sınırı yaklaşık 1000.

Böl ve fethet: parçala, parçaları kendinle çöz, birleştir. Merge sort
"ortadan böl, birleştir", quick sort "pivotun etrafında ayır". Aynı alt
problemi tekrar tekrar çözen özyineleme üstel büyüyebilir; çaresi ALG 2'deki
dinamik programlama.

## 6. O(n)'e indiren kalıplar (Bölüm 8–10)

| Soru | Kalıp | Maliyet |
|---|---|---|
| Sıralı listede toplamı hedef olan çift | iki işaretçi, iki uçtan içeri | `O(n)` |
| Art arda `k` elemanın en büyük toplamı | sabit kayan pencere | `O(n)` |
| Şartı sağlayan en uzun parça | değişken pencere | `O(n)` |
| Çok sayıda aralık toplamı | önek toplamı: `prefix[hi] - prefix[lo]` | hazırlık `O(n)`, soru `O(1)` |
| Görüldü mü, kaç kez, tümleyeni var mı | küme / sözlük | `O(n)` |

Ortak fikir: işaretçiler geri gitmiyorsa ya da her eleman bir kez sözlüğe
giriyorsa toplam iş doğrusal kalır.

```python
seen = {}
for i, x in enumerate(nums):         # two-sum: tümleyeni sözlükte ara
    if target - x in seen:
        print(seen[target - x], i)
    seen[x] = i
```

## 7. Yığın, kuyruk, bağlı liste (Bölüm 11–12)

- **Yığın** (LIFO): liste ile `append` / `pop`. Parantez denetimi, geri alma,
  postfix, monoton yığın (sıradaki büyük eleman `O(n)`).
- **Kuyruk** (FIFO): `deque` ile `append` / `popleft`. Sırayla işlem, BFS.
  Listeyle `pop(0)` `O(n)`.
- **Bağlı liste:** düğüm = değer + sonraki. Başa ekleme `O(1)`, `i`'inci eleman
  `O(n)`. Ters çevirme üç işaretçi; döngü bulma kaplumbağa ve tavşan. LRU
  önbellek: sözlük + çift yönlü bağlı liste (`OrderedDict`).

## 8. Ağaçlar (Bölüm 13–15)

- **Ağaç:** özyineli iskelet: `None` ise taban, değilse iki çocuğun cevabını
  birleştir. DFS (preorder, inorder, postorder) yığınla, BFS kuyrukla.
- **BST:** sol alt ağaç küçük, sağ büyük. Arama, ekleme, silme `O(h)`;
  dengeliyse `O(log n)`, sıralı eklenirse zincir. Inorder sıralı verir.
- **Heap:** boşluksuz ağaç + ebeveyn ≤ çocuk, düz listede. Ekle ve en küçüğü
  al `O(log n)`; en büyük `k` için boyu `k` min-heap, `O(n log k)`.

## Hangi soruya hangi araç?

| Soru | İlk düşünülecek |
|---|---|
| "İçinde var mı?" çok kez | küme |
| "Kaç kez geçiyor?" | sözlük sayacı |
| Sıralı veride arama, "ilk/son uygun yer" | ikili arama, `bisect` |
| Art arda parçalar, alt dizi | kayan pencere ya da önek toplamı |
| Eşleşen parantez, "son açılan" | yığın |
| Sırayla işlem, en kısa adım | kuyruk (BFS) |
| Hep en küçüğü/büyüğü al | heap |
| Sıra korunarak ekle/sil, aralık sorgusu | BST ya da sıralı liste + `bisect` |
| İç içe yapı | özyineleme |

## Sırada ne var?

ALG 2 bu araçları birleştirir: dinamik programlama (özyinelemenin tekrar eden
alt problemlerini bir kez çözmek), açgözlü algoritmalar, geri izleme (tüm
olasılıkları akıllıca denemek), graflar (BFS, Dijkstra, en küçük kapsayan
ağaç), metin algoritmaları ve olasılıksal veri yapıları. ALG 3'te de veri
bilimi ve makine öğrenmesi algoritmalarını NumPy ile sıfırdan kuracaksın.
