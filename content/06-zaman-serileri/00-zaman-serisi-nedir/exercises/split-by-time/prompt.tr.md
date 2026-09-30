Veriyi eğitim ve test olarak ikiye ayır: **doğru yoldan** ve rastgele
ayırmanın ne kadar yanlış gittiğini ölçerek.

Veri zaten tarih sırasında. Zamana göre ayırmak için konuma göre kesmek
yetiyor: ilk %80 eğitim, geri kalanı test.

**Yapman gerekenler:**

1. `store_sales.csv` dosyasını oku.
2. Eğitimdeki satır sayısını `int(len(table) * 0.8)` ile bul. `iloc` ile ilk
   kısmı `train`, kalanı `test` yap.
3. Eğitimin son tarihini, testin ilk tarihini ve test satır sayısını aynı
   satıra yazdır.
4. Eğitimin en büyük tarihi, testin en küçük tarihinden küçük mü? Sonucu
   (`True` / `False`) yazdır.
5. Şimdi yanlış yolu dene: `train_test_split(table, test_size=0.2,
   random_state=0)`. Rastgele testte, rastgele eğitimin **en son
   tarihinden önce** kalan kaç gün var? Bu sayıyı ve test satır sayısını aynı
   satıra yazdır.

**Beklenen çıktı:**

```
2024-05-25 2024-05-26 220
True
219 220
```

Rastgele ayırmada test günlerinin neredeyse hepsi, modelin eğitimde
gördüğü bir günden önce. Model geleceği görmüş olarak sınanıyor.
