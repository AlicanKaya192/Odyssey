Düzeyin hangi gün değiştiğini geriye dönük bul ve seriyi temizlemenin kanıtı
nasıl güçlendirdiğini ölç.

**Yapman gerekenler:**

1. `best_split(x, margin=14)` fonksiyonunu yaz: `x`'i numpy dizisine çevirsin;
   `margin` ile `len(x) - margin` arasındaki her `k` için iki parçanın kendi
   ortalamalarından sapmalarının kare toplamını hesaplasın; en küçüğü veren
   `k`'yi ve kazancı (`1 - en küçük toplam / bütün serinin kare toplamı`)
   döndürsün.
2. Ham seride (`v`) değişim gününü (`"%Y-%m-%d"`) ve kazancı (iki ondalık)
   yazdır.
3. Hafta sonu etkisini gider: `ratio`, hafta sonu günlerinin ortancasının hafta
   içi günlerinin ortancasına oranı (üç ondalıkla yazdır). `adjusted`, hafta
   sonu değerleri `ratio`'ya bölünmüş seri. Değişim gününü ve kazancı yazdır.
4. Üç anomali gününü de onar: `adjusted`'ın bir kopyasında 14 Mart, 20 Haziran
   ve 8 Ekim'i `NaN` yap ve `interpolate()` ile doldur (`clean`). Değişim
   gününü, kazancı, öncesinin ve sonrasının ortalamasını (tam sayı) ve yüzde
   değişimi (tam sayı) aynı satıra yazdır.
5. `clean`'in iki parçasına `best_split`'i yeniden uygula; iki kazancı üç
   ondalıkla aynı satıra yazdır.

**Beklenen çıktı:**

```
2024-09-02 0.3
0.723
2024-09-02 0.52
2024-09-02 0.88 4004 5235 31
0.013 0.015
```

Üç denemede de aynı gün bulunuyor, ama kazanç 0.30'dan 0.88'e çıkıyor: haftalık
desen ve anomaliler çıkarılınca düzey kayması oynamanın neredeyse tamamı. İki
parçanın içinde ikinci bir değişim yok: kazanç yüzde bir-iki. `best_split` her
zaman bir gün döndürür; karar kazançtan verilir.
