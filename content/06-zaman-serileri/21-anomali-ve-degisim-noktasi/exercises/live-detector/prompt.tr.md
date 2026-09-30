Web trafiği için yalnızca geçmişi kullanan bir dedektör kur ve beklentinin
ortancayla mı ortalamayla mı kurulduğunun neyi değiştirdiğini gör.

Başlangıç kodunda `past` hazır: her gün için aynı günün son dört haftadaki
değerleri (dört sütun).

**Yapman gerekenler:**

1. `alarms(expected)` fonksiyonunu yaz: oransal sapmayı hesaplasın
   (`v / expected - 1`) ve mutlak değeri 0.25'i geçen günleri `"%m-%d"`
   listesi olarak döndürsün.
2. Beklenti `past.median(axis=1)` iken alarm sayısını ve listeyi alt alta
   yazdır.
3. Beklenti `past.mean(axis=1)` iken alarm sayısını yazdır.
4. Ortalamayla alarm veren ama ortancayla **vermeyen** günleri liste olarak
   yazdır.
5. 21 Mart için ortalama beklentiyi, ortanca beklentiyi ve gerçek değeri tam
   sayı olarak aynı satıra yazdır.

**Beklenen çıktı:**

```
12
['03-14', '06-20', '09-02', '09-03', '09-05', '09-08', '09-09', '09-10', '09-11', '09-12', '09-14', '10-08']
16
['04-04', '04-11', '07-04', '07-11', '10-15', '11-05']
5366 4015 4075
```

Ortancayla 12 alarm: iki kampanya, kesinti ve Eylül'deki düzey kayması.
Ortalamayla fazladan gelen altı alarmın hepsi bir anomaliden **sonraki**
haftalarda, aynı haftanın gününde: tamamen olağan günler, bozulmuş bir
beklentiyle karşılaştırılmış. 21 Mart'ta ortalama, bir hafta önceki
kampanyayı içine aldığı için 5366 bekliyor.
