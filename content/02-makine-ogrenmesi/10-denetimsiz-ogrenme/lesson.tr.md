# Denetimsiz Öğrenme

Şimdiye kadar her bölümde bir `y` vardı: fiyat, geçti/kaldı, dolandırıcılık.
Model tahmin ediyordu, biz doğru cevapla karşılaştırıyorduk.

Bu bölümde **`y` yok.**

Elimizde 350 müşterinin dört sütunu var — `spend` (harcama), `visits`
(ziyaret), `items` (ürün), `returns` (iade) — ve kimsenin "bu müşteri şu
tip" diye etiketlediği bir liste yok. Soru şu: **bu insanlar kaç gruba
ayrılıyor ve grupları ne ayırıyor?**

## Neyin değiştiği

| | Denetimli | Denetimsiz |
|---|---|---|
| Girdi | `X` ve `y` | Yalnızca `X` |
| Çıktı | Tahmin | Yapı (grup, eksen) |
| Ölçü | Doğruluk, MAE, F1 | Silüet, açıklanan varyans |
| Doğru cevap | Var | **Yok** |
| Eğitim/test | Şart | Genelde anlamsız |

Son iki satır önemli. **Doğru cevap olmadığı için "model %92 doğru" diye
bir cümle kurulamıyor.** Elindeki ölçüler sonucun ne kadar *derli toplu*
olduğunu söylüyor, ne kadar *doğru* olduğunu değil.

Bu, denetimsiz öğrenmeyi kolay değil **daha zor** yapıyor: sonucun işe
yarayıp yaramadığına bakan tek merci sensin.

## K-ortalamalar

En yaygın kümeleme yöntemi. Fikri üç adım:

<figure class="fig">
  <div class="flow">
    <span class="node"><b>1</b><br>rastgele <code>k</code><br>merkez seç</span>
    <span class="arrow">&rarr;</span>
    <span class="node"><b>2</b><br>her kaydı<br>en yakına ata</span>
    <span class="arrow">&rarr;</span>
    <span class="node acc"><b>3</b><br>merkezleri<br>ortalamaya taşı</span>
  </div>
  <figcaption>Merkezler kıpırdamayana kadar dönüyor. Adı da buradan geliyor: k tane ortalama.</figcaption>
</figure>

```python
from sklearn.cluster import KMeans

model = KMeans(n_clusters=4, random_state=42, n_init=10)
labels = model.fit_predict(X_scaled)
```

`fit_predict` — çünkü tahmin edilecek ayrı bir test kümesi yok; model aynı
veriyi hem öğreniyor hem etiketliyor.

**`n_clusters` bir hiperparametre değil, bir girdi.** Modele "dört grup
bul" diyorsun ve o dört grup buluyor. Üç dersen üç bulur. Verinin kaç grup
içerdiğine dair bir fikri yok.

## İlk sonuç

Ölçekleyip `k=4` ile çalıştırınca kümelerin büyüklükleri **79, 102, 70, 99**
çıkıyor. Ortalamalara bakalım:

| Küme | `spend` | `visits` | `items` | `returns` |
|---|---|---|---|---|
| 0 | 428.2 | 15.2 | 23.4 | 3.3 |
| 1 | 45.8 | 3.2 | 4.2 | 0.3 |
| 2 | 63.9 | **19.3** | 6.4 | 2.6 |
| 3 | 180.2 | 8.4 | 11.3 | 1.1 |

**Bu tablo bölümün asıl çıktısı.** Küme numaraları hiçbir şey anlatmıyor;
anlatan şey ortalamalar:

- **Küme 1** — nadir gelen, az harcayan. 350 kişinin 102'si.
- **Küme 3** — orta düzey, düzenli. 99 kişi.
- **Küme 0** — çok harcayan, çok alan. 79 kişi.
- **Küme 2** — **ilginç olan.** Harcaması küme 1 kadar düşük (63.9) ama
  ayda 19 kez giriyor ve 2.6 iade yapıyor. Sık gelen, çok bakan, az alan,
  aldığını da geri veren biri.

Küme 2 bu veriden gözle bulunamazdı. Kümeleme tam da bunun için var:
**dört sütunun aynı anda söylediği şeyi görmek.**

## Ölçekleme burada da zorunlu

K-ortalamalar uzaklığa dayanıyor — tıpkı KNN gibi. Ölçeklemeden
çalıştırınca ne oluyor:

| | Silüet |
|---|---|
| Ölçekli | **0.517** |
| Ölçeksiz | **0.202** |

Ölçeksiz kümelerin büyüklükleri: **175, 47, 95, 33.**

