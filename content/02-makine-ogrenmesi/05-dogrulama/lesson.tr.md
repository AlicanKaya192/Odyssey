# Doğrulama ve Aşırı Öğrenme

Şimdiye kadar her bölümde tek bir sayı ölçtük: test kümesindeki hata. Bu
bölümde o sayının **ne kadar güvenilir** olduğunu soracağız.

İki soru var ve ikisi de aynı yere çıkıyor:

- Model ezberliyor mu, öğreniyor mu?
- Ölçtüğüm sayı gerçek mi, yoksa şansın eseri mi?

## İki skor, dört durum

Bölüm 01'den beri yalnızca test skoruna bakıyorduk. Eğitim skorunu da
yanına koyunca model hakkında çok daha fazla şey görünüyor.

<figure class="fig">
  <div class="versus">
    <div class="versus-side">
      <h4>Aşırı öğrenme</h4>
      <p>Eğitim <b>çok iyi</b>, test <b>kötü</b>.<br>Model ezberledi; kuralı çıkaramadı.</p>
    </div>
    <div class="versus-side">
      <h4>Yetersiz öğrenme</h4>
      <p>İkisi de <b>kötü</b>.<br>Kural fazla basit kaldı.</p>
    </div>
  </div>
  <figcaption>Tek başına test skoru bu ikisini ayırt edemiyor: %62 hem ezberlemiş hem de hiç öğrenememiş bir modelden gelebiliyor. Çözüm farklı.</figcaption>
</figure>

Ayrımın pratik değeri şu: **iki durumun çözümü birbirinin tersi.**

- Aşırı öğrenmede modeli **basitleştiriyorsun** ya da veri ekliyorsun.
- Yetersiz öğrenmede modeli **karmaşıklaştırıyorsun** ya da özellik
  ekliyorsun.

Yanlış teşhis, seni ters yöne götürüyor.

## Karmaşıklık düğmesi

Karar ağacının `max_depth` değeri, karmaşıklığı doğrudan ayarlıyor. Aynı
veride derinliği artırırken iki skoru birden izleyelim:

```
derinlik   egitim   test
       1    99.68   96.65
       2    72.72   58.47
       3    51.34   65.30
       5    18.25   53.83
       8     0.19   56.83
    none     0.00   59.06
```

**Eğitim sütunu sıfıra kadar iniyor.** Derinlik sınırı kalkınca ağaç her
kaydı ayrı bir dalda ezberliyor ve eğitim verisinde **sıfır hata** yapıyor.

**Test sütunu inmiyor.** 53 ile 96 arasında geziniyor ve hiçbir zaman
50'nin altına düşmüyor.

**Aradaki uçurum aşırı öğrenmenin kendisi.** Derinlik 1'de fark -3.03
(model o kadar basit ki ikisinde de aynı derecede kötü), derinlik sınırsızda
**59.06**.

Sıfır eğitim hatası gördüğünde sevinilmiyor; o sayı modelin veriyi
ezberlediğini söylüyor, öğrendiğini değil.

## Test sütununa dikkatlice bak

Şimdi asıl mesele. Test sütunu şöyle gidiyor:

```
96.65 → 58.47 → 65.30 → 53.83 → 56.83 → 59.06
```

Derinlik 2'de 58.47, 3'te 65.30, 5'te 53.83. **Düzgün bir eğri değil,
zıplıyor.**

Hangi derinlik en iyi? Tabloya bakıp "5" demek kolay. Ama 27 kayıtlık bir
test kümesinde bu sayılar arasındaki 5 birimlik farklar, gerçek bir üstünlük
mü yoksa hangi 27 aracın teste düştüğüyle ilgili bir tesadüf mü?

Bu soruyu cevaplamadan derinlik seçmek, gürültüye göre karar vermek oluyor.

## Tek bir ayrım ne kadar şanslı

Deneyelim: aynı model, aynı veri, yalnızca `random_state` değişiyor.

```
random_state   0      1      2      3      4
MAE          16.16  16.95  17.07  19.68  21.56
```

**En düşük 16.16, en yüksek 21.56.** Aradaki fark **5.40** — yani sayının
kendisinin üçte biri kadar.

Model değişmedi, veri değişmedi. Değişen tek şey hangi 27 aracın teste
düştüğü.

Bu, önceki bölümlerde ölçtüğümüz her sayının üstünde duran bir uyarı:
**tek bir ayrımdan gelen sonuç bir tahmindir, kesin bir ölçüm değil.**
`random_state=42` yazmak sonucu tekrarlanabilir yapıyor ama daha doğru
yapmıyor.

## Çapraz doğrulama

Çözüm basit: bir kez değil, **birçok kez** ölç ve ortalamasını al.

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">1. tur</span><span class="anat-body">veri beşe bölünüyor; <b>1. parça test</b>, kalan dördü eğitim</span></div>
    <div class="anat-row"><span class="anat-label">2. tur</span><span class="anat-body"><b>2. parça test</b>, kalan dördü eğitim</span></div>
    <div class="anat-row"><span class="anat-label">…</span><span class="anat-body">her parça sırayla bir kez test oluyor</span></div>
    <div class="anat-row"><span class="anat-label">sonuç</span><span class="anat-body">beş skorun <b>ortalaması</b> ve <b>yayılımı</b></span></div>
  </div>
  <figcaption>Her kayıt tam bir kez test ediliyor ve tam dört kez eğitimde kullanılıyor. Veri boşa gitmiyor.</figcaption>
</figure>

```python
from sklearn.model_selection import KFold, cross_val_score

kf = KFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(model, X, y, cv=kf,
                         scoring="neg_mean_absolute_error")
```

```
kat skorlari: [14.97, 15.96, 19.29, 19.63, 12.64]
ortalama 16.50   yayilim (std) 2.65
```

