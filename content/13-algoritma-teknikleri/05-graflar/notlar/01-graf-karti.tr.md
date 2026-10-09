## Terimler

| Terim | Anlamı |
|---|---|
| Düğüm (node, vertex) | grafın noktası: kişi, şehir, sayfa |
| Kenar (edge) | iki düğüm arasındaki bağ |
| Komşu | bir kenarla doğrudan bağlı düğüm |
| Derece | düğümün kenar sayısı; yönlüde giren ve çıkan ayrı |
| Yönlü / yönsüz | kenarın tek yönlü olup olmadığı |
| Ağırlıklı | kenarın değeri var (uzunluk, süre) |
| Yol | kenarlarla bağlanan düğüm dizisi |
| Döngü (cycle) | başladığı düğüme dönen yol |
| Bağlı | her düğümden her düğüme yol var |
| Seyrek / yoğun | kenar sayısı `n²`'den çok az / ona yakın |

## Kurulum kalıpları

```python
graph = {}
for a, b in edges:                        # yönsüz
    graph.setdefault(a, set()).add(b)
    graph.setdefault(b, set()).add(a)

directed = {}
for a, b in edges:                        # yönlü: yalnızca a → b
    directed.setdefault(a, set()).add(b)
    directed.setdefault(b, set())         # çıkışı olmayan düğüm de görünsün
```

Ağırlıklı grafta küme yerine sözlük: `graph[a][b] = ağırlık`.

## Hangi temsil?

- **Komşuluk sözlüğü:** varsayılan seçim; seyrek graflar, gezinme
  algoritmaları.
- **Matris:** küçük ve yoğun graflar, `A @ A` gibi cebir, "kenar var mı?"
  sorusu çok sık soruluyorsa.
- **Kenar listesi:** dosyada saklamak, kenarları ağırlığa göre sıralamak
  (en küçük kapsayan ağaçta Kruskal).

## Hazır paketler

`networkx` grafları ve yüzlerce algoritmayı hazır verir; büyük graflarda
`scipy.sparse` matrisleri seyrek komşuluk matrisini belleğe sığdırır. Bu
patikada algoritmaları kendimiz yazıyoruz; gerçek işte önce bunlara bakılır.

## Sık hatalar

- Yönsüz grafta kenarı yalnızca bir yöne eklemek.
- Yalnızca kenarların içinde geçen düğümleri tutmak: hiç kenarı olmayan
  düğüm sözlükte görünmez; gerekiyorsa ayrıca eklenir.
- Büyük seyrek grafı yoğun matrisle tutmak: 10 000 düğüm 100 milyon hücre.