Ne olduğu tabloya bakınca anlaşılıyor: `spend` sütununun yayılımı 155,
`returns` sütununun 1.5. Uzaklık hesabında `spend` her şeyi eziyor.

Sonuç: model **iki düşük harcamalı grubu tek bir 175 kişilik yığına
koyuyor** — sık gelen browser'lar kayboluyor — ve buna karşılık yüksek
harcamalıları **yalnızca harcamaya göre** ikiye bölüyor (481 ve 348).

Dört gerçek grup yerine, tek bir sütunun dört dilimini buluyor.

## `k`'yı seçmek

`k` girdi olduğuna göre onu nereden bilecek? İki araç var.

**Birincisi: eylemsizlik (inertia).** Her kaydın kendi merkezine olan
uzaklığının karesi toplamı. `k` arttıkça mutlaka düşüyor — `k` kayıt
sayısına eşit olsaydı sıfır olurdu. Bakılan şey **nerede yavaşladığı**:

```
k=2   695.9
k=3   388.8      <- buyuk dusus
k=4   265.6      <- buyuk dusus
k=5   212.7      <- yavasliyor
k=6   189.6
k=7   167.3
```

Buna **dirsek yöntemi** deniyor: eğrinin büküldüğü nokta. Burada dirsek
3 ile 4 arasında.

**İkincisi: silüet.** Her kayıt için "kendi kümesine ne kadar yakın, en
yakın diğer kümeye ne kadar uzak" oranı. −1 ile +1 arasında; yüksek iyi.

```
k=2   0.514
k=3   0.525      <- en yuksek
k=4   0.517
k=5   0.489
```

**İşte dürüst kısım: silüet `k=3` diyor, veri gerçekte dört gruptan
üretildi.** Aradaki fark 0.008 — ölçüm gürültüsü kadar.