**İki sayı birden çıkıyor ve ikincisi en az birincisi kadar değerli.**

- **16.50** modelin beklenen hatası.
- **2.65** o sayının ne kadar oynadığı.

Yayılım büyükse elindeki sayıya az güveniyorsun demektir. İki modelin
ortalaması 16.5 ve 17.2 ise ve yayılımları 2.65 ise, aradaki 0.7'lik farkın
bir anlamı yok.

**`neg_` öneki tuhaf ama sebebi var:** sklearn her skoru "büyük olan iyidir"
diye ele alıyor. Hata için bu ters olduğundan işaret çevriliyor. Sonuçlar
negatif geliyor ve okunurken başına eksi konuyor.

**`shuffle=True` genelde gerekiyor:** dosya bir sütuna göre sıralıysa,
karıştırmadan bölmek katları birbirinden çok farklı hâle getiriyor.

## Nereye ne bakılır: üç parça

Çapraz doğrulama nereye oturuyor? Bunun için verinin üç işi olduğunu
hatırlamak gerekiyor.

<figure class="fig">
  <div class="flow">
    <span class="node acc"><b>Eğitim</b><br>model öğreniyor</span>
    <span class="arrow">+</span>
    <span class="node"><b>Doğrulama</b><br>ayar seçiliyor</span>
    <span class="arrow">+</span>
    <span class="node ok"><b>Test</b><br>bir kez ölçülüyor</span>
  </div>
  <figcaption>Ayarı test kümesine bakarak seçmek, testi eğitim verisine çevirir. Üçüncü kutuya yalnızca en sonda, bir kez bakılıyor.</figcaption>
</figure>

Veri bolsa üçe bölünüyor. Az veride üçe bölmek pahalı: 106 satırı üçe
ayırınca her parça çok küçük kalıyor.

**Çapraz doğrulama doğrulama kümesinin yerini alıyor.** Eğitim tarafında
tekrar tekrar bölünüp ölçülüyor, test kümesi hiç dokunulmadan bekliyor.

Sıra şöyle:

1. Veriyi eğitim ve test diye ayır. Testi bir kenara koy.
2. Ayarları **eğitim tarafında çapraz doğrulamayla** seç.
3. Seçtiğin ayarla modeli bütün eğitim verisinde eğit.
4. Test kümesinde **bir kez** ölç ve o sayıyı raporla.

## Öğrenme eğrisi: daha çok veri işe yarar mı?

Bir modelin başarısı yetersizse iki yol var: **daha çok veri** ya da **daha
iyi model**. Hangisinin işe yarayacağını öğrenme eğrisi söylüyor.

Eğitim verisinin bir kısmını kullanarak modeli tekrar tekrar eğitiyoruz:

```
kayit   egitim   test
   10    10.10   19.40
   20    11.80   18.59
   30    13.87   18.22
   45    15.45   18.01
   60    16.33   16.75
   79    15.52   15.69
```

**İki eğri birbirine doğru gidiyor.** Eğitim hatası **yükseliyor** (10 kayıtla
ezberlemek kolay, 79 kayıtla değil), test hatası **düşüyor**, ve sonunda
buluşuyorlar: 15.52 ile 15.69.

<figure class="fig">
  <div class="versus">
    <div class="versus-side">
      <h4>Eğriler buluştuysa</h4>
      <p>Daha çok veri <b>işe yaramaz</b>.<br>Gereken: yeni özellik ya da farklı model.</p>
    </div>
    <div class="versus-side">
      <h4>Arada açıklık kaldıysa</h4>
      <p>Model ezberliyor.<br>Daha çok veri <b>işe yarar</b>.</p>
    </div>
  </div>
  <figcaption>Öğrenme eğrisi "veri mi toplayayım, model mi değiştireyim" sorusunu tahmin etmek yerine ölçmeyi sağlıyor.</figcaption>
</figure>

Buradaki cevap net: iki eğri buluştu, yani bu modelden bu veriyle
alınabilecek alındı. Yüz araba daha toplamak sonucu değiştirmeyecek.

## Karmaşık model daha iyi model değil

Bu bölümün sessiz bulgusu şu. Aynı veride çapraz doğrulamayla ölçelim:

```
karar agaci (derinlik 5)   MAE 64.33
karar agaci (sinirsiz)     MAE 66.21
dogrusal regresyon         MAE 16.50
```

**Ağaç, düz bir doğrunun dörtte biri kadar bile iyi değil.**

Sebep basit: bu veride fiyat gerçekten metrekare, yaş ve kilometreyle
**doğrusal** ilişkili. Doğrusal regresyon o ilişkiyi tam olarak
yakalıyor; ağaç ise onu basamak basamak taklit etmeye çalışıyor ve 106
satırla yeterince basamak kuramıyor.

Alınacak ders: **model seçimi bir moda değil, bir ölçüm işi.** Daha
karmaşık olan, daha iyi olan demek değil.

## Bu bölümde neyi atladık

- **Ayar aramayı otomatikleştirmek.** Elle döngü yazmak yerine
  `GridSearchCV` bütün ayar birleşimlerini çapraz doğrulamayla deneyip en
  iyisini seçiyor. 11. bölümde geliyor.
- **Sınıflandırmada katlama.** Sınıflar dengesizse `KFold` yerine
  `StratifiedKFold` kullanılıyor: her kat sınıf oranını koruyor.
- **Zaman serisi.** Orada rastgele katlama geleceği geçmişe sızdırıyor;
  `TimeSeriesSplit` gerekiyor.

Şimdilik elinde iki alışkanlık var: **iki skoru birden bak** ve **tek bir
ayrımdan gelen sayıya fazla güvenme.** İkisi de sonraki her bölümde
geçerli.
