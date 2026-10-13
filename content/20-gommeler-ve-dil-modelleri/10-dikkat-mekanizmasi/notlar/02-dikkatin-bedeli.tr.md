Dikkat her kelimeyi her kelimeyle karşılaştırır. Bir cümlenin bütün
kelimeleri birbirine dikkat ettiğinde (kendi kendine dikkat, bir sonraki
bölüm) n kelime için n × n puan hesaplanır. RNN ise n adım atar.

```python
for n in [10, 100, 1000, 10000]:
    scores = n * n
    memory_mb = scores * 4 / 1e6
    print(f"{n:>6} {scores:>12,} {memory_mb:>10.1f} MB")
```

```text
    10          100        0.0 MB
   100       10,000        0.0 MB
  1000    1,000,000        4.0 MB
 10000  100,000,000      400.0 MB
```

- 1000 kelimelik bir metinde bir milyon, 10 000 kelimede yüz milyon puan;
  her puan 4 baytlık bir sayıysa yalnızca bir dikkat tablosu 400 MB.
  Gerçek modellerde bu tablo her katmanda ve her "başta" (bir sonraki
  bölüm) yeniden hesaplanır.
- Bu kare büyüme, dil modellerinin bir anda okuyabildiği metin uzunluğunu
  (bağlam penceresi) sınırlayan başlıca sebeplerden biri. Uzun metinler için
  seyrek dikkat, kayan pencere ya da tabloyu parça parça hesaplayan
  yöntemler geliştirildi.
- Buna karşılık dikkat **paraleldir**: n × n puanın hepsi aynı anda
  hesaplanabilir. RNN'de her adım bir öncekini beklemek zorunda. Büyük
  modellerin dikkatle kurulmasının ana sebebi bu paralellik.
