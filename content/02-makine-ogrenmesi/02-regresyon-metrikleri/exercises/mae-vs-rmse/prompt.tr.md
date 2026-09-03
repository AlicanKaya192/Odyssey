İki model var ve gerçek değerin hepsi 100.

- **Model A** her tahmininde 10 birim yanılıyor.
- **Model B** dokuzunu tam biliyor, birinde 100 birim yanılıyor.

Hangisi daha iyi? Önce ölçelim.

**Yapman gerekenler:**

1. `sklearn.metrics` içinden gereken iki fonksiyonu içe aktar.
2. İki model için de **MAE** ve **RMSE** hesapla. (sklearn RMSE'yi doğrudan
   vermiyor; MSE'nin karekökünü sen alıyorsun.)
3. Her model için tek satır yazdır: **model adı, MAE, RMSE** — üçü yan yana,
   sayılar iki ondalık.

**Beklenen çıktı:**

```
a 10.0 10.0
b 10.0 31.62
```

**MAE ikisini ayırt edemiyor.** İkisi de 10.0. MAE'ye göre bu iki model
birebir aynı.

**RMSE ayırt ediyor.** B'nin tek büyük hatası, kare alınınca üç katı ceza
getiriyor.

**Hangisi haklı?** Ölçü değil, problem karar veriyor:

- Teslimat süresi tahmininde on dakikalık sapma tolere edilir ama tek bir
  siparişte 100 dakika yanılmak müşteriyi kaybettirir. **B kötü model,
  RMSE haklı.**
- Aylık toplam maliyet tahmininde küçük sapmalar birikir, tek bir büyük
  sapma ortalamada erir. **A kötü model, MAE haklı.**

Ölçü seçmek teknik değil, **iş kararı**. "Büyük bir hata küçük hataların
toplamından daha mı pahalı" sorusunun cevabı ne ise, ölçü o.
