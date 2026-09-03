Önceki alıştırmada `k`'yı test tablosuna bakarak seçemeyeceğini gördün.
Bölüm 05'in kuralı: hiperparametre **çapraz doğrulamayla** seçilir.

Ama bu alıştırmada bir tuzak var ve tuzağın kendisi ders.

**Yapman gerekenler:**

1. Veriyi hazırla, ayır, ölçekle. `StratifiedKFold` kur (5 kat,
   `shuffle=True`, `random_state=42`).
2. Şu `k` değerleri için **yalnızca eğitim verisinde** çapraz doğrulama yap:
   **1, 3, 5, 7, 9, 15, 25**.
3. Her `k` için tek satır yazdır: **k, CV ortalaması, CV yayılımı** (üç
   ondalık).
4. **En yüksek ortalamaya sahip** `k`'yı bul.
5. **Gürültü eşiğini** hesapla: en iyi ortalamadan onun kendi yayılımını
   çıkar. Bu eşiğin üstünde kalan `k`'lardan **en büyüğünü** seç.
6. İki seçim için de test doğruluğunu yazdır: önce CV kazananı, sonra
   seçtiğin sağlam `k`. Her biri tek satır: **k, test doğruluğu**.

**Beklenen çıktı:**

```
1 0.913 0.04
3 0.893 0.039
5 0.9 0.052
7 0.873 0.057
9 0.88 0.062
15 0.893 0.053
25 0.88 0.054
1 0.82
25 0.92
```

**İlk yedi satıra bak.** En yüksek ortalama `k=1`'de: 0.913. Seçim tamam
gibi görünüyor.

**Şimdi yayılıma bak: 0.040.** En iyi ile en kötü ortalama arasındaki fark
da 0.040 (0.913 - 0.873). Yani **bütün `k` değerleri birbirinin gürültü
aralığında.** Çapraz doğrulama burada hiçbirini ayırt edemiyor.

Bölüm 05'in cümlesi: *"'Şu model daha iyi' demeden önce farkın yayılımdan
büyük olması gerekiyor."* Değilse seçim başka bir ölçütle yapılıyor — ve
KNN'de o ölçüt belli: **daha büyük `k` daha sağlam**, çünkü tek bir
komşuya bağlı değil.

**Son iki satır sonucu gösteriyor:**

```
CV kazanani  k=1   ->  test 0.820
saglam secim k=25  ->  test 0.920
```

**Naif seçim on puan kaybettiriyor.**

**Bu, çapraz doğrulamanın işe yaramadığı anlamına gelmiyor** — tam tersi.
Yayılımı da verdiği için "bu fark anlamsız" diyebildik. Yalnızca ortalamaya
bakan biri `k=1`'i seçer ve neden kaybettiğini de anlamazdı.
