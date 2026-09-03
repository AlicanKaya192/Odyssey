Grafiklerin çoğu hatası **kod hatası değil, anlatım hatası.** Kod çalışıyor,
grafik çıkıyor ve okuyan kişi yanlış bir sonuç çıkarıyor.

## 1. Eksen sıfırdan başlamıyor

Değerler 85, 87 ve 88 olduğunda matplotlib ekseni 84'ten başlatabiliyor.
Aradaki %3'lük fark ekranda **üç kat** gibi görünüyor.

Bu, yanıltıcı grafik üretmenin en kolay yolu ve çoğu zaman kasıtsız oluyor.

**Çubuk grafikte** ekseni sıfırdan başlatmak kural sayılabilir:

```python
ax.set_ylim(0, 100)
```

Sebebi şu: çubuğun **uzunluğu** değeri temsil ediyor. Alt kısmı kesersen
uzunluk artık değerle orantılı olmuyor.

Çizgi grafiklerde bu kural yok — orada konu eğilim, mutlak büyüklük değil.

## 2. Başlıksız ve etiketsiz grafik

```python
ax.bar(x, y)
fig.savefig("chart.png")
```

Bu grafik neyi gösteriyor? Y ekseni adet mi, lira mı, yüzde mi? Okuyan kişi
tahmin etmek zorunda.

Bir grafik başkasına gösterilmek için çiziliyor; başlığı ve eksen etiketleri
onun cümlesi. Üç satır fazladan yazmak zorunda değilsin — **yazmak zorunda
olduğun şey bu.**

Birim özellikle unutuluyor: `set_ylabel("Satis (bin TL)")`.

## 3. Yanlış grafik türü

| Yanlış | Neden | Doğrusu |
|---|---|---|
| Kategorileri çizgiyle birleştirmek | Aralarında olmayan bir süreklilik anlatıyor | Çubuk |
| Zaman serisini çubukla | Eğilim görünmüyor | Çizgi |
| Beşten fazla dilimli pasta | Dilimler karşılaştırılamıyor | Çubuk |
| Dağılımı çubukla | Şekil kayboluyor | Histogram |

Pasta grafiği özellikle sorunlu: insan gözü açıları karşılaştırmakta kötü.
İki ya da üç dilimde iş görüyor, ötesinde çubuk her zaman daha okunaklı.

## 4. Çok fazla şey aynı grafikte

Sekiz çizgili bir grafik okunmuyor. Renkleri ayırt etmek, hangisinin
hangisi olduğunu takip etmek imkânsız hâle geliyor.

İki çözüm:

- **Vurgula:** ilgilendiğin seriyi renkli, gerisini gri çiz.
- **Böl:** `plt.subplots(2, 2)` ile dört ayrı küçük grafik.

Genel kural: bir grafik **bir şey** anlatıyor. İki şey anlatmak istiyorsan
iki grafik çiz.

## 5. `plt.bar()` ile `ax.bar()` karışıyor

```python
plt.bar(x, y)      # "su anki eksene" cizer
ax.bar(x, y)       # belirli bir eksene cizer
```

`plt` yazımı arkada gizli bir durum tutuyor: "şu an hangi eksen açık".
Tek grafikte sorun çıkarmıyor ama iki grafik çizdiğinde hangisine
yazdığın karışıyor.

**`fig, ax` yazımı** her zaman açık ve tahmin gerektirmiyor. Öğreticilerde
`plt` yazımı yaygın çünkü kısa; kendi kodunda `ax` kullan.

## 6. Döngüde tuval kapatmamak

```python
for city in cities:
    fig, ax = plt.subplots()
    ...
    fig.savefig(f"{city}.png")
```

Yirmi şehir için yirmi açık tuval birikiyor ve matplotlib uyarı veriyor.

Kaydettikten sonra kapatmak gerekiyor:

```python
    plt.close(fig)
```

## 7. Ölçek yanıltması: farklı eksenler

İki grafiği yan yana koyup karşılaştırmak istiyorsun ama eksenleri farklı
aralıkta. Birinde 0-100, ötekinde 0-10 varsa **görsel karşılaştırma
anlamsız** oluyor.

```python
fig, (sol, sag) = plt.subplots(1, 2, sharey=True)
```

`sharey=True` iki grafiği aynı ekseni paylaşmaya zorluyor.

## 8. Aykırı değer bütün grafiği eziyor

Bir kayıt 10.000, diğerleri 10-50 arasındaysa histogram tek bir çubuk gibi
görünüyor; asıl dağılım ezilmiş oluyor.

Üç seçenek:

- Aykırıyı ayrı incele, ana grafikten çıkar (ve **bunu grafikte belirt**).
- Ekseni logaritmik yap: `ax.set_yscale("log")`.
- Ekseni sınırla: `ax.set_xlim(0, 100)` — ama o zaman veri kaybı görünmüyor.

Hangisini seçersen seç, okuyana söylemen gerekiyor.

## 9. Renk körlüğü

Kırmızı ve yeşil erkeklerin yaklaşık %8'i için ayırt edilemiyor. "Yeşil iyi,
kırmızı kötü" düzeni o kişiler için bilgi taşımıyor.

Çözümler: mavi-turuncu gibi güvenli çiftler, ya da rengin yanında **başka
bir işaret** (desen, kalınlık, doğrudan etiket).

Aynı sebeple bir grafiğin siyah beyaz basıldığında da okunabiliyor olması iyi
bir testtir.

## 10. Nedensellik iddiası

Dağılım grafiğinde noktalar bir çizgi oluşturuyorsa iki değişken **birlikte
hareket ediyor** demek. Birinin ötekine sebep olduğu anlamına gelmiyor.

Klasik örnek: dondurma satışı ile boğulma vakaları birlikte artıyor. İkisinin
sebebi de yaz.

Grafik başlığında "X, Y'yi artırıyor" yazmak bir **iddia**; grafik onu
kanıtlamıyor. "X ile Y arasındaki ilişki" dürüst başlıktır.

## 11. Kesilen etiketler

Uzun kategori adları alt alta binebiliyor ya da kenardan kesilebiliyor.

Üç çözüm:

```python
ax.tick_params(axis="x", rotation=45)   # dondur
ax.barh(x, y)                            # yatay cubuk
fig.savefig(..., bbox_inches="tight")   # kenari kirpma
```

Yatay çubuk uzun adlarda genelde en okunaklısı.

## 12. Grafiği ekranda göstermeye çalışmak

```python
plt.show()
```

Odyssey'de pencere yok; bu çağrı bir şey yapmıyor. `matplotlib.use("Agg")`
ile belleğe çiziliyor ve `fig.savefig(...)` ile dosyaya alınıyor.

Kendi bilgisayarında `show()` çalışıyor. Ama rapor üretiyorsan dosyaya
kaydetmek zaten daha kullanışlı: aynı grafiği tekrar üretmek için kodu
çalıştırman yetiyor.
