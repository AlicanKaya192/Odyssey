Bir sınıflandırıcıyı en basit hâliyle kuracaksın: **yeni nokta, kendisine
en yakın komşusuna benzer.**

Elinde etiketli beş nokta ve etiketi bilinmeyen yeni bir nokta var.

**Yapman gerekenler:**

1. Yeni noktanın her noktaya olan mesafesini hesapla (Öklid mesafesi:
   farkların karelerinin toplamının karekökü).
2. Mesafeleri **küçükten büyüğe sıralı** olarak, iki ondalıkla ve liste
   hâlinde yazdır.
3. **En yakın** noktanın etiketini yazdır.
4. **En yakın üç** noktanın etiketlerini liste hâlinde yazdır.

**Beklenen çıktı:**

```
[0.71, 1.12, 5.66, 6.73, 7.11]
B
['B', 'B', 'A']
```

**Kurduğun şeyin adı var: KNN.** `k=1` alırsan en yakın komşunun etiketini
verirsin; `k=3` alırsan en yakın üçe bakıp çoğunluğa uyarsın. Son satırda
`['B', 'B', 'A']` çıktı: üçte iki çoğunlukla yine **B**.

`k`'yı sen seçiyorsun, model değil — buna **hiperparametre** deniyor.
Küçük `k` gürültüye duyarlı, büyük `k` sınırları bulanıklaştırıyor.

**Bir uyarı:** bu yöntem mesafeye bakıyor. Bir sütun 0-1, öteki 0-100.000
arasında olsaydı mesafeyi tek başına büyük sütun belirlerdi. 6. bölümün
konusu bu.
