# Bağlı Listeler

Python listesi elemanlarını bellekte **yan yana** tutar: indeksle erişim
`O(1)`, ama başa ya da ortaya eklemek bütün elemanları kaydırır, `O(n)`.
**Bağlı liste (linked list)** bunun tersini seçer: elemanlar bellekte
dağınık durur, her eleman **bir sonrakinin adresini** taşır. Kaydırma yok;
başa eklemek `O(1)`. Bedeli: `i`'inci elemana gitmek için baştan saymak
gerekir, `O(n)`.

Python'da hazır bir bağlı liste sınıfı yok (`deque` içeride buna benzer bir
yapı kullanır). Kendimiz yazacağız; asıl amaç **işaretçilerle düşünmeyi**
öğrenmek: ağaçlar ve graflar da aynı fikirle kurulur.

## Düğüm (node)

Bağlı listenin her parçası bir **düğüm**: bir değer ve bir sonraki düğüme
**bağlantı** (`next`). Son düğümün `next`'i `None`. Listenin kendisi yalnızca
ilk düğümü (**baş**, *head*) tutar.

```python
class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next

def to_list(head):                 # düğümleri gezip Python listesine çevir
    out = []
    while head:
        out.append(head.value)
        head = head.next
    return out

head = Node(1, Node(2, Node(3)))
print(to_list(head))
head = Node(0, head)               # başa ekleme: O(1)
print(to_list(head))
```

```text
[1, 2, 3]
[0, 1, 2, 3]
```

<figure class="fig">
  <div class="flow">
    <span class="node acc">head → 0</span><span class="arrow">→</span>
    <span class="node">1</span><span class="arrow">→</span>
    <span class="node">2</span><span class="arrow">→</span>
    <span class="node">3</span><span class="arrow">→</span>
    <span class="node">None</span>
  </div>
  <figcaption>Her düğüm bir değer ve bir sonrakinin bağlantısını taşır. Başa eklenen 0'ın bağlantısı eski baş olan 1'i gösteriyor.</figcaption>
</figure>

Başa eklerken hiçbir eleman kaydırılmadı: yeni düğüm eski başı gösteriyor,
liste artık yeni düğümden başlıyor. Farkı ölçelim; 50 000 elemanı başa
eklemek:

```text
linked list, add at front : 9.0 ms
list.insert(0, x)         : 198.5 ms
```

## Gezinmek: `while head:`

Bağlı listede `for` ile indeks yok; bir işaretçiyi düğümden düğüme
ilerletirsin: `head = head.next`. `head` `None` olunca liste bitmiştir. Bu tek
satır, bağlı listelerdeki her algoritmanın iskeleti. Dikkat: işaretçiyi
ilerletmeyi unutmak sonsuz döngüdür.

## Listeyi ters çevirmek

Bağlantıların yönünü tek geçişte çevirmek klasik bir sorudur. Üç işaretçi
gerekir: önceki (`prev`), şimdiki (`head`), sonraki (`nxt`). Sonrakini
kaybetmeden önce saklarsın:

```python
def reverse(head):
    prev = None
    while head:
        nxt = head.next        # 1. sonrakini sakla
        head.next = prev       # 2. oku geriye çevir
        prev = head            # 3. bir adım ilerle
        head = nxt
    return prev               # yeni baş

print(to_list(reverse(head)))
```

```text
[3, 2, 1, 0]
```

`O(n)` süre, `O(1)` ek bellek: yeni düğüm kurulmadı, yalnızca oklar döndü.
Sıra önemli: 1. adımı atlarsan 2. adımdan sonra listenin geri kalanına
ulaşamazsın.

## Döngü var mı? Kaplumbağa ve tavşan

Bir hata yüzünden son düğüm, listenin ortasındaki bir düğümü gösteriyorsa
liste **döngülüdür** ve `while head:` hiç bitmez. Görülen düğümleri bir
kümede tutmak işe yarar (`O(n)` bellek), ama daha zarif bir yol var: **iki
işaretçi**. Biri adım adım (kaplumbağa), öbürü ikişer ikişer (tavşan)
ilerler. Döngü yoksa tavşan sona ulaşır; döngü varsa döngünün içinde
kaplumbağaya **mutlaka yetişir** (koşu pistinde hızlı koşanın yavaşı
turlaması gibi).

