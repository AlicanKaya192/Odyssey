Teşhis iki skoru yan yana koymakla başlıyor. Tedavi teşhise göre değişiyor
ve **yanlış teşhis seni ters yöne götürüyor.**

## Teşhis tablosu

| Eğitim | Test | Durum | Yön |
|---|---|---|---|
| Çok iyi | Kötü | **Aşırı öğrenme** | Basitleştir |
| Kötü | Kötü | **Yetersiz öğrenme** | Karmaşıklaştır |
| İyi | İyi | Sorun yok | Dokunma |
| Kötü | İyi | Bir şeyler ters | Ayrımı ve kodu kontrol et |

Son satır nadir ve neredeyse her zaman bir hata işareti: kümelerin
karışması, sızıntı, ya da test kümesinin tesadüfen kolay olması.

## Aşırı öğrenme: yedi çözüm

**1. Modeli basitleştir.**

Karmaşıklığı doğrudan ayarlayan hiperparametreler var:

| Model | Ayar | Yön |
|---|---|---|
| Karar ağacı | `max_depth` | Küçült |
| Karar ağacı | `min_samples_leaf` | Büyüt |
| KNN | `n_neighbors` | Büyüt |
| Rastgele orman | `max_depth`, `min_samples_leaf` | Sınırla |
| Doğrusal model | `alpha` (Ridge/Lasso) | Büyüt |

**2. Daha çok veri topla.**

Öğrenme eğrisi bunun işe yarayıp yaramayacağını söylüyor: eğriler arasında
açıklık kalmışsa yarar, buluşmuşlarsa yaramaz.

**3. Özellik sayısını azalt.**

Özellik sayısı örnek sayısına yaklaştıkça ezber kolaylaşıyor. Hedefle
ilgisi zayıf sütunları çıkarmak modeli iyileştirebiliyor.

**Ama seçimi eğitim tarafında yap** — bütün veriye bakarak seçmek sızıntı.

**4. Düzenlileştirme (regularization) kullan.**

Doğrusal modellerde katsayıların büyümesini cezalandıran sürümler var:

```python
from sklearn.linear_model import Ridge, Lasso

model = Ridge(alpha=1.0)     # katsayilari kucultur
model = Lasso(alpha=0.1)     # bazi katsayilari sifira indirir
```

`alpha` büyüdükçe model basitleşiyor. **Bu modellerde ölçekleme
gerekiyor**, çünkü ceza katsayının büyüklüğüne bakıyor.

**5. Topluluk yöntemlerine geç.**

Rastgele orman, tek bir ağacın ezberini birçok ağacın ortalamasıyla
söndürüyor. 8. bölümün konusu.

**6. Erken durdur.**

Tur tur öğrenen modellerde (gradyan artırma, sinir ağları) doğrulama skoru
kötüleşmeye başladığında durmak.

**7. Gürültüyü azalt.**

Yanlış etiketler ve aykırı değerler ezberlenecek şey üretiyor. Veri
temizliği bir aşırı öğrenme tedavisi olarak da işe yarıyor.

## Yetersiz öğrenme: dört çözüm

**1. Modeli karmaşıklaştır.** Derinliği artır, komşu sayısını azalt,
doğrusal yerine ağaç dene.

**2. Özellik ekle.** Modelin bilmediği bir şeyi öğrenmesini bekleyemezsin.
Kalıntı grafiği hangi sütunun eksik olduğunu söylüyor (2. bölüm).

**3. Türetilmiş özellik üret.** İlişki eğriyse `x` yanına `x**2` koymak
doğrusal modelin eğri yakalamasını sağlıyor. İki sütunun çarpımı ya da
oranı da bilgi taşıyabiliyor.

**4. Düzenlileştirmeyi gevşet.** `alpha` çok büyükse model fazla
basitleşmiş olabiliyor.

## Karmaşıklık ve hata

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">çok basit</span><span class="anat-body">eğitim ve test hatası <b>ikisi de yüksek</b> — yetersiz öğrenme</span></div>
    <div class="anat-row"><span class="anat-label">dengede</span><span class="anat-body">test hatası <b>en düşük</b> noktada</span></div>
    <div class="anat-row"><span class="anat-label">çok karmaşık</span><span class="anat-body">eğitim hatası sıfıra iner, <b>test hatası yeniden yükselir</b></span></div>
  </div>
  <figcaption>Aranan şey test hatasının en düşük olduğu nokta; eğitim hatasının en düşük olduğu nokta değil.</figcaption>
</figure>

**Pratikte bu eğri düzgün çıkmıyor.** Küçük test kümelerinde sayılar
zıplıyor ve en düşük noktayı gözle seçmek gürültüye göre karar vermek
oluyor. Çapraz doğrulama tam olarak bu yüzden var.

## Karmaşık her zaman daha iyi değil

Bu modülün araba verisinde ölçüldü:

```
karar agaci (derinlik 5)   MAE 64.33
karar agaci (sinirsiz)     MAE 66.21
dogrusal regresyon         MAE 16.50
```

Doğrusal regresyon, karar ağacının dört katı iyi. Sebebi veri: fiyat
gerçekten doğrusal bir ilişkiyle belirleniyor ve ağaç onu basamak basamak
taklit etmeye çalışıyor.

**Model seçimi bir moda değil, bir ölçüm işi.** "Daha gelişmiş" bir model
denemeden önce basitini ölçmek, çoğu zaman zaman kazandırıyor.

## Kontrol listesi

Bir modeli iyileştirmeye başlamadan önce:

1. **İki skoru da ölçtün mü?** Yalnızca test skoru teşhis koydurmuyor.
2. **Taban çizgiyi geçiyor mu?** Geçmiyorsa mesele karmaşıklık değil.
3. **Çapraz doğrulama yaptın mı?** Tek ayrımdan gelen fark gürültü olabilir.
4. **Yayılıma baktın mı?** Ortalamalar arasındaki fark yayılımdan küçükse
   anlamı yok.
5. **Öğrenme eğrisi ne diyor?** Veri mi lazım, model mi?
6. **Kalıntılarda desen var mı?** Varsa eksik bir özellik var demektir.

Bu altı soruya cevap vermeden model değiştirmek, karanlıkta düğme
çevirmek.
