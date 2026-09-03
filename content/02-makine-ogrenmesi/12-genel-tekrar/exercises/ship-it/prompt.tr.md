Son alıştırma. Modeli ayarla, kaydet, geri yükle ve **ham hasta
kayıtlarıyla** tahmin üret.

**Yapman gerekenler:**

1. Veriyi hazırla ve ayır (`followup_calls` yok, `stratify=y`).
2. Pipeline kur: ön işleyici + `LogisticRegression(max_iter=1000,
   class_weight="balanced")`.
3. `GridSearchCV` ile ara (`StratifiedKFold` 5 kat, `shuffle=True`,
   `random_state=42`, `scoring="average_precision"`):
   - `model__C`: `[0.01, 0.1, 1, 10]`
   - `prepare__num__impute__strategy`: `["median", "mean"]`
4. En iyi `C`, en iyi strateji ve CV skorunu tek satırda yazdır.
5. En iyi pipeline'ı `model.joblib` olarak kaydet; dosyanın 1000 bayttan
   büyük olduğunu yazdır.
6. Geri yükle. Test kümesindeki ortalama precision'ı yazdır.
7. Üç yeni hastadan oluşan bir `DataFrame` kur:
   - 72 / male / south / bmi 34.5 / visits 5 / smoker yes
   - 29 / female / **bilinmeyen bölge** / **bilinmeyen bmi** / visits 0 /
     smoker no
   - 58 / female / north / bmi 26.0 / visits 2 / smoker no
8. Üç hastanın olasılıklarını yazdır (üç ondalık).
9. Son satırda **0.3 eşiğiyle** üretilen tahminleri yazdır.

**Beklenen çıktı:**

```
0.01 median 0.541
True
0.444
[0.825, 0.234, 0.426]
[1, 0, 1]
```

**Birinci satır: `C=0.01` ve `median`, CV skoru 0.541.** Sekiz noktanın
tamamı 0.533 ile 0.541 arasında sıkışmış; ayarsız hâl (`C=1`, `median`)
0.534 veriyor. **Kazanç 0.007 ve yayılım 0.031** — yani arama pratikte bir
şey değiştirmedi.

Bu bir başarısızlık değil, bir bilgi: bu veride `C` ve doldurma stratejisi
önemli değil. İyileşme başka yerden gelmeli.

**İkinci ve üçüncü satır:** model kaydedildi, geri yüklendi ve test
kümesinde 0.444 verdi.

**Dördüncü satır asıl sınav.** İkinci hastanın `bmi` ve `region` sütunları
boş. Ona ham bir sözlük verdin — ölçeklenmemiş sayılar, kodlanmamış metin,
eksik değerler.

Model çalıştı, çünkü kaydedilen şey katsayılar değil **bütün pipeline**:
eğitimde hesaplanan medyan, mod, kodlayıcının kategorileri, ölçek
değerleri ve sütun sırası.

**Olasılıklar okunabiliyor:**

- Birinci hasta **0.825** — 72 yaşında, sigara içiyor, BMI 34.5, beş
  ziyaret. Dört risk faktörü birden.
- İkinci hasta **0.234** — 29 yaşında, sigara içmiyor, hiç ziyaret yok.
  Eksik iki sütun eğitimde öğrenilen medyan ve modla dolduruldu.
- Üçüncü hasta **0.426** — ortalarda ve kararsız.

**Son satır eşiğin işi.** `predict()` çağırsaydın 0.5 kullanacak ve
sonuç `[1, 0, 0]` olacaktı. **0.3 eşiğiyle üçüncü hasta da 1'e dönüyor**:
`[1, 0, 1]`.

Aynı model, aynı olasılıklar, farklı karar — ve o kararı veren tek şey
0.5 yerine 0.3 yazmak.

Bu eşik `joblib` dosyasında **yok**. `predict()` her zaman 0.5 kullanıyor.
Seçtiğin eşiği not etmezsen, modeli kullanan bir sonraki kişi sessizce
başka bir modeli çalıştırmış olacak.

**İşte bu yüzden dosyanın yanına bir not konuyor** — ikinci ders notu
nasıl yazılacağını anlatıyor.

Modülün sonundasın. Bir modeli kurmayı, dürüstçe ölçmeyi, sızıntıdan
korumayı ve teslim etmeyi biliyorsun.
