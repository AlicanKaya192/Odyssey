## Ölçüler

| Ölçü | Formül | Okuma |
|---|---|---|
| Destek | `destek(A ∪ B)` | kural ne kadar sık geçerli |
| Güven | `destek(A ∪ B) / destek(A)` | `A` varken `B` oranı |
| Kaldıraç | `güven / destek(B)` | `> 1` artırıyor, `≈ 1` ilgisiz, `< 1` azaltıyor |

Kaldıraç simetriktir: `A → B` ile `B → A`'nın kaldıracı aynı (derste bira ↔
cips ikisi de 2,86); güven simetrik değildir (0,527 ve 0,607).

## Apriori

- **Aşağı kapanma** (downward closure): sık kümenin her alt kümesi sık.
- Katman katman: `k` elemanlı sıklardan `k + 1` elemanlı adaylar, alt
  kümesi seyrek olan aday sayılmadan atılır.
- Her katmanda veri bir kez taranır; büyük veride **FP-Growth** gibi
  yöntemler veriyi sıkıştırılmış bir ağaçta tutarak taramayı azaltır.

## Pratikte

- Python'da `mlxtend` paketi (`apriori`, `association_rules`) yaygın;
  sepetleri bir doğru/yanlış tablosuna (her sütun bir ürün) çevirmek gerekir.
- Önce destek eşiğiyle kümeleri, sonra güven ya da kaldıraç eşiğiyle
  kuralları süz.

## Sık hatalar

- Kuralları yalnızca güvene göre sıralamak: popüler ürünler her yerde.
- Birlikteliği nedensellik sanmak: "bira cipsi artırıyor" değil, "birlikte
  görülüyorlar".
- Eşiği çok düşük seçip binlerce kural üretmek.
- Kaldıracı 1'in altındaki kuralları görmezden gelmek: onlar da bilgi
  (birbirinin yerine geçen ürünler).
