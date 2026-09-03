Hedef ilk kez bir **kategori**: öğrenci geçti mi (`1`) kaldı mı (`0`).
Akış aynı, model ve ölçü değişiyor.

`students.csv` dosyasında 160 öğrenci var; sütunlar `hours` (çalışma
saati), `prev_score` (önceki not), `attendance` (devam yüzdesi) ve
`passed`.

**Yapman gerekenler:**

1. Gereken her şeyi içe aktar ve dosyayı oku. Model **`LogisticRegression`**
   (`max_iter=1000` ver, yoksa uyarı çıkıyor).
2. Üç sütunu `X`'e, `passed`'i `y`'ye al.
3. Ayır: dörtte biri test, `random_state=42`, ve **`stratify=y`**.
4. Eğitim ve test kayıt sayılarını yan yana yazdır.
5. **Taban çizgiyi** kur: en sık görülen sınıfı her test kaydı için tahmin
   et ve doğruluğunu hesapla.
6. Modeli eğit, doğruluğunu hesapla. Taban çizgi ile model doğruluğunu
   **yan yana** yazdır (üç ondalık).
7. Model taban çizgiyi geçtiyse `better`, geçemediyse `worse` yazdır.

**Beklenen çıktı:**

```
120 40
0.675 0.85
better
```

**`stratify=y` yeni.** Sınıf oranını eğitim ve testte aynı tutuyor.
Olmasaydı rastgele ayrım testte 30 geçen 10 kalan, eğitimde başka bir oran
bırakabilirdi — ölçüm o zaman ayrımın şansına bağlı olurdu.
Sınıflandırmada neredeyse her zaman veriliyor.

**İkinci satır bu alıştırmanın konusu.** Taban çizgi **%67.5** — çünkü
öğrencilerin çoğu geçiyor ve "herkes geçti" diyen bir satır bile üçte
ikisini tutturuyor.

Modelin %85'i ancak bunun yanında anlam kazanıyor. Sınıflar dengesizken
doğruluk tek başına neredeyse hiçbir şey söylemiyor: bir sınıf %95 olsaydı,
hiçbir şey öğrenmeyen satır **%95 doğru** olurdu.