```python
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:          # aynı düğüm (is: kimlik karşılaştırması)
            return True
    return False

a, b, c, d = Node("a"), Node("b"), Node("c"), Node("d")
a.next, b.next, c.next = b, c, d
print(has_cycle(a))
d.next = b                        # d → b: döngü
print(has_cycle(a))
```

```text
False
True
```

`O(n)` süre, `O(1)` bellek. İki işaretçi kalıbının bağlı listedeki hâli; aynı
fikirle listenin **ortası** da bulunur (tavşan sona varınca kaplumbağa
ortadadır).

## Bağlı listenin gerçek dünyadaki işi: LRU önbellek

Bir web sitesi en sık istenen sayfaları bellekte tutmak istiyor, ama yer
sınırlı: dolunca **en uzun süredir kullanılmayanı** atacak. Buna **LRU
(least recently used) önbellek** denir. İki işi birden hızlı yapmak gerekir:

- Anahtarla bulmak: `O(1)` → **sözlük**.
- "En son kullanılan" sırasını tutmak, bir elemanı sıranın sonuna taşımak,
  en eskisini baştan atmak: `O(1)` → **çift yönlü bağlı liste** (her düğüm
  hem öncekini hem sonrakini bilir).

Python'un `collections.OrderedDict`'i tam olarak bu ikisinin birleşimi:
içinde bir sözlük ve bir çift yönlü bağlı liste var. `move_to_end` ve
`popitem(last=False)` bağlı liste işlemleri, ikisi de `O(1)`:

```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.data = OrderedDict()

    def get(self, key):
        if key not in self.data:
            return None
        self.data.move_to_end(key)          # kullanıldı: en yeni
        return self.data[key]

    def put(self, key, value):
        self.data[key] = value
        self.data.move_to_end(key)
        if len(self.data) > self.capacity:
            self.data.popitem(last=False)   # en eskiyi at

cache = LRUCache(2)
cache.put("a", 1)
cache.put("b", 2)
print(cache.get("a"))
cache.put("c", 3)                           # dolu: en eski b atılır
print(cache.get("b"), list(cache.data))
```

```text
1
None ['a', 'c']
```

`a` okununca en yeni oldu; `c` gelince yer açmak için en eski olan `b`
atıldı. Python'da fonksiyon sonuçlarını önbelleğe almak için hazır
`functools.lru_cache` dekoratörü de var; içinde aynı fikir çalışır (Dinamik
Programlama bölümünde kullanacağız).

## Bağlı liste mi, Python listesi mi?

<figure class="fig">
  <div class="versus">
    <div><h4>Python listesi</h4>
      <p><code>items[i]</code>: <code>O(1)</code></p>
      <p>Başa/ortaya ekleme: <code>O(n)</code> (kaydırma)</p>
      <p>Bellekte yan yana, önbellek dostu</p></div>
    <div class="ok"><h4>Bağlı liste</h4>
      <p><code>i</code>'inci eleman: <code>O(n)</code> (baştan sayma)</p>
      <p>Başa ya da elindeki düğümün arkasına ekleme: <code>O(1)</code></p>
      <p>Her düğüm ayrı nesne, ek bellek</p></div>
  </div>
  <figcaption>Sık sık başa/ortaya ekleyip çıkarıyorsan ve elinde düğüm varsa bağlı liste; indeksle erişiyorsan Python listesi.</figcaption>
</figure>

Pratikte Python'da çoğu iş için liste ya da `deque` yeterli; bağlı listeyi
kendin nadiren yazarsın. Ama **düğüm + bağlantı** düşüncesi bir sonraki
bölümlerin temeli: ağaçta her düğümün iki çocuğu, grafta istediği kadar
komşusu olur.

## Özet

- Bağlı liste: her düğüm değer + sonraki düğüme bağlantı; liste yalnızca başı
  tutar.
- Başa ekleme `O(1)`, `i`'inci elemana gitmek `O(n)`.
- Gezinme iskeleti: `while head: ...; head = head.next`.
- Ters çevirme: üç işaretçi, `O(n)` süre, `O(1)` bellek.
- Döngü bulma: kaplumbağa ve tavşan, `O(1)` bellek.
- LRU önbellek: sözlük + çift yönlü bağlı liste; Python'da `OrderedDict` ve
  `functools.lru_cache`.
