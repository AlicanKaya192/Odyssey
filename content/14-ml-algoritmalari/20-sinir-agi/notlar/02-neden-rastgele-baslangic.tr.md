Derste ağırlıklar rastgele başladı (`rng.normal`). Peki hepsi sıfırla ya da
hepsi aynı sayıyla başlasa ne olur? Dersteki 10 nöronlu ağı, hilal verisinde
üç başlangıçla eğitelim ve eğitimden sonra `W₁`'in kaç **farklı** sütunu
(farklı gizli nöronu) kaldığını sayalım:

```python
for name, value in (("zeros", 0.0), ("same", 0.5), ("random", None)):
    P = init(2, 10)
    if value is not None:
        P["W1"][:] = value
        P["W2"][:] = value
    train(P, Xtr, ytr.astype(float), 0.5, 3000)
    distinct = np.unique(P["W1"].round(6), axis=1).shape[1]
    acc = ((forward(P, Xte)[1] > 0.5) == yte).mean()
    print(name, distinct, round(acc, 3))
```

```text
zeros 1 0.5
same 1 0.93
random 10 0.97
```

**Hepsi sıfır:** ağ hiçbir şey öğrenmiyor (doğruluk 0,5). Gizli katmanın
çıktısı `tanh(0) = 0`, çıkış ağırlıkları da sıfır olduğu için iki katmanın
türevleri de sıfır çıkıyor; yalnızca çıkışın sabit terimi değişiyor ve ağ her
noktaya aynı cevabı veriyor.

**Hepsi aynı (0,5):** 10 nöron eğitim boyunca **aynı** kalıyor (1 farklı
sütun). Hepsi aynı girdiyi görüp aynı türevi aldığı için hiçbir şey onları
birbirinden ayırmıyor; 10 nöronlu ağ aslında tek nöronlu bir ağ. Doğruluk
0,93: lojistik regresyonun düzeyi.

**Rastgele:** 10 nöronun hepsi farklı, doğruluk 0,97.

Buna **simetri sorunu** denir. Rastgele başlangıç simetriyi kırar: her
nöron farklı bir yerden başlar ve farklı bir şey öğrenir. Ağırlıkların
**ölçeği** de önemlidir; derin ağlarda katman genişliğine göre ayarlanan
başlangıçlar (Xavier, He gibi) kullanılır.
