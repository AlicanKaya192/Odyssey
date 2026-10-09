## Formüller

| Ne | Formül |
|---|---|
| Geçiş matrisi | `M[i, j] = 1 / çıkış(j)`, `j → i` bağlantısı varsa |
| Bir adım | `r ← d · M r + (1 − d) / n` |
| Tam çözüm | `(I − d M) r = (1 − d) / n · 1` |
| Durma | `Σ abs(r_yeni − r) < tol` |
| Hata sınırı | her adımda en az `d` katına iner (L1 normunda) |

## Özel durumlar

| Durum | Sorun | Çare |
|---|---|---|
| Çıkmaz sayfa (dangling) | olasılık sızar, toplam < 1 | o sütunu `1 / n` yap |
| Kapalı döngü (spider trap) | olasılığı toplar | sönümleme (`d < 1`) |
| Bağlantısız parçalar | tek bir çözüm olmayabilir | rastgele atlama (`1 − d`) birleştirir |

## Nerede kullanılır?

- Arama motorları: sayfa sıralamasında sinyallerden biri.
- Sosyal ağ: etkili hesap; atıf ağı: önemli makale.
- Öneri: kişiselleştirilmiş PageRank ile "bu düğüme yakın ve önemli" olanlar.
- Kelime ve cümle grafları: TextRank ile anahtar kelime ve özet çıkarma.

## Sık hatalar

- Matrisi ters kurmak: `M[i, j]` `j`'den `i`'ye; sütunların toplamı 1 olmalı.
- Çıkmaz sayfaları unutmak: sıralar yanlış değil ama toplam 1 değil ve
  karşılaştırmalar bozulur.
- Bağlantı sayısını (giriş derecesi) PageRank sanmak.
- Büyük ağda tam çözüm denemek: matris `n × n`, yoğun hâli belleğe sığmaz;
  seyrek matris ve kuvvet yinelemesi kullanılır.
