Her mağazanın haftalık toplamını uzun biçimde hesapla.

**Yapman gerekenler:**

1. `stores.csv` dosyasını oku.
2. Mağaza ve hafta bazında toplamı hesapla:
   `long.groupby(["store", pd.Grouper(key="date", freq="W")])["sales"].sum()`.
3. Sonuçtaki satır sayısını yazdır.
4. A mağazasının ilk iki haftasını liste olarak yazdır
   (`weekly.loc["A"].head(2).tolist()`).
5. Her mağaza için en yüksek haftalık toplamı ve o haftanın etiketini
   (`"%Y-%m-%d"`) `mağaza tarih toplam` biçiminde alt alta yazdır.

**Beklenen çıktı:**

```
195
[2296, 2297]
A 2024-12-29 2590
B 2024-01-14 1393
C 2024-01-07 1666
D 2024-12-22 1618
```

Dört mağazanın da tepesi yıl sonu–yıl başı döneminde: ortak bir yıllık
mevsimsellik paylaşıyorlar. Ama büyüyen A ve D tepeyi Aralık'ta, büyümeyen B ve
C Ocak'ta yapıyor: trend, mevsimin hangi ucunun daha yüksek olacağını
belirliyor. Satır sayısı 4 × 53'ten az, çünkü D yılın ortasında açıldı.
