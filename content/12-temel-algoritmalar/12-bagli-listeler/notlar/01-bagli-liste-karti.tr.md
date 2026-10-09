## Maliyetler

| İşlem | Tek yönlü bağlı liste | Python listesi |
|---|---|---|
| Başa ekle / baştan sil | `O(1)` | `O(n)` |
| Sona ekle | `O(n)` (sonu tutulursa `O(1)`) | `O(1)` amortize |
| `i`'inci eleman | `O(n)` | `O(1)` |
| Bir değeri aramak | `O(n)` | `O(n)` |
| Elindeki düğümün arkasına eklemek | `O(1)` | `O(n)` |

## Tek yönlü ve çift yönlü

- **Tek yönlü:** düğüm yalnızca `next`'i bilir. Bir düğümü silmek için ondan
  **öncekini** bulmak gerekir.
- **Çift yönlü:** düğüm `prev` ve `next`'i bilir. Elindeki herhangi bir düğümü
  `O(1)`'de silebilirsin: `node.prev.next = node.next`,
  `node.next.prev = node.prev`. LRU önbellek bu yüzden çift yönlü ister.

## Nöbetçi (sentinel) düğüm

Boş liste ve "baştaki düğümü silmek" gibi durumlar ayrı `if`'ler ister. Başa
değeri önemsiz, hep var olan bir **sahte düğüm** koymak bu özel durumları
ortadan kaldırır:

```python
dummy = Node(None, head)     # baştaki sahte düğüm
prev = dummy
while prev.next:
    if prev.next.value == target:
        prev.next = prev.next.next     # baştaki düğüm de aynı kodla silinir
        break
    prev = prev.next
head = dummy.next
```

## Sık hatalar

- İşaretçiyi ilerletmeyi unutmak (`head = head.next`) → sonsuz döngü.
- Bağlantıyı değiştirmeden önce sonrakini saklamamak → listenin geri kalanı
  kaybolur.
- `None`'un `.next`'ine erişmek → `AttributeError`. Döngü koşulunu
  `while node and node.next:` gibi yaz.
- Eşitlik ile kimliği karıştırmak: düğüm karşılaştırırken `is`, değer
  karşılaştırırken `==`.
