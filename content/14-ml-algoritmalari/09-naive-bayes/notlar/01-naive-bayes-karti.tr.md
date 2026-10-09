## Türler

| Tür | Özellik | Sınıf içi dağılım | scikit-learn |
|---|---|---|---|
| Gauss | sürekli sayılar | normal (ortalama, varyans) | `GaussianNB` |
| Çok terimli | sayılar (kelime sayıları) | kelime payları | `MultinomialNB` |
| Bernoulli | 0/1 (kelime var mı) | var olma olasılığı | `BernoulliNB` |

## Formül

`sınıf = argmax ( log P(c) + Σ log P(xᵢ | c) )`

- Öncül `P(c)`: eğitimde sınıfın payı.
- Gauss: `log N(x | ort, var) = −½ log(2π var) − (x − ort)² / (2 var)`.
- Çok terimli: `log P(kelime | c) = log((sayı + α) / (toplam + α · V))`,
  `V` sözlük boyu.

## Artıları ve eksileri

- Çok hızlı (tek geçiş), az veriyle çalışır, çok sayıda özelliği (binlerce
  kelime) kaldırır, yeni veriyle kolayca güncellenir.
- Bağımsızlık varsayımı yüzünden olasılıkları aşırı emin olabilir; özellikler
  arası etkileşimi öğrenemez.

## Sık hatalar

- Olasılıkları çarpmak: alt taşma. Logaritmaları topla.
- Düzeltmeyi (`alpha`) kapatmak: görülmemiş tek kelime kararı siler.
- Gauss NB'de sıfır varyanslı özellik: bölme hatası; scikit-learn bu yüzden
  küçük bir pay ekler.
