Elinde iç içe sözlükle yazılmış bir karar ağacı (`tree`) ve etiketli beş
çiçek var. İki fonksiyon yaz:

- `predict(node, flower)`: kökten başla; `flower[feature] <= threshold`
  ise `left`'e, değilse `right`'a git. Düğüm sözlük olmadığı anda (yaprak)
  onu döndür.
- `accuracy(tree, flowers, labels)`: her çiçeği tahmin et, doğru tahminlerin
  oranını döndür (`doğru / toplam`).

Program her çiçeğin tahminini ve gerçeğini, sonra doğruluğu yazdırıyor.

**Beklenen çıktı:**

```
setosa setosa
versicolor versicolor
virginica virginica
virginica versicolor
virginica virginica
0.8
```
