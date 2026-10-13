Ağırlıkları neden rastgele başlattık? Hepsini sıfırla başlatıp dersteki
`forward`, `backward` ve eğitim döngüsüyle on tur eğitelim:

```python
def train(P, epochs=10, seed=1):
    rng = np.random.default_rng(seed)
    for _ in range(epochs):
        order = rng.permutation(len(y_train))
        for start in range(0, len(order), 32):
            batch = order[start:start + 32]
            grads = backward(P, A_train[batch], y_train[batch])
            for name in P:
                P[name] -= 0.5 * grads[name]
    return round(float((predict(P, A_test) == y_test).mean()), 3)


zeros = {name: np.zeros_like(value) for name, value in params.items()}
print(train(zeros))
print(np.bincount(predict(zeros, A_test)), round(float((y_test == 2).mean()), 3))
```

```text
0.66
[  0   0 500] 0.66
```

- Sıfırla başlayan ağ her yoruma "olumlu" diyor; doğruluğu taban çizgisi
  kadar. Hiçbir şey öğrenmedi.
- Sebep: `W1` ve `W2` sıfırsa gizli katman hep 0, geri gelen türev de 0.
  Yalnızca çıkış sabiti (`b2`) öğreniyor; o da en sık sınıfı seçiyor.
- Sıfır olmasa bile **eşit** başlangıç işe yaramaz: aynı değerle başlayan
  nöronlar aynı türevi alır ve hep aynı kalır (simetri). Rastgele başlangıç
  simetriyi bozar. Derste `W1` için `sqrt(2 / girdi)` ölçeği ReLU için
  önerilen başlangıçtır (He başlatması).
