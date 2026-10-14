Başlangıç kodu dersteki `train_lora`'yı içeriyor, ama `A` ve `B`'nin türevleri
sıfır bırakılmış; LoRA hiçbir şey öğrenmiyor. `M = W1 + A @ B` için
`g_M` hazır. Türevleri yaz: `g_A = g_M @ B.T`, `g_B = A.T @ g_M`.
`lora_accuracy(r)` uyarlanmış ağın yeni görevdeki doğruluğunu döndürüyor.
Veri ve ağ fonksiyonları salt okunur `finetune_tools.py`'de.

**Beklenen çıktı:**

```
0.94
```
