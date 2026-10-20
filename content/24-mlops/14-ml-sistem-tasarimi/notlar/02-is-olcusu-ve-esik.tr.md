Model aynı kalırken eşik değişince karar, karar değişince kâr değişir.

## Dersteki ölçüm (1000 müşteri, 297'si iptal)

| Eşik | Teklif | Kâr | Doğruluk |
|---|---|---|---|
| 0,2 | 474 | 2166 | 0,733 |
| 0,31 | 352 | 2254 | 0,797 |
| 0,4 | 272 | 2150 | 0,821 |
| 0,5 | 204 | 1806 | 0,813 |

- Kârı en büyük eşik 0,31; doğruluğu en büyük eşik 0,4.
- Herkese teklif: 1000 teklif, 346 birim.

## Yedek plan karşılaştırması

| Ne çalışıyor | Teklif | Kâr |
|---|---|---|
| Model (eşik 0,31) | 352 | 2254 |
| Kural (`support_calls >= 2`) | 172 | 1066 |
| Hiçbir şey | 0 | 0 |

## Hesap

- Teklif edilen her müşteri için: iptal edecekse `18 - 5 = 13`, kalacaksa
  `-5`.
- Kâr = bu değerlerin toplamı.

## Yapma

- Eşiği varsayılan 0,5'te bırakma; ölçüye göre seç.
- Eşiği seçtiğin kümede kârı raporlayıp bitirme; başka bir dönemde
  doğrula.
