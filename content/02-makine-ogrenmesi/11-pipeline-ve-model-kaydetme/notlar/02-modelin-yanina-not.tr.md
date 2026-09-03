`joblib.dump` bir dosya üretiyor ve o dosya modelin **yarısı**. Öteki
yarısı, dosyanın yanına yazılan nottur.

Bu not olmadan altı ay sonra elinde adı `model.joblib` olan, ne yaptığı
belirsiz bir ikili dosya kalıyor.

## Neyin kaydedilmediği

| | |
|---|---|
| **Dosyada var** | Bütün adımlar, öğrenilmiş medyan/mod/ortalama, kodlayıcının kategorileri, model katsayıları, sütun sırası |
| **Dosyada yok** | Kütüphane sürümleri |
| **Dosyada yok** | Eğitim verisi ve nereden geldiği |
| **Dosyada yok** | Seçtiğin karar eşiği |
| **Dosyada yok** | Ölçtüğün skorlar ve hangi test kümesinde |
| **Dosyada yok** | Neyi kasten dışarıda bıraktığın |

Son satır sık atlanıyor ama en pahalısı. "Neden `age` sütununu
kullanmadık?" sorusunun cevabı altı ay sonra kimsenin aklında olmuyor.

## Yeterli bir not

Modelin yanına konan düz bir metin dosyası. Örnek:

```
model.joblib
============
Ne yapiyor : abone kaybi (churn) tahmini, ikili siniflandirma
Egitildigi : subscribers.csv, 600 satir, 2026-09 kopyasi
Girdi      : city, plan (metin) + tenure, monthly, support (sayi)
             ham veri veriliyor; eksik degerleri pipeline dolduruyor
Cikti      : 0 = kalir, 1 = ayrilir

Olculen    : taban cizgi 0.573
             capraz dogrulama 0.738 +/- 0.037 (5 kat, egitim tarafinda)
             test dogrulugu 0.793 (150 kayit, bir kez olculdu)

Esik       : 0.5 (varsayilan; is tarafi bir maliyet vermedi)
Ayar       : LogisticRegression(C=0.1), GridSearchCV ile secildi

Disarida   : musteri kimligi (kimlik, ogrenilecek bir sey yok)
             kayit tarihi (tenure ile ayni bilgiyi tasiyor)

Ortam      : scikit-learn 1.7, pandas 3.0, Python 3.14
             ayrintisi requirements.txt icinde

Bilinen sinirlar:
  - Bursa disindaki sehirler icin ornek sayisi az
  - 2026 oncesi veriyle test edilmedi
```

Yirmi satır. Yazması beş dakika, olmaması bir gün.

## Sürüm uyumu

`joblib` dosyası Python nesnelerini saklıyor. Farklı bir scikit-learn
sürümünde açmak:

- **Çalışabilir** (küçük sürüm farkı, uyarı verir)
- **Uyarı verip yanlış çalışabilir** (iç yapı değişmişse)
- **Hiç açılmayabilir** (sınıf kaldırılmışsa)

Bu yüzden modelin yanına `requirements.txt` konuyor:

```
scikit-learn==1.7.0
pandas==3.0.5
numpy==2.3.0
```

Uyarıyı görmezden gelmek yaygın bir hata. `InconsistentVersionWarning`
"muhtemelen sorun yok" demiyor; "kontrol et" diyor.

## Eşik dosyada değil

Bölüm 09'da eşiği 0.5'ten 0.1'e indirmenin yakalanan dolandırıcılığı
6'dan 13'e çıkardığını ölçmüştün.

**O eşik `joblib` dosyasına girmiyor.** `predict()` her zaman 0.5
kullanıyor. Seçtiğin eşik yalnızca senin kodunda duruyor:

```python
probability = loaded.predict_proba(new)[:, 1]
prediction = (probability >= 0.1).astype(int)
```

Bunu not etmezsen modeli kullanan bir sonraki kişi `predict()` çağırıyor
ve **sessizce başka bir modeli** çalıştırmış oluyor.

## Modelin yaşlanması

Üretimdeki veri zamanla eğitim verisinden uzaklaşıyor: fiyatlar değişiyor,
yeni bir şehir açılıyor, müşteri davranışı kayıyor. Model aynı kalıyor ve
**sessizce kötüleşiyor.**

Buna **kayma** (drift) deniyor ve iki türü var:

| Tür | Ne değişiyor | Örnek |
|---|---|---|
| Veri kayması | Girdilerin dağılımı | Ortalama abonelik ücreti iki katına çıkıyor |
| Kavram kayması | Girdi-hedef ilişkisi | Rakip çıkıyor, ucuz planlar da terk edilmeye başlıyor |

İkincisi daha sinsi: girdiler aynı görünüyor ama model artık yanlış.

**Pratikte ne yapılıyor:**

- Tahminlerin dağılımı izleniyor (birden herkese "ayrılır" demeye
  başladıysa bir şey olmuş demektir).
- Gerçek sonuçlar geldikçe skor yeniden ölçülüyor.
- Düzenli aralıkla yeniden eğitiliyor ve **eski modelle karşılaştırılıyor.**

Son madde önemli: yeni model her zaman daha iyi olmuyor.

## Dosyayı üretirken

- **Adına sürüm koy:** `churn-2026-09.joblib`. `model.joblib` üçüncü
  modelde karışıyor.
- **Eğitim betiğini sakla.** Modeli yeniden üretebilmek, dosyayı
  saklamaktan daha değerli.
- **Rastgele tohumu sabitle.** `random_state` olmadan aynı betik aynı
  modeli vermiyor.
- **Test skorunu bir kez ölç.** Test kümesine ikinci kez bakıp ayar
  değiştirirsen o skor artık dürüst değil.

## Tek cümle

**Kaydedilen dosya modelin ne yaptığını anlatmıyor; onu yanındaki not
anlatıyor.**