Silüet yanılmıyor; kendi sorusuna doğru cevap veriyor. Onun sorusu
"kümeler ne kadar derli toplu", "kaç gerçek grup var" değil. Küme 1 ile
küme 2 (az harcayanlar ile sık gelen browser'lar) uzayda birbirine yakın
duruyor; üçe indirince silüet biraz artıyor ama **iş açısından anlamlı bir
ayrım kayboluyor.**

**Sonuç:** `k` bir ölçüm sonucu değil, bir karar. İki araç aralığı
daraltıyor (2 ile 5 arası değil, 3 ile 4 arası), gerisini tablodaki
ortalamalara bakan insan seçiyor.

## K-ortalamalar her zaman küme buluyor

Bu bölümün en önemli uyarısı. Tamamen rastgele üretilmiş, hiçbir yapısı
olmayan 350 satırlık bir veriye `KMeans` uygulayınca:

```
k=2   silhouette 0.169
k=3   silhouette 0.176
k=4   silhouette 0.181
k=5   silhouette 0.185
```

**Model dört küme döndürüyor, silüet pozitif ve `k` arttıkça artıyor.**
Ortada hiçbir grup yok.

İki ders var burada:

1. **Küme döndürmesi, küme olduğunun kanıtı değil.** Algoritma ne
   verirsen bölüyor.
2. **Silüeti maksimize etmek bir yöntem değil.** Gürültüde bile artıyor.
   Karşılaştırma yaparken bir referansa ihtiyacın var — gerçek veride
   0.52, gürültüde 0.18: aradaki üç kat fark asıl bilgi.

Kümelerin gerçek olup olmadığının testi sayıda değil: **ortalama tablosu
anlamlı bir hikâye anlatıyor mu?** Küme 2 için anlatıyordu.

## Küme numaraları keyfi

Aynı veriyi farklı `random_state` ile çalıştırınca:

```
seed 0   [45.8, 428.2, 63.9, 180.2]
seed 1   [180.2, 428.2, 63.9, 45.8]
seed 2   [63.9, 45.8, 180.2, 428.2]
```

**Gruplar aynı, numaraları farklı.** "Küme 0" diye bir şey yok; bir sonraki
çalıştırmada başka bir gruba düşüyor.

Bu yüzden iki kümelemeyi karşılaştırırken etiketler doğrudan
karşılaştırılmıyor. Doğru araç:

```python
from sklearn.metrics import adjusted_rand_score
print(adjusted_rand_score(labels_a, labels_b))
```

**Düzeltilmiş Rand skoru** numaralara değil, "aynı iki kayıt aynı kümede
mi" sorusuna bakıyor. 1.0 aynı gruplama, 0 rastgele kadar benzer.

Ölçekli ile ölçeksiz kümelemenin ARI'si **0.602** — yani gerçekten farklı
iki gruplama, yalnızca numaralar kaymış değil.

## Temel bileşenler analizi (PCA)

İkinci denetimsiz yöntem, kümeleme değil **boyut indirgeme**: dört sütunu
iki sütuna indirmek, mümkün olduğunca az bilgi kaybederek.

```python
from sklearn.decomposition import PCA

pca = PCA(n_components=2)
Z = pca.fit_transform(X_scaled)
print(pca.explained_variance_ratio_)   # [0.662 0.223]
```

**Birinci bileşen verinin varyansının %66,2'sini, ikincisi %22,3'ünü
taşıyor.** İkisi birlikte **%88,5**. Dört sütunu ikiye indirdik ve
bilginin %11,5'ini kaybettik.

Bileşenler ne? Ağırlıklarına bakılıyor:

```
bilesen 1   [ 0.531,  0.426,  0.540,  0.495]
bilesen 2   [-0.471,  0.659, -0.425,  0.403]
              spend  visits   items  returns
```

**Birinci bileşende dördü de pozitif ve birbirine yakın:** bu eksen "genel
hareketlilik". Sağa gittikçe her şeyi çok yapan müşteri.

**İkinci bileşende `visits` ve `returns` artı, `spend` ve `items` eksi:**
bu eksen tam olarak "çok geliyor ama az alıyor". Yani küme 2'yi ayıran
şey ikinci bileşende yazıyor.

PCA hiçbir etiket görmeden bu ekseni buldu.

**PCA'nın bedeli yorumlanabilirlik.** Yeni sütunların adı `PC1` ve `PC2`;
bunlar dört orijinal sütunun karışımı. "Harcama arttıkça şu oluyor" gibi
bir cümle artık kurulamıyor.

## PCA + kümeleme

İki bileşenin üstünde tekrar `KMeans` çalıştırınca:

```
tam uzayda silüet    0.517
PCA uzayinda silüet  0.652
ARI (ikisi arasinda) 1.000
```

**ARI 1.000: gruplama birebir aynı.** Dört sütunun ikisi atıldı ve hiçbir
müşteri yer değiştirmedi.

**Ama silüetin yükselmesine aldanma.** 0.652, kümelerin daha iyi olduğunu
değil, **daha az boyutta ölçüldüğünü** gösteriyor. Atılan iki boyut
kümeleri birbirine karıştıran gürültüydü; onları atınca aynı gruplar daha
derli toplu *görünüyor*. Farklı boyuttaki iki uzayın silüetleri
karşılaştırılmaz.

PCA'nın buradaki gerçek faydası **çizim**: dört boyutlu veriyi kâğıda
dökemezsin, ikisini dökebilirsin.

## Ne zaman ne

| İhtiyaç | Yöntem |
|---|---|
| Müşterileri gruplara ayırmak | K-ortalamalar |
| Dört boyutlu veriyi çizmek | PCA |
| Çok sayıda ilişkili sütunu azaltmak | PCA |
| Aykırı davranış bulmak | Kümeleme değil, anomali tespiti |
| Grupları önceden biliyorsan | Kümeleme değil, sınıflandırma |

Son satır sık atlanıyor: **etiketin varsa kümeleme yapma.** Denetimli
öğrenme her zaman daha güçlü; denetimsiz yöntemler etiket *olmadığında*
başvurulan yollar.

## Bu bölümde neyi atladık

- **K-ortalamaların varsayımları.** Yuvarlak, benzer boyutlu ve benzer
  yoğunluklu kümeler arıyor. Hilal biçimli iki grup verirsen ikisini
  ortadan keser.
- **DBSCAN.** Yoğunluğa bakıyor; `k` istemiyor, kümeleri kendi buluyor ve
  hiçbir kümeye ait olmayan kayıtları **gürültü** diye işaretleyebiliyor.
  Yuvarlak olmayan biçimlerde çok daha iyi.
- **Hiyerarşik kümeleme.** Kayıtları tek tek birleştirip bir ağaç
  (dendrogram) üretiyor; `k`'yı sonradan, ağaca bakarak seçiyorsun.
- **t-SNE ve UMAP.** Görselleştirme için PCA'dan çok daha güçlü, ama
  uzaklıkları korumadıkları için üstlerinde kümeleme yapılmıyor — yalnızca
  bakmak için.

Bu bölümün özeti: **denetimsiz öğrenmede algoritma her zaman bir cevap
veriyor; cevabın anlamlı olup olmadığına karar veren sensin.**
