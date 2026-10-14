| Terim | Anlamı |
|---|---|
| **VAE** (varyasyonel otomatik kodlayıcı) | Kodu tek bir nokta yerine bir dağılım olarak öğrenen ve kod uzayını standart normale çeken otomatik kodlayıcı |
| **Ortalama** $\mu$ | Bir resmin kod dağılımının merkezi |
| **Log-varyans** $\log\sigma^2$ | Kod dağılımının yayılımının logaritması; $\sigma = e^{\frac{1}{2}\log\sigma^2}$ |
| **Yeniden parametrelendirme hilesi** | Örneği $z = \mu + \sigma\varepsilon$ ile çekmek; rastgelelik $\varepsilon$'ye taşınır, türev $\mu$ ve $\sigma$'ya geçer |
| **Önsel dağılım** (prior) | Kodların benzemesi istenen dağılım; burada standart normal |
| **KL ıraksaması** | İki dağılım arasındaki farkın ölçüsü; normal dağılımlar için $\frac{1}{2}\sum(\mu^2 + \sigma^2 - \log\sigma^2 - 1)$ |
| **İkili çapraz entropi** | 0–1 arasındaki pikseller için geri kurma kaybı; `sigmoid` çıkışla türevi `out - x` |
| **β** (KL ağırlığı) | Kayıpta KL teriminin çarpanı; geri kurma ile düzenli kod uzayı arasındaki denge |
| **Sonsal çöküş** (posterior collapse) | Kodların standart normale yapışıp resim hakkında bilgi taşımaması |
| **Ara değerleme** (interpolation) | İki kodun arasındaki doğru üzerinde ilerleyip her noktayı çözmek |

**Akılda tut:**

- VAE'de kod dağılımı bilinir: yeni örnek için standart normalden çekilir.
  Derste otomatik kodlayıcı oradan 10 rakamın 4'ünü, VAE hepsini üretti.
- `beta = 0` sıradan otomatik kodlayıcıdır; çok büyük β'da model çöker
  (β = 4'te KL 0, tek rakam).
- Ölçerken kodun merkezi ($\mu$) kullanılır; örnek yalnızca eğitimde ve
  üretimde çekilir.
