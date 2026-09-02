# Görselleştirme

Şu ana kadar sayılarla cevap verdin: ortalama 87, üç şehir, en yüksek Mina.
Bazı sorular için bu yetiyor. Bazıları içinse **bakmak** gerekiyor.

```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
```

`plt` de `pd` ve `np` gibi bir gelenek.

**`matplotlib.use("Agg")` satırı ne?** Grafiği ekranda göstermek yerine
belleğe çiziyor. Odyssey'de alıştırmaların penceresi yok, o yüzden bu satır
gerekiyor. Kendi bilgisayarında çalışırken yazmıyorsun.

## Neden grafik?

Aynı veriye iki şekilde bakalım:

```text
city    ortalama
Ankara      87.0
Izmir       71.3
Bursa       69.0
```

Bu tabloyu okumak için üç sayıyı karşılaştırman gerekiyor. Bir çubuk
grafikte aynı bilgi **tek bakışta** geliyor: Ankara belirgin şekilde önde,
diğer ikisi birbirine yakın.

Fark üç satırda küçük, otuz satırda büyük, üç yüz satırda tabloyu okumak
imkânsız.

<figure class="fig">
  <div class="versus">
    <div class="versus-side">
      <h4>Tablo</h4>
      <p>Kesin değerler. "Ankara tam olarak kaç?" sorusunu cevaplıyor.</p>
    </div>
    <div class="versus-side">
      <h4>Grafik</h4>
      <p>İlişkiler ve desenler. "Hangisi öne çıkıyor, bir eğilim var mı?" sorusunu cevaplıyor.</p>
    </div>
  </div>
  <figcaption>Biri ötekinin yerine geçmiyor. Raporda genelde ikisi birden oluyor: grafik dikkat çekiyor, tablo doğruluyor.</figcaption>
</figure>

## Şekil ve eksen

matplotlib'de iki kavram var:

```python
fig, ax = plt.subplots()
```

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">fig</span><span class="anat-body">tuval — kaydedilen, boyutu ayarlanan şey</span></div>
    <div class="anat-row"><span class="anat-label">ax</span><span class="anat-body">çizim alanı — çubuklar, çizgiler ve etiketler buraya giriyor</span></div>
  </div>
</figure>

Bir tuvalde birden fazla çizim alanı olabiliyor:

```python
fig, (sol, sag) = plt.subplots(1, 2)
```

Öğreticilerde `plt.bar(...)` gibi kısa yazımlar da göreceksin. O da çalışıyor
ama arkada "şu anki eksen" diye gizli bir durum tutuyor; iki grafik
çizdiğinde hangisine yazdığın karışıyor. **`fig, ax` yazımı açık ve
karışmıyor.**

## Çubuk grafik

Kategoriler arasında karşılaştırma için:

```python
data = pd.DataFrame({"city": ["Ankara", "Izmir", "Bursa"], "score": [87, 71, 69]})

fig, ax = plt.subplots()
ax.bar(data["city"], data["score"])
ax.set_title("Sehirlere gore ortalama not")
ax.set_xlabel("Sehir")
ax.set_ylabel("Not")
fig.savefig("chart.png")
```

Üç satırlık etiketleme isteğe bağlı gibi duruyor ama değil: **başlıksız ve
etiketsiz bir grafik eksik bir cümledir.** Onu gören kişi neye baktığını
bilmiyor.

## Çizgi grafik

Zaman içindeki değişim için:

```python
fig, ax = plt.subplots()
ax.plot(months, sales, marker="o")
```

Çubuk **kategorileri** karşılaştırıyor, çizgi **bir şeyin nasıl değiştiğini**
gösteriyor. Ayları çubukla çizmek de mümkün ama çizgi eğilimi daha iyi
anlatıyor.

`marker="o"` gerçek ölçüm noktalarını işaretliyor — aradaki çizgi bir
tahmin, noktalar veri.

## Histogram

Bir sayısal sütunun **dağılımı** için:

```python
fig, ax = plt.subplots()
ax.hist(data["score"], bins=10)
```

Histogram değerleri aralıklara bölüp her aralıkta kaç kayıt olduğunu
gösteriyor. Çubuk grafikten farkı: orada kategoriler var, burada **sayı
aralıkları**.

`describe()` sana ortalama ve medyanı veriyordu; histogram **şekli**
gösteriyor. İki tepe mi var, sağa mı yatık, uç değerler nerede — bunlar
sayılarda görünmüyor.

