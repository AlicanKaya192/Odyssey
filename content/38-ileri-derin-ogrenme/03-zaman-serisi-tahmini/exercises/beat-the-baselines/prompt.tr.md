Başlangıç kodu 28 günlük pencerelerle küçük bir LSTM eğitiyor. Sonunda üç
hatayı asıl birimde hesapla:

- `mae_lstm`: modelin test tahminleri (`* std + mean` ile geri çevrilmiş)
  ile `actual` arasındaki ortalama mutlak hata,
- `mae_naive`: dünün değerinin hatası,
- `mae_week`: geçen haftanın aynı gününün hatası.

Son satır ikisiyle karşılaştırıyor.

**Beklenen çıktı:**

```
True True
```
