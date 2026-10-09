## Terimler

| Terim | Anlamı |
|---|---|
| Kök (root) | En üstteki düğüm, ebeveyni yok |
| Yaprak (leaf) | Çocuğu olmayan düğüm |
| Alt ağaç (subtree) | Bir düğüm ve altındaki her şey |
| Derinlik (depth) | Düğümün köke uzaklığı; kök 0 |
| Yükseklik (height) | En uzun kökten yaprağa yoldaki düğüm sayısı |
| İkili ağaç (binary tree) | Her düğümün en fazla iki çocuğu (sol, sağ) var |

## Gezinme sıraları

Derslerdeki ağaç: kök `1`; `2`'nin çocukları `4`, `5`; `3`'ün sağ çocuğu `6`.

| Sıra | Kural | Sonuç | Ne için |
|---|---|---|---|
| Preorder | kök, sol, sağ | `1 2 4 5 3 6` | yapıyı kopyalamak, yazdırmak |
| Inorder | sol, kök, sağ | `4 2 5 1 3 6` | arama ağacında sıralı değerler |
| Postorder | sol, sağ, kök | `4 5 2 6 3 1` | önce çocukların cevabı gerekince |
| Seviye (BFS) | kuyrukla kat kat | `[1] [2, 3] [4, 5, 6]` | en kısa yol, kat kat işlem |

## İki iskelet

Özyineli (çoğu soru):

```python
def solve(node):
    if node is None:
        return BOS_AGACIN_CEVABI
    left = solve(node.left)
    right = solve(node.right)
    return BIRLESTIR(node.value, left, right)
```

Seviye seviye:

```python
queue = deque([root])
while queue:
    for _ in range(len(queue)):
        node = queue.popleft()
        ...                                # bu seviyedeki düğüm
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
```

## Maliyetler

| İş | Süre | Ek bellek |
|---|---|---|
| Bütün düğümleri gezmek (DFS ya da BFS) | `O(n)` | DFS `O(h)`, BFS `O(genişlik)` |
| Kökten bir yaprağa yürümek | `O(h)` | `O(1)` |
| Dengeli ağaçta `h` | `≈ log₂ n` | |
| Zincir hâlindeki ağaçta `h` | `n` | |

## Sık hatalar

- Taban durumunu (`if node is None`) unutmak → `None`'un `.left`'ine erişip
  `AttributeError`.
- Yaprağı yanlış tanımlamak: yaprak `left` **ve** `right` `None` olan düğüm;
  yalnızca biri `None` olan düğüm yaprak değil.
- BFS'te seviyeyi ayırmak için `len(queue)`'yu döngü **başlamadan** almak
  gerek; `range(len(queue))` bunu kendiliğinden yapar, `while` içinde
  `len(queue)`'ya her adımda bakmak yapmaz.
- Çok derin (zincire yakın) ağaçta özyineleme `RecursionError` verir; o zaman
  yığınlı ya da kuyruklu yazım.
