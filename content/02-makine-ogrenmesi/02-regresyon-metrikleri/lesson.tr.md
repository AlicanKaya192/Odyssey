# Regresyon Metrikleri

Önceki bölümde `18.5` çıktı ve taban çizgiye bakarak "iyi" dedik. Doğruydu,
ama eksikti.

Çünkü `18.5` bir **özet**. Özetin arkasında on tahmin var ve o tahminlerin
nasıl dağıldığı, ortalamalarından daha çok şey anlatıyor. Bu bölüm o
arkaya bakıyor.

## Her şey kalıntıyla başlıyor

Bir tahminin hatası, gerçek değerle tahmin arasındaki fark. Buna **kalıntı**
(residual) deniyor.

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">kalıntı</span><span class="anat-body"><code>gercek - tahmin</code> — tek bir kaydın hatası</span></div>
    <div class="anat-row"><span class="anat-label">pozitif</span><span class="anat-body">model <b>düşük</b> tahmin etmiş; gerçek daha yüksek çıkmış</span></div>
    <div class="anat-row"><span class="anat-label">negatif</span><span class="anat-body">model <b>yüksek</b> tahmin etmiş</span></div>
  </div>
  <figcaption>Bütün regresyon ölçüleri bu sayılardan türüyor. Farkları, kalıntıları nasıl topladıklarında.</figcaption>
</figure>

Sekiz tahminin kalıntıları şöyle olsun:

```
[12, -7, -15, 15, -15, 30, -8, 10]
```

Bu sekiz sayıyı **tek bir sayıya indirmenin** birden çok yolu var ve her
yol farklı bir şeye önem veriyor.

## MAE — ortalama mutlak hata

En doğrudan yol: işaretleri at, ortalamasını al.

```python
mae = sum(abs(e) for e in errors) / len(errors)   # 14.0
```

**Neden mutlak değer:** işaretler kalırsa +15 ile -15 birbirini götürüyor
ve model kusursuz görünüyor. Mutlak değer yanılmanın **yönünü** değil
**miktarını** ölçüyor.

MAE'nin en büyük avantajı okunabilirliği: birimi hedefin birimi. "Ortalama
14 bin lira yanılıyorum" cümlesi kurulabiliyor ve herkes anlıyor.

```python
from sklearn.metrics import mean_absolute_error
mae = mean_absolute_error(y_test, prediction)
```

## MSE ve RMSE — kareyi almak

İkinci yol: mutlak değer yerine **kare** al.

```python
mse = sum(e ** 2 for e in errors) / len(errors)   # 241.5
rmse = mse ** 0.5                                 # 15.54
```

Kare almak da işareti yok ediyor, ama bir yan etkisi var: **büyük hatalar
orantısız ağırlık kazanıyor.** 30'luk bir hata, 10'luk bir hatanın dokuz
katı ceza alıyor.

MSE'nin birimi hedefin biriminin karesi — "241.5 bin lira kare" diye bir
şey yok. Bu yüzden karekökü alınıyor: **RMSE** yine hedefin biriminde.

## Aynı MAE, çok farklı RMSE

Aradaki farkı en iyi gösteren örnek şu. İki model, gerçek değerlerin hepsi
100:

<figure class="fig">
  <div class="versus">
    <div class="versus-side">
      <h4>Model A</h4>
      <p>Her tahminde <b>10</b> yanılıyor.<br>MAE <b>10.0</b> · RMSE <b>10.0</b></p>
    </div>
    <div class="versus-side">
      <h4>Model B</h4>
      <p>Dokuzunu tam biliyor, birinde <b>100</b> yanılıyor.<br>MAE <b>10.0</b> · RMSE <b>31.62</b></p>
    </div>
  </div>
  <figcaption>MAE ikisini ayırt edemiyor. RMSE, B'nin tek büyük hatasını görüyor ve üç katı ceza veriyor.</figcaption>
</figure>

**Hangisi daha iyi bir model?** Cevap ölçüde değil, problemde.

- Bir teslimat süresi tahmininde on dakikalık sapmalar tolere edilebilir;
  ama tek bir tahminde 100 dakika yanılmak müşteriyi kaybettiriyor.
  **B kötü, RMSE haklı.**
- Bir toplam maliyet tahmininde küçük sapmalar birikiyor, tek bir büyük
  sapma ise ortalamada eriyor. **A kötü, MAE haklı.**

**Ölçüyü problem seçiyor, alışkanlık değil.** "Hangi ölçüyü kullanayım"
sorusunun cevabı, "büyük bir hata küçük hataların toplamından daha mı
pahalı" sorusunun cevabı.

## R² — birimsiz olan

MAE ve RMSE hedefin biriminde konuşuyor. Bu okunabilir ama bir sorun
doğuruyor: **iki farklı problemin sayıları karşılaştırılamıyor.** Ev fiyatı
tahmininde MAE 18.5, sıcaklık tahmininde MAE 2.1 — hangisi daha başarılı?

R² bu soruyu çözüyor, çünkü birimi yok:

```
R² = 1 - (modelin hatasi) / (taban cizginin hatasi)
```

Formülün açık hâli:

```python
mean = y_test.mean()
ss_res = sum((a - p) ** 2 for a, p in zip(y_test, prediction))
ss_tot = sum((a - mean) ** 2 for a in y_test)
r2 = 1 - ss_res / ss_tot        # 0.943
```

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">R² = 1</span><span class="anat-body">kusursuz; hiç hata yok</span></div>
    <div class="anat-row"><span class="anat-label">R² = 0.94</span><span class="anat-body">taban çizginin hatasının yalnızca %6'sı kalmış</span></div>
    <div class="anat-row"><span class="anat-label">R² = 0</span><span class="anat-body">taban çizgi kadar; öğrenilmiş bir şey yok</span></div>
    <div class="anat-row"><span class="anat-label">R² &lt; 0</span><span class="anat-body">taban çizgiden <b>kötü</b>; model atılıyor</span></div>
  </div>
  <figcaption>R²'nin sıfır noktası taban çizgi. Önceki bölümün taban çizgisi burada ölçünün içine gömülü.</figcaption>
