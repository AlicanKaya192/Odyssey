## Gradyan inişi türleri

| Tür | Her adımda | Artısı | Eksisi |
|---|---|---|---|
| Toplu (batch) | bütün veri | kararlı, düzgün iniş | büyük veride yavaş |
| Mini-batch | küçük grup (32–512) | hızlı, GPU'ya uygun | gürültülü |
| Stokastik (SGD) | tek örnek | çok hızlı adım | çok gürültülü |
| Momentum | birikmiş gradyan | dar vadide hızlı | bir ayar daha (`β`) |
| Adam | ağırlık başına uyarlanan adım | ölçeğe dayanıklı | daha çok ayar (`β₁`, `β₂`) |

## Ayarlar

- **Öğrenme oranı:** önce kaba bir tarama (0,001, 0,01, 0,1, 1); kayıp
  ıraksıyorsa küçült, çok yavaşsa büyüt.
- **Durdurma:** belli bir adım sayısı ya da kayıp artık neredeyse düşmüyorsa
  (`|L_önce − L_sonra| < tolerans`).
- **Öğrenme oranı takvimi:** başta büyük, sonra küçük adımlar; SGD'nin dipte
  dolaşmasını azaltır.

## Sık hatalar

- Ölçeklemeyi unutmak: tek bir öğrenme oranı bütün ağırlıklara uymaz.
- Gradyanda `1/n`'i unutmak: veri büyüdükçe adımlar da büyür, ıraksar.
- Her epoch'ta veriyi karıştırmamak: mini-batch'ler hep aynı sırayla gelir.
- Yazılan gradyanı sayısal gradyanla denetlememek.