`bins` sayısı önemli: az verirsen ayrıntı kayboluyor, çok verirsen gürültü
görünüyor.

## Dağılım grafiği

İki sayısal sütun arasındaki **ilişki** için:

```python
fig, ax = plt.subplots()
ax.scatter(data["hours"], data["score"])
```

Her nokta bir kayıt. Noktalar bir çizgi oluşturuyorsa iki değişken birlikte
hareket ediyor demek.

**Dikkat:** birlikte hareket etmek, birinin ötekine sebep olduğu anlamına
gelmiyor. Dondurma satışı ile boğulma vakaları birlikte artıyor; ikisinin
sebebi de yaz.

## Etiketler pazarlık konusu değil

```python
ax.set_title("Sehirlere gore ortalama not")
ax.set_xlabel("Sehir")
ax.set_ylabel("Not (0-100)")
```

Bir grafik başkasına gösterilmek için çiziliyor. Başlık neye baktığını,
eksen etiketleri hangi birimde olduğunu söylüyor.

Birim özellikle önemli: "Satış" yazan bir eksen adet mi, lira mı, bin lira
mı? Okuyan kişi tahmin etmek zorunda kalıyor.

## Kaydetmek

```python
fig.savefig("chart.png", dpi=150, bbox_inches="tight")
```

- `dpi` çözünürlük; rapora koyacaksan 150 iyi bir değer.
- `bbox_inches="tight"` kenarlardaki fazla boşluğu kırpıyor; uzun etiketler
  kesilmesin diye.

`plt.show()` diye bir çağrı da var ama o pencere açıyor; Odyssey'de
çalışmıyor ve zaten dosyaya kaydetmek raporlama için daha kullanışlı.

## pandas'ın kısayolu

pandas'ın kendi `plot` metodu matplotlib'i arkada çağırıyor:

```python
data.plot(kind="bar", x="city", y="score")
```

Hızlı bakış için pratik. Ama üzerinde denetim az; başlık, renk ve düzen
gerektiğinde `fig, ax` yazımına dönülüyor.

## Hangi grafik?

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">Çubuk</span><span class="anat-body">kategorileri karşılaştır — şehirlere göre satış</span></div>
    <div class="anat-row"><span class="anat-label">Çizgi</span><span class="anat-body">zaman içindeki değişim — aylara göre satış</span></div>
    <div class="anat-row"><span class="anat-label">Histogram</span><span class="anat-body">tek sütunun dağılımı — notlar nasıl yayılmış</span></div>
    <div class="anat-row"><span class="anat-label">Dağılım</span><span class="anat-body">iki sütun arasındaki ilişki — çalışma saati ile not</span></div>
  </div>
</figure>

Yanlış grafik seçmek yanlış sonuç kadar kötü: kategorileri çizgiyle
birleştirmek, aralarında olmayan bir süreklilik olduğunu söylüyor.

## Bir uyarı: eksen sıfırdan başlamıyorsa

matplotlib çubuk grafiklerde ekseni verinin aralığına göre ayarlıyor.
Değerler 85, 87 ve 88 ise eksen 84'ten başlayabiliyor ve **küçük farklar
devasa görünüyor**.

Bu, farkında olmadan yanıltıcı grafik üretmenin en kolay yolu. Çubuk
grafikte ekseni sıfırdan başlatmak iyi bir alışkanlık:

```python
ax.set_ylim(0, 100)
```

Çizgi grafiklerde bu kural yok — orada asıl konu eğilim, mutlak büyüklük
değil.

## Özet

- **Grafik ilişki gösteriyor, tablo değer veriyor.** İkisi birbirinin yerine
  geçmiyor.
- `fig, ax = plt.subplots()` — `fig` tuval, `ax` çizim alanı. Açık yazım
  karışmıyor.
- **Çubuk** kategori, **çizgi** zaman, **histogram** dağılım, **dağılım
  grafiği** iki değişken arasındaki ilişki.
- **Başlık ve eksen etiketleri zorunlu**; birim yazılmazsa okuyan tahmin
  ediyor.
- `fig.savefig(...)` ile kaydediliyor; `dpi` ve `bbox_inches` işe yarıyor.
- Odyssey'de `matplotlib.use("Agg")` gerekiyor — pencere yok.
- **Çubuk grafikte ekseni sıfırdan başlat**, yoksa küçük farklar büyük
  görünüyor.
- Birlikte hareket etmek **nedensellik değil**.