</figure>

**Dikkat:** R²'nin sıfır noktası **test kümesinin kendi ortalaması**. Bu,
elle kurduğun taban çizgiden biraz farklı — sen eğitim ortalamasını
kullanıyordun. İki sayı yakın çıkıyor ama aynı değil.

**"R² yüzde kaç açıklıyor" cümlesine dikkat.** Yaygın ama gevşek bir
ifade. R² 0.94, "hedefteki değişkenliğin %94'ünü açıkladım" gibi
okunabiliyor; ama bu bir **açıklama** değil, bir uyum ölçüsü. Model neyi
neden açıkladığını bilmiyor.

## MAPE — yüzdeyle konuşmak

Bir ölçü daha: hatayı gerçek değere oranlayıp yüzde vermek.

```python
mape = sum(abs((a - p) / a) for a, p in zip(actual, predicted)) / len(actual)
```

Anlaşılır: "ortalama %8 yanılıyorum". Ama iki tuzağı var:

- **Gerçek değer sıfırsa bölme patlıyor.** Satış tahmininde sıfır satılan
  gün varsa MAPE hesaplanamıyor.
- **Simetrik değil.** 100 yerine 50 demek %50 hata; 100 yerine 150 demek de
  %50 hata. Ama 100 yerine 200 demek %100, 100 yerine 0 demek yine %100.
  Düşük tahmin etmenin cezası üstten sınırlı, yüksek tahmin etmeninki
  değil. Model bunu fark ediyor ve **sistematik olarak düşük tahmin
  etmeye** kayıyor.

Kullanılıyor, ama körü körüne değil.

## Kalıntılara bakmak: asıl iş burada

Ölçüler bir sayı veriyor. **Kalıntıların kendisi** ise nerede yanıldığını
gösteriyor — ve bu genelde daha kullanışlı.

Önceki bölümün tek özellikli modelinde en büyük hata hangi evde çıkmıştı?

```
en buyuk kalinti: 43.87
o evin metrekaresi: 130
o evin yasi: 26
```

Veri kümesindeki en yaşlı evlerden biri. Model yaşı bilmiyor — o sütunu
vermemiştik — ve tam olarak orada yanılıyor.

Bu tek bir kayıt. Peki bu bir **desen** mi, tesadüf mü?

## Kalıntı grafiği

Kalıntıları modelin görmediği bir sütuna karşı çizdiğimizde ortaya çıkan
şey şu:

```
kalinti ile yas arasindaki korelasyon: -0.937
```

Neredeyse mükemmel bir ilişki. Yaş büyüdükçe model **sistematik olarak
yüksek** tahmin ediyor.

<figure class="fig">
  <div class="versus">
    <div class="versus-side">
      <h4>Desensiz kalıntılar</h4>
      <p>Sıfırın etrafında rastgele dağılmış.<br>Model yakalayacağını yakalamış; kalan gürültü.</p>
    </div>
    <div class="versus-side">
      <h4>Desenli kalıntılar</h4>
      <p>Bir yöne doğru eğilim var.<br>Model bir şeyi <b>kaçırmış</b>; o şey hâlâ orada.</p>
    </div>
  </div>
  <figcaption>Kalıntı grafiği bir sınav değil, bir teşhis: modelin ne öğrenmediğini gösteriyor.</figcaption>
</figure>

**Kalıntıda desen görmek iyi haber.** Çünkü desen, hâlâ öğrenilebilecek bir
şeyin durduğu anlamına geliyor: burada `age` sütununu eklemek. Önceki
bölümde eklediğimizde hata 18.5'ten 7.13'e inmişti — kalıntı grafiği bunu
**eklemeden önce** söylüyordu.

**Bir ayrıntı:** doğrusal regresyonun kalıntılarının ortalaması eğitim
verisinde her zaman sıfıra çok yakın çıkıyor. Bu bir başarı işareti değil,
yöntemin bir sonucu. Ortalamaya değil **dağılıma** bakılıyor.

**Bir ayrıntı daha:** kalıntı incelemesi genelde **eğitim** verisinde
yapılıyor ve bu, "eğitimde ölçme" kuralıyla çelişmiyor. Orada ölçmüyorsun,
**teşhis koyuyorsun**. Ölçüm hâlâ testte.

## Ne raporlanır

Tek sayı bir rapor değil. Bir regresyon sonucu şunları taşıyor:

| Ne | Neden |
|---|---|
| MAE (ya da RMSE) | Ne kadar yanıldığın, anlaşılır birimde |
| R² | Karşılaştırılabilir bir oran |
| Taban çizginin aynı ölçüsü | "İyi" kelimesinin dayanağı |
| Hangi veride, kaç kayıtla | Sayının geçerli olduğu bağlam |
| Nerede yanıldığı | En büyük hatalar, kalıntı deseni |

Son satır en çok atlanan ve çoğu zaman en önemli olan. Bütün hataların tek
bir müşteri grubunda toplandığı bir model, ortalaması iyi olsa bile
kullanılamaz.

## Sınıflandırmada bunların hiçbiri işe yaramıyor

Bu bölümün tamamı **sayısal hedef** içindi. Hedef kategoriyse kalıntı
diye bir şey yok: "kedi" ile "köpek" arasındaki fark bir sayı değil.

Orada bambaşka ölçüler var — doğruluk, precision, recall — ve bir sonraki
bölümün konusu tam olarak bu.
