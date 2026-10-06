Bir yılın artık yıl (Şubat'ın 29 çektiği yıl) olup olmadığını **tek bir
mantıksal ifadeyle** bul ve `is_leap` değişkenine koy:

```
1900 is a leap year: False
```

Kural üç parçalı:

1. 4'e tam bölünen yıllar artık yıldır…
2. …ama 100'e tam bölünenler **değildir**…
3. …ama 400'e tam bölünenler yine **artık yıldır**.

Yani `2024` artık yıl, `1900` değil (100'e bölünüyor), `2000` artık yıl
(400'e bölünüyor).

"Tam bölünür" `%` ile anlaşılır: `year % 4 == 0`. Parçaları `and`, `or` ve
gerekirse parantezle birleştir.

Kodun `1900` için `False` vermeli. Bitince `year`'ı `2000`, `2024` ve
`2023` yapıp dene: sırasıyla `True`, `True`, `False` çıkmalı. Sonra `1900`'e
geri döndür.

> Dikkat: Yalnızca `year % 4 == 0` yazarsan `1900` için de `True` çıkar.
> Kuralın üç parçasının üçü de ifadede olmalı.
