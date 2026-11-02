İki yaklaşım rakip değil, farklı soruların cevabı. Aynı veriye ikisiyle de
bakmak çoğu zaman en sağlıklısı.

| | Frekansçı | Bayesçi |
|---|---|---|
| Olasılık neyi anlatır? | çok tekrarda görülen sıklığı | bir şeye ne kadar inandığımızı |
| Parametre | sabit ama bilinmeyen bir sayı | dağılımı olan bir bilinmeyen |
| Ana çıktı | p değeri, güven aralığı | sonsal, inandırıcı aralık, P(B > A) |
| Geçmiş bilgi | tasarımda (güç hesabı) | doğrudan önselde |
| Denetlediği | yanlış alarm oranı (α) | kararın beklenen kaybı |
| Zayıf yanı | sonucu ekibe anlatmak zor | önsel tartışılabilir |

## Sık karışan cümleler

- "%95 güven aralığı: gerçek değer %95 olasılıkla burada." → Bu cümle
  **inandırıcı aralık** için doğru, güven aralığı için değil.
- "p = 0,03, yani B'nin daha iyi olma olasılığı %97." → Yanlış. Bu bir
  P(B > A) cümlesi; p bunu söylemez.
- "Bayesçi yöntemde istediğim an bakıp durdurabilirim." → Bakmak serbest,
  ama durdurma kuralı önceden yazılmazsa kararların yanlış olma sıklığı
  yine artar.

## Ne zaman Bayesçi bakış işe yarar?

- Karar vericiye "B'nin daha iyi olma olasılığı" ve "yanılırsak kaybımız"
  gibi doğrudan sayılar gerekiyorsa.
- Güvenilir geçmiş veri varsa ve örneklem küçükse.
- Birçok küçük grubu (ör. yüzlerce ürün) birlikte tahmin ederken, büzülme
  aşırı uçlara inanmayı önler.
