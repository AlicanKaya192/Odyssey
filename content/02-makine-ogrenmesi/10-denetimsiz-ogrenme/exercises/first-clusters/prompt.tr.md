Bu bölümde ilk kez elinde bir `y` yok. 350 müşterinin dört sütunu var
ve kimse "bu müşteri şu tip" diye etiketlememiş.

Soru: **bu insanlar kaç gruba ayrılıyor ve grupları ne ayırıyor?**

**Yapman gerekenler:**

1. Veriyi oku, dört sütunu (`spend`, `visits`, `items`, `returns`) al ve
   **ölçekle**. K-ortalamalar uzaklığa dayanıyor — tıpkı KNN gibi.
2. `KMeans(n_clusters=4, random_state=42, n_init=10)` ile kümele.
3. Küme boyutlarını liste olarak yazdır.
4. Etiketi `cluster` adlı bir sütun yap ve **profil tablosunu** yazdır:
   her küme için dört sütunun ortalaması (bir ondalık).
5. Son satırda silüet skorunu yazdır (üç ondalık).

**Beklenen çıktı:**

```
[79, 102, 70, 99]
         spend  visits  items  returns
cluster
0        428.2    15.2   23.4      3.3
1         45.8     3.2    4.2      0.3
2         63.9    19.3    6.4      2.6
3        180.2     8.4   11.3      1.1
0.517
```

**Bu tablo alıştırmanın asıl çıktısı.** Küme numaraları hiçbir şey
anlatmıyor; anlatan şey ortalamalar:

- **Küme 1** — nadir gelen, az harcayan. 102 kişi.
- **Küme 3** — orta düzey, düzenli. 99 kişi.
- **Küme 0** — çok harcayan, çok alan. 79 kişi.
- **Küme 2 ilginç olan.** Harcaması küme 1 kadar düşük (63.9) ama ayda
  **19 kez** giriyor ve 2.6 iade yapıyor. Sık gelen, çok bakan, az alan,
  aldığını da geri veren biri. 70 kişi.

**Küme 2'yi gözle bulamazdın.** `spend` sütununa baksan küme 1 ile aynı
görünüyor; `visits` sütununa baksan küme 0 ile aynı. Ancak dördü birden
okununca ayrışıyor. Kümeleme tam olarak bunun için var.

**Silüet 0.517.** Şimdilik bu sayının iyi mi kötü mü olduğunu bilmiyorsun —
neye göre? Dördüncü alıştırmada karşılığını ölçeceksin.

**Dikkat:** `n_clusters` bir hiperparametre değil, bir **girdi**. Modele
"dört grup bul" dedin ve dört grup buldu. Üç deseydin üç bulurdu; verinin
kaç grup içerdiğine dair bir fikri yok.
