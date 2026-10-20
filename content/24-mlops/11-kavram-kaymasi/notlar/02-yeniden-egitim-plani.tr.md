Yeniden eğitim bir hattır; tek bir `fit` çağrısı değildir.

<figure class="fig">
  <div class="flow">
    <span class="node">Tetik</span>
    <span class="arrow">→</span>
    <span class="node">Veri penceresi</span>
    <span class="arrow">→</span>
    <span class="node">Eğit</span>
    <span class="arrow">→</span>
    <span class="node acc">Güncel kapı</span>
    <span class="arrow">→</span>
    <span class="node">Kayıt</span>
  </div>
  <figcaption>Kapı güncel ve etiketli bir kümeyle çalışır.</figcaption>
</figure>

## Dersteki seçenekler (6. ve 7. ay)

| Seçenek | 6. ay | 7. ay |
|---|---|---|
| Hiç eğitme | 0,685 | 0,658 |
| Bütün geçmiş (0–5) | 0,759 | 0,742 |
| Son pencere (4–5) | 0,821 | 0,798 |

## Kapı tuzağı

| Model | 0. ay kümesi | 5. ay kümesi |
|---|---|---|
| İlk model | 0,813 | 0,681 |
| Son pencere | 0,718 | 0,837 |

Eski kümeyle kurulan kapı yeni modeli geri çevirirdi.

## Kontrol listesi

- Tetik belli mi (takvim, kalite uyarısı ya da ikisi)?
- Pencere boyu gelecekteki bir dönemde ölçülerek mi seçildi?
- Eğitim verisi tarih itibarıyla mı çekildi ve doğrulandı mı?
- Kapının değerlendirme kümesi güncel ve etiketli mi?
- Yeni model kayda sürümüyle, verisiyle ve ölçümleriyle girdi mi?

## Yapma

- Kavram kaydığında "veri ne kadar çoksa o kadar iyi" deme.
- Kapıyı eğitim zamanından kalma bir kümeyle çalıştırma.
- Her kayma uyarısında kendiliğinden yeniden eğitme; önce verinin hatalı
  olmadığını doğrula.
