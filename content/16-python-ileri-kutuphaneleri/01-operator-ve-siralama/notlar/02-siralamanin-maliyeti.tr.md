## key kaç kez çağrılır?

```python
import random

calls = 0


def slow_key(x):
    global calls
    calls += 1
    return -x


result = sorted(range(1000), key=slow_key)
print(calls, result[:3])
comparisons = 0


class Counted:
    def __init__(self, value):
        self.value = value

    def __lt__(self, other):
        global comparisons
        comparisons += 1
        return self.value < other.value


data = [Counted(v) for v in random.Random(1).sample(range(10_000), 1000)]
sorted(data)
print(comparisons)
```

```text
1000 [999, 998, 997]
8669
```

- **`key` her eleman için yalnızca bir kez** çağrıldı (1000 eleman, 1000
  çağrı). Python anahtarları önce hesaplayıp saklıyor, karşılaştırmaları
  saklanan anahtarlarla yapıyor. Pahalı bir anahtar (dosyadan okumak,
  hesaplamak) bu yüzden sorun değil.
- Karşılaştırma sayısı ise 8 669: yaklaşık `n × log₂ n` (1000 × 10 ≈
  10 000). Sıralamanın maliyeti eleman sayısından biraz hızlı büyür.

## Ne zaman ne?

| İş | Araç | Neden |
|---|---|---|
| Bütün liste sıralı lazım | `sorted` / `sort` | tek seferde |
| Yalnızca ilk 10 | `heapq.nlargest(10, x)` | bütün listeyi sıralamaz |
| Tek en büyük | `max(x, key=...)` | bir geçiş |
| Sıralı listeye sık ekleme | `bisect.insort` | her seferinde baştan sıralamaz |
| Sıralı listede var mı | `bisect.bisect_left` | ikili arama, `in`'den hızlı |
| Çok sık "var mı" sorusu | `set` | sırasız ama en hızlısı |

Sıralı bir listede `x in liste` baştan sona bakar; `bisect` ikiye bölerek
bakar. Bir milyon elemanda bu fark yaklaşık 50 000 kat karşılaştırma
demektir (bir milyona karşı yaklaşık 20). Algoritmalar patikasında ikili
arama ayrıntılı anlatılıyor.
