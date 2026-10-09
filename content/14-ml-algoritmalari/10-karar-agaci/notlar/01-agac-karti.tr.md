## Bölme ölçüleri

| Ölçü | Formül | Kullanım |
|---|---|---|
| Gini | `1 − Σ pₖ²` | sınıflandırma (scikit-learn varsayılanı) |
| Entropi | `−Σ pₖ log₂ pₖ` | sınıflandırma (`criterion="entropy"`) |
| Hata kareleri | `Σ (y − ȳ)²` | regresyon |

## Ayarlar (scikit-learn adlarıyla)

| Ayar | Etkisi |
|---|---|
| `max_depth` | en çok kaç soru; küçük → basit ağaç |
| `min_samples_split` | bir düğümün bölünmesi için en az örnek |
| `min_samples_leaf` | yaprakta en az örnek; gürültüye yaprak açmayı engeller |
| `ccp_alpha` | maliyet-karmaşıklık budaması: büyük → daha çok budama |

## Artıları ve eksileri

- Okunabilir, ölçekleme istemez, eksik dönüşüm gerektirmez, doğrusal olmayan
  sınırları ve etkileşimleri kendiliğinden öğrenir.
- Kararsızdır: veride küçük bir değişiklik bambaşka bir ağaç kurdurabilir;
  sınırları eksenlere paraleldir; derin ağaç kolayca aşırı uyar.

## Sık hatalar

- Derinliği sınırlamamak: eğitimde %100, testte düşük.
- Ağacın seçtiği ilk özelliği "en önemli neden" sanmak: açgözlü seçim,
  benzer özelliklerden yalnızca birini kullanabilir.
- Regresyon ağacından düzgün bir eğri beklemek: tahmin basamaklıdır.
