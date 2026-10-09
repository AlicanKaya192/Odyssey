## Kural

Her düğümde: sol alt ağacın **tamamı** küçük, sağ alt ağacın **tamamı** büyük.
Inorder gezinme değerleri sıralı verir.

## Maliyetler

| İşlem | Dengeli BST | Zincir hâlinde BST | Sıralı liste + `bisect` | Sözlük / küme |
|---|---|---|---|---|
| Arama | `O(log n)` | `O(n)` | `O(log n)` | `O(1)` |
| Ekleme | `O(log n)` | `O(n)` | `O(n)` (kaydırma) | `O(1)` |
| Silme | `O(log n)` | `O(n)` | `O(n)` | `O(1)` |
| En küçük / en büyük | `O(log n)` | `O(n)` | `O(1)` | `O(n)` |
| Sıralı gezinme | `O(n)` | `O(n)` | `O(n)` | `O(n log n)` (sıralamak gerek) |

Sıra gerekmiyorsa sözlük ve küme her zaman daha hızlı. BST'nin işi **sırayı
korurken** değiştirebilmek.

## Silmenin üç durumu

| Durum | Ne yapılır |
|---|---|
| Yaprak | Çıkarılır |
| Tek çocuk | Çocuk yerine geçer |
| İki çocuk | Sağ alt ağacın en küçüğü (sıradaki değer) yerine yazılır, sonra o değer sağ alt ağaçtan silinir |

Sıradaki değer yerine **önceki değer** (sol alt ağacın en büyüğü) de
kullanılabilir; ikisi de kuralı korur.

## Sık hatalar

- **Yalnızca çocuklara bakmak:** `sol < düğüm < sağ` her düğümde tutsa da ağaç
  BST olmayabilir. `[5, [3, 1, 6], 8]` ağacında `6`, `3`'ün sağında doğru
  yerde ama `5`'in **sol** alt ağacında ve `5`'ten büyük. Doğrulama, her
  düğüme izin verilen **aralığı** (alt ve üst sınır) taşıyarak yapılır.
- **Eşit değerleri unutmak:** eklemede eşit değer ne olacak, baştan seçilmeli
  (yok say, say ya da hep sağa koy).
- **Özyineli eklemede dönüş değerini bağlamamak:** `insert(node.left, value)`
  yazıp `node.left = ...` demezsen yeni düğüm ağaca hiç bağlanmaz.
- **Sıralı veri eklemek:** ağaç zincire döner. Veriyi karıştırmak ya da
  dengeli bir yapı kullanmak gerekir.
