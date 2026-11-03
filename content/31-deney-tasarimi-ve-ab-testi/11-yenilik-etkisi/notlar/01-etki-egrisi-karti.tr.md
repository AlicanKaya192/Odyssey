## Eğrinin yönünü okumak

```python
def trend(weekly_lifts, tol=0.01):
    change = weekly_lifts[-1] - weekly_lifts[0]
    if change < -tol:
        return "novelty"
    if change > tol:
        return "learning"
    return "stable"


print(trend([0.136, 0.066, 0.048, 0.052]))
print(trend([-0.03, 0.0, 0.02, 0.03]))
print(trend([0.04, 0.05, 0.04, 0.045]))
```

```text
novelty
learning
stable
```

Bu kaba bir okumadır: haftalık artışlar da gürültülüdür, `tol` gürültüden
küçük seçilirse her eğri "değişiyor" görünür. Eğri her zaman çizilip
gözle de bakılır.

## İki etki yan yana

| | Yenilik etkisi | Öğrenme etkisi |
|---|---|---|
| Neden | merak, "yeni bir şey" | alışkanlık, direnç |
| İlk günler | etki büyük görünür | etki küçük, hatta negatif |
| Zamanla | söner | büyür |
| Kısa test | iyimser | kötümser |
| Yeni kullanıcılar | etkilenmez | etkilenmez |

## Hızlı kurallar

- En az iki tam hafta; eğri düzleşmeden karar yok.
- Etkiyi gün ya da hafta başına çiz.
- Yeni kullanıcı kohortunu ayrı oku.
- Kalıcı etki için tutma grubu.
