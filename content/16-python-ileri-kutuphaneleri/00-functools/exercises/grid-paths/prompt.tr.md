`grid_paths(rows, cols)` fonksiyonu `rows` × `cols` hücrelik bir ızgarada
sol üstten sağ alta yalnızca sağa ve aşağı giderek kaç farklı yol olduğunu
özyinelemeyle sayıyor. Kod doğru ama `16 × 16`'da milyonlarca kez aynı
hesabı yapıyor ve süreye takılıyor. Fonksiyona **`@lru_cache`** ekleyerek
hızlandır.

**Beklenen çıktı:**

```
6
155117520
```
