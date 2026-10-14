| Hata | Ne olur | Doğrusu |
|---|---|---|
| `side="right"` yazmamak | `u` tam bir sınıra düşerse (ör. 0,45) yanlış kategori seçilir | `np.searchsorted(cum, u, side="right")` |
| Olasılıkların toplamı 1 değil | Son kategori fazla ya da az seçilir; `rng.choice` hata verir | Önce `p = p / p.sum()` |
| `np.log(u)` yerine `np.log(1 - u)` ile karıştırmak | İkisi de çalışır ama `u` tam 0 çıkarsa `log(0)` sonsuz olur | `-np.log(1 - u)` (`u` 1 olamaz) |
| Dikdörtgen eğriden alçak | Tepedeki bölge kesilir, dağılım bozulur | Yükseklik en az eğrinin en büyük değeri |
| Aynı üreteçte çağrı sırasını değiştirmek | Sonuçlar başka sayılar çıkar | Sırayı sabit tut ve yaz |
| Tek çekilişe bakıp karar vermek | Şans yanıltır | Çok örneğin oranına bak |
| Az veride kuyruk oranına güvenmek | 17 balıkla %6, gerçek %7,9 | Örnek sayısını da raporla |
| Monte Carlo'yu kesin sanmak | Model yanlışsa sonuç da yanlış | Varsayımı veriyle karşılaştır |
