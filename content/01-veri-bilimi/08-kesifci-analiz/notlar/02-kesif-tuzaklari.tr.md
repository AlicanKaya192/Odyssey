Bu bölümdeki hataların hiçbiri kod hatası değil. Kod çalışıyor, sayı
çıkıyor ve **sayıdan yanlış bir sonuç çıkarılıyor.**

## 1. Ortalamayı yayılım olmadan okumak

İki grubun da ortalaması 70. Birincide herkes 68-72 arasında, ikincide
yarısı 40, yarısı 100.

Aynı ortalama, tamamen farklı iki durum. `std` istemeden ortalama yarım
bilgi:

```python
data.groupby("city")["score"].agg(["count", "mean", "std"])
```

## 2. Küçük grubu ciddiye almak

```text
        count  mean
Bursa       2  48.0
```

İki kişilik bir grubun ortalaması hakkında söylenebilecek şey yok. Bir
kişi eksik ya da fazla olsa sayı tamamen değişirdi.

Kaba bir eşik: **30'un altındaki gruplarda** sayıyı bir sonuç olarak değil,
bir işaret olarak oku. Ve grup büyüklüğünü raporda mutlaka yaz.

## 3. Ortalamanın gruplarda tersine dönmesi

Bu, adı olan bir tuzak: **Simpson paradoksu**.

```text
team
A    74.0
B    61.0
```

A takımı önde görünüyor. Ama zorluk seviyesine göre ayırınca:

```text
team  level
A     easy     80.0
      hard     50.0
B     easy     85.0
      hard     55.0
```

**Her iki seviyede de B daha iyi.** Sebep dağılım: A çoğunlukla kolay
soruları çözmüş, B çoğunlukla zor olanları.

Toplam ortalama yalan söylemiyor, ama **eksik soruya cevap veriyor.**

Korunma yolu: bir grup farkı bulduğunda "bu grupların başka bir şeyi de
farklı mı" diye sor ve o sütuna göre de kır.

## 4. Korelasyonu nedensellik sanmak

En sık tekrarlanan hata.

`hours` ile `score` arasında 0.98 var. Ama aynı veride `age` ile `hours`
arasında da -0.89 var: yaşı büyükler daha az çalışmış. Notu düşüren yaş
mı, çalışma saati mi? Veri söylemiyor.

Üç ihtimal her zaman açık:

- A, B'ye sebep oluyor.
- B, A'ya sebep oluyor.
- C ikisine birden sebep oluyor.

Analiz üçünü ayırt edemiyor; ayırt etmek için deney gerekiyor.

## 5. Korelasyon 0 çıktı diye "ilişki yok" demek

Korelasyon **doğrusal** ilişkiyi ölçüyor. U şeklinde bir ilişkide
korelasyon 0'a yakın çıkıyor ama ilişki fazlasıyla var.

Bu yüzden sayıya bakmadan önce **dağılım grafiğine** bakılıyor. Aynı
korelasyon değerini veren tamamen farklı desenler çizilebiliyor.

## 6. Aykırı değeri düşünmeden silmek

```python
data = data[data["score"] < 1000]
```

Bu satır bir karar. Değeri silmeden önce sorulacak soru: **bu bir hata mı,
yoksa gerçek bir uç mu?**

- Yaş 200 → hata, silinebilir.
- Maaş ortalamanın 40 katı → belki genel müdür. Silersen veriyi
  çarpıtırsın.

Uç değerler bazen verinin en ilginç kısmı: dolandırıcılık tespiti tamamen
onların üstüne kurulu.

## 7. Eksik değeri rastgele sanmak

`dropna()` kolay bir çözüm gibi duruyor. Ama boşluklar rastgele
dağılmıyorsa **kalan veri artık temsil etmiyor.**

Ankette gelir sorusunu genelde yüksek gelirliler boş bırakıyor. Boşları
atınca ortalama gelir olduğundan düşük çıkıyor — hem de kimse fark
etmeden.

Sorulacak soru "kaç tane boş" değil, **"neden boş"**.

## 8. Yüzde yerine sayı, sayı yerine yüzde

"20 kayıt eksik" bilgi değil. 100 satırda 20 eksik ciddi, 100.000 satırda
20 eksik önemsiz.

Ters yönde de aynı: "%50 artış" 2'den 3'e çıkmışsa bir şey anlatmıyor.
**Yüzde ve ham sayı birlikte yazılıyor.**

## 9. Bir şey çıkana kadar aramak

Yirmi sütunu birbiriyle karşılaştırırsan içlerinden biri rastlantı eseri
yüksek korelasyon verir. Bulduğun şey veride değil, aramanda.

Dürüst yol: **soruyu önce sor**, sonra bak. Veriye bakarken doğan soruları
"bunu ayrıca doğrulamak gerekiyor" diye not et; bulguymuş gibi yazma.

## 10. Ortalamayı medyan yerine kullanmak

Gelir, süre, fiyat gibi sağa çarpık verilerde ortalama gerçeği anlatmıyor.
Birkaç büyük değer ortalamayı yukarı çekiyor ve "ortalama kullanıcı"
diye tarif ettiğin kişi veride hiç yok.

`describe()`'da `mean` ile `50%` uzaksa **medyanı yaz**.

## 11. Tipin sessizce yanlış olması

`score` sütunu `str` tipindeyse `sort_values()` çalışıyor ama **metin
sırasına** göre sıralıyor: `"100"` `"9"`'dan önce geliyor.

Hata yok, uyarı yok, sonuç yanlış. Bu yüzden ikinci adım `dtypes`.

## 12. Bulguyu iddiaya çevirmek

Raporun son cümlesi en tehlikeli yer:

| Veriden okunuyor | Fazladan iddia var |
|---|---|
| "Bu veride X ile Y birlikte hareket ediyor" | "X, Y'yi artırıyor" |
| "Bursa'daki iki kayıt düşük" | "Bursa'da notlar düşük" |
| "Ocak'ta satış arttı" | "Kampanya işe yaradı" |

Sağdaki cümleler yanlış olmak zorunda değil — ama **veri onları
kanıtlamıyor.** Analizin dürüstlüğü tam olarak bu farkı korumakta.
