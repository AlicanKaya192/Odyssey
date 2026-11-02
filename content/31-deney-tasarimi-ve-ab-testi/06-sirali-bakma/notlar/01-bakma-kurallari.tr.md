## Bakış sayısına göre Bonferroni eşiği

```python
for looks in [1, 2, 7, 14]:
    print(looks, round(0.05 / looks, 4))
```

```text
1 0.05
2 0.025
7 0.0071
14 0.0036
```

Bonferroni her zaman güvenlidir ama bakışlar aynı birikmiş veriye
baktığı için gereğinden sıkıdır. Benzetimle ayarlanmış eşik (Pocock tipi)
ya da O'Brien–Fleming sınırları daha az güç kaybettirir.

## Kurallar

| Yapılabilir | Yapılmaz |
|---|---|
| Sonucu planlanan son günde okumak | Her gün p'ye bakıp anlamlı olunca durmak |
| Koruma metriği bozulunca durmak | "Biraz daha bekleyelim" diye süreyi uzatmak |
| Önceden yazılmış ardışık tasarımla erken durmak | Ardışık eşikleri test sırasında seçmek |
| Panoda gidişatı izlemek (karar vermeden) | Ara sonucu ekibe "kazanıyoruz" diye duyurmak |

## Plana yazılacaklar

- Kaç kez bakılacak, hangi günlerde.
- Her bakışın eşiği.
- Erken durma yalnızca kazanç için mi, zarar için de mi.
- Süre sonunda karar nasıl verilecek.
