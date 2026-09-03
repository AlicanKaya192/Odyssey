Dört sütunlu veriyi kâğıda dökemezsin. **Temel bileşenler analizi**
(PCA) tam da bunun için var: dört sütunu ikiye indirmek, mümkün olduğunca
az bilgi kaybederek.

**Yapman gerekenler:**

1. Veriyi hazırla ve ölçekle. (PCA varyansa baktığı için ölçekleme burada
   da zorunlu.)
2. **Bütün** bileşenleri hesapla ve kümülatif açıklanan varyansı üç
   ondalıkla liste olarak yazdır.
3. İki bileşenle yeniden kur, dönüştür. İki bileşenin ağırlıklarını ayrı
   satırlarda yazdır (üç ondalık, sütun sırası `spend`, `visits`, `items`,
   `returns`).
4. Tam uzayda ve PCA uzayında **ayrı ayrı** `KMeans(n_clusters=4,
   random_state=42, n_init=10)` çalıştır. İki silüeti yan yana yazdır
   (üç ondalık).
5. İki kümelemenin `adjusted_rand_score` değerini yazdır.
6. PCA uzayındaki noktaları serpme grafiği olarak çiz, **tam uzaydaki küme
   etiketiyle renklendir**. Eksenleri `pc1` ve `pc2` diye adlandır, başlık
   koy, `chart.png` olarak kaydet.

**Beklenen çıktı:**

```
[0.662, 0.885, 0.973, 1.0]
[0.531, 0.426, 0.54, 0.495]
[-0.471, 0.659, -0.425, 0.403]
0.517 0.652
1.0
```

**Birinci satır: iki bileşen varyansın %88,5'ini taşıyor.** Dört sütunu
ikiye indirdik ve bilginin %11,5'ini kaybettik.

**İkinci satır — birinci bileşen:** dördü de pozitif ve birbirine yakın
(0.531, 0.426, 0.540, 0.495). Bu eksen "genel hareketlilik": sağa gittikçe
her şeyi çok yapan müşteri.

**Üçüncü satır — ikinci bileşen:** `visits` (0.659) ve `returns` (0.403)
artı, `spend` (−0.471) ve `items` (−0.425) eksi. Bu eksen tam olarak
**"çok geliyor ama az alıyor"**. Birinci alıştırmadaki küme 2'yi ayıran
şey burada yazıyor.

**PCA bu ekseni hiçbir etiket görmeden buldu.** Ona kimse "browser'ları
ayır" demedi; yalnızca varyansı en çok taşıyan yönleri aradı ve ikincisi
bu çıktı.

**Dördüncü satır: 0.517 ve 0.652.** PCA sonrası silüet yükseliyor —
**ama buna aldanma.** Yüksek silüet kümelerin daha iyi olduğunu değil,
**daha az boyutta ölçüldüğünü** gösteriyor. Atılan iki boyut kümeleri
birbirine karıştıran gürültüydü; onları atınca aynı gruplar daha derli
toplu *görünüyor*. Farklı boyuttaki iki uzayın silüetleri
karşılaştırılmaz.

**Beşinci satır bunu kanıtlıyor: ARI 1.0.** Gruplama birebir aynı. İki
sütun atıldı ve **hiçbir müşteri yer değiştirmedi.**

Grafikte dört kümenin ayrıldığını göreceksin. PCA'nın buradaki gerçek
faydası bu: dört boyutlu veriyi kâğıda dökemezsin, ikisini dökebilirsin.

**Bedeli yorumlanabilirlik.** Yeni sütunların adı `pc1` ve `pc2`; bunlar
dört orijinal sütunun karışımı. "Harcama arttıkça şu oluyor" gibi bir
cümle artık kurulamıyor.
