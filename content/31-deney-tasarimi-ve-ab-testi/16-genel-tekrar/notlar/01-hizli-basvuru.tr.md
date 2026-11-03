## Hangi adımda ne kullanırım?

| Adım | Araç |
|---|---|
| Kaç kişi gerekir? | `proportion_effectsize` + `NormalIndPower().solve_power` |
| Atama | tuzlu karma: `hashlib.md5(f"{salt}:{user_id}".encode())` → kova |
| SRM | `stats.chisquare(n)`; p < 0,001 ise dur |
| İki oran | `proportions_ztest`, `confint_proportions_2indep` |
| Formülsüz istatistik | bootstrap: `rng.choice(x, len(x))`, yüzdelik aralık |
| Varsayımsız test | permütasyon: `rng.permutation(labels)` |
| Her gün bakmak | Bonferroni α / bakış ya da benzetimle ayarlanmış eşik |
| Çok metrik | `multipletests(p, method="holm")` ya da `"fdr_bh"` |
| Gürültülü metrik | CUPED: Y − θ(X − X̄), θ = cov(X, Y) / var(X) |
| Oran metriği | delta yöntemi (kullanıcı düzeyinde varyans ve kovaryans) |
| Değişen atama oranı | tabakalı tahmin |
| Paylaşılan kaynak | küme halinde atama, analiz küme düzeyinde |
| Hızlı seçim | Thompson örneklemesi: `rng.beta(1 + k, 1 + n - k)` |
| Belirsiz sonuç | P(B > A) ve beklenen kayıp |

## Sayılar

- 20 bağımsız testte en az bir yanlış alarm: yaklaşık %64.
- CUPED'den sonra kalan varyans: 1 − ρ².
- Kümede tasarım etkisi: 1 + (m − 1) · ICC.
- SRM eşiği: 0,001.

## Dört karar

| Aralık | Karar |
|---|---|
| tamamen eşiğin üstünde | uygula |
| tamamen sıfırın altında | zararlı |
| sıfırı ve eşiği içeriyor | belirsiz |
| sıfırın üstünde, eşiğin altında | değmez |

## Kırmızı bayraklar

- Planı testten sonra yazmak; eşiği, metriği ya da süreyi sonuca göre
  değiştirmek.
- SRM varken sonuç okumak.
- Her gün bakıp anlamlı olunca durmak.
- En çarpıcı segmenti ya da metriği öne çıkarmak.
- İlk haftanın etkisini kalıcı sanmak.
- Gösterimleri bağımsız saymak.
