# Tekil Değer Ayrışımı (SVD)

Önceki bölümde özdeğerler bir matrisin "iskeletini" gösterdi: doğru
tabanda matris yalnızca bir ölçekleme. Ama o fikrin iki eksiği vardı:
yalnızca **kare** matrislerde çalışıyordu ve her kare matriste bile işe
yaramıyordu (döndürmenin gerçel özvektörü yoktu).

**Tekil değer ayrışımı** (Singular Value Decomposition, SVD) bu iki
eksiği de kapatıyor: **her** matrisi, hangi boyutta olursa olsun, üç
basit parçaya ayırıyor. Doğrusal cebirin belki de en kullanışlı sonucu
bu. Görüntü sıkıştırma, öneri sistemleri, PCA, gürültü temizleme ve
metinlerden anlam çıkarma, hepsi SVD'nin uygulamaları.

Ön bilgi: Özdeğerler ve Özvektörler bölümü.

## Ana fikir: döndür, esnet, döndür

Her $m \times n$ matris $A$ şöyle yazılabilir:

$$
A = U \Sigma V^\mathsf{T}
$$

| Parça | Boyut | Ne yapıyor? |
|---|---|---|
| $V^\mathsf{T}$ | $n \times n$ | Döndürür (ya da yansıtır); uzunlukları değiştirmez |
| $\Sigma$ | $m \times n$ | Eksenler boyunca esnetir; köşegeninde $\sigma_1 \ge \sigma_2 \ge \cdots \ge 0$ |
| $U$ | $m \times m$ | Döndürür (ya da yansıtır); uzunlukları değiştirmez |

$U$ ve $V$'nin sütunları birbirine dik birim vektörler (bu tür matrislere
**dik matris** denir; $U^\mathsf{T}U = I$, tersleri devrikleri). $\Sigma$'nın
köşegenindeki sayılar **tekil değerler**: hep sıfır ya da pozitif,
büyükten küçüğe dizilmiş.

<figure class="fig">
<svg viewBox="0 0 440 144" width="440"><line class="grid" x1="8" y1="116" x2="8" y2="14"/><line class="grid" x1="25" y1="116" x2="25" y2="14"/><line class="grid" x1="42" y1="116" x2="42" y2="14"/><line class="line" x1="59" y1="116" x2="59" y2="14"/><line class="grid" x1="76" y1="116" x2="76" y2="14"/><line class="grid" x1="93" y1="116" x2="93" y2="14"/><line class="grid" x1="110" y1="116" x2="110" y2="14"/><line class="grid" x1="8" y1="116" x2="110" y2="116"/><line class="grid" x1="8" y1="99" x2="110" y2="99"/><line class="grid" x1="8" y1="82" x2="110" y2="82"/><line class="line" x1="8" y1="65" x2="110" y2="65"/><line class="grid" x1="8" y1="48" x2="110" y2="48"/><line class="grid" x1="8" y1="31" x2="110" y2="31"/><line class="grid" x1="8" y1="14" x2="110" y2="14"/><polygon class="dot" opacity="0.14" points="76.0,65.0 75.9,63.5 75.7,62.0 75.4,60.6 75.0,59.2 74.4,57.8 73.7,56.5 72.9,55.2 72.0,54.1 71.0,53.0 69.9,52.0 68.8,51.1 67.5,50.3 66.2,49.6 64.8,49.0 63.4,48.6 62.0,48.3 60.5,48.1 59.0,48.0 57.5,48.1 56.0,48.3 54.6,48.6 53.2,49.0 51.8,49.6 50.5,50.3 49.2,51.1 48.1,52.0 47.0,53.0 46.0,54.1 45.1,55.2 44.3,56.5 43.6,57.8 43.0,59.2 42.6,60.6 42.3,62.0 42.1,63.5 42.0,65.0 42.1,66.5 42.3,68.0 42.6,69.4 43.0,70.8 43.6,72.2 44.3,73.5 45.1,74.8 46.0,75.9 47.0,77.0 48.1,78.0 49.2,78.9 50.5,79.7 51.8,80.4 53.2,81.0 54.6,81.4 56.0,81.7 57.5,81.9 59.0,82.0 60.5,81.9 62.0,81.7 63.4,81.4 64.8,81.0 66.2,80.4 67.5,79.7 68.8,78.9 69.9,78.0 71.0,77.0 72.0,75.9 72.9,74.8 73.7,73.5 74.4,72.2 75.0,70.8 75.4,69.4 75.7,68.0 75.9,66.5"/><polygon class="curve3" points="76.0,65.0 75.9,63.5 75.7,62.0 75.4,60.6 75.0,59.2 74.4,57.8 73.7,56.5 72.9,55.2 72.0,54.1 71.0,53.0 69.9,52.0 68.8,51.1 67.5,50.3 66.2,49.6 64.8,49.0 63.4,48.6 62.0,48.3 60.5,48.1 59.0,48.0 57.5,48.1 56.0,48.3 54.6,48.6 53.2,49.0 51.8,49.6 50.5,50.3 49.2,51.1 48.1,52.0 47.0,53.0 46.0,54.1 45.1,55.2 44.3,56.5 43.6,57.8 43.0,59.2 42.6,60.6 42.3,62.0 42.1,63.5 42.0,65.0 42.1,66.5 42.3,68.0 42.6,69.4 43.0,70.8 43.6,72.2 44.3,73.5 45.1,74.8 46.0,75.9 47.0,77.0 48.1,78.0 49.2,78.9 50.5,79.7 51.8,80.4 53.2,81.0 54.6,81.4 56.0,81.7 57.5,81.9 59.0,82.0 60.5,81.9 62.0,81.7 63.4,81.4 64.8,81.0 66.2,80.4 67.5,79.7 68.8,78.9 69.9,78.0 71.0,77.0 72.0,75.9 72.9,74.8 73.7,73.5 74.4,72.2 75.0,70.8 75.4,69.4 75.7,68.0 75.9,66.5"/><line class="curve" x1="59" y1="65" x2="67.0" y2="57.0"/><polygon class="dot" points="71.0,53.0 68.5,59.5 64.5,55.5"/><line class="curve2" x1="59" y1="65" x2="51.0" y2="57.0"/><polygon class="dot2" points="47.0,53.0 53.5,55.5 49.5,59.5"/><text class="ink" x="59.0" y="134" font-size="11" text-anchor="middle">Başlangıç</text><text class="dim" x="113" y="69.0" font-size="12" text-anchor="middle">→</text><line class="grid" x1="116" y1="116" x2="116" y2="14"/><line class="grid" x1="133" y1="116" x2="133" y2="14"/><line class="grid" x1="150" y1="116" x2="150" y2="14"/><line class="line" x1="167" y1="116" x2="167" y2="14"/><line class="grid" x1="184" y1="116" x2="184" y2="14"/><line class="grid" x1="201" y1="116" x2="201" y2="14"/><line class="grid" x1="218" y1="116" x2="218" y2="14"/><line class="grid" x1="116" y1="116" x2="218" y2="116"/><line class="grid" x1="116" y1="99" x2="218" y2="99"/><line class="grid" x1="116" y1="82" x2="218" y2="82"/><line class="line" x1="116" y1="65" x2="218" y2="65"/><line class="grid" x1="116" y1="48" x2="218" y2="48"/><line class="grid" x1="116" y1="31" x2="218" y2="31"/><line class="grid" x1="116" y1="14" x2="218" y2="14"/><polygon class="dot" opacity="0.14" points="179.0,77.0 180.0,75.9 180.9,74.8 181.7,73.5 182.4,72.2 183.0,70.8 183.4,69.4 183.7,68.0 183.9,66.5 184.0,65.0 183.9,63.5 183.7,62.0 183.4,60.6 183.0,59.2 182.4,57.8 181.7,56.5 180.9,55.2 180.0,54.1 179.0,53.0 177.9,52.0 176.8,51.1 175.5,50.3 174.2,49.6 172.8,49.0 171.4,48.6 170.0,48.3 168.5,48.1 167.0,48.0 165.5,48.1 164.0,48.3 162.6,48.6 161.2,49.0 159.8,49.6 158.5,50.3 157.2,51.1 156.1,52.0 155.0,53.0 154.0,54.1 153.1,55.2 152.3,56.5 151.6,57.8 151.0,59.2 150.6,60.6 150.3,62.0 150.1,63.5 150.0,65.0 150.1,66.5 150.3,68.0 150.6,69.4 151.0,70.8 151.6,72.2 152.3,73.5 153.1,74.8 154.0,75.9 155.0,77.0 156.1,78.0 157.2,78.9 158.5,79.7 159.8,80.4 161.2,81.0 162.6,81.4 164.0,81.7 165.5,81.9 167.0,82.0 168.5,81.9 170.0,81.7 171.4,81.4 172.8,81.0 174.2,80.4 175.5,79.7 176.8,78.9 177.9,78.0"/><polygon class="curve3" points="179.0,77.0 180.0,75.9 180.9,74.8 181.7,73.5 182.4,72.2 183.0,70.8 183.4,69.4 183.7,68.0 183.9,66.5 184.0,65.0 183.9,63.5 183.7,62.0 183.4,60.6 183.0,59.2 182.4,57.8 181.7,56.5 180.9,55.2 180.0,54.1 179.0,53.0 177.9,52.0 176.8,51.1 175.5,50.3 174.2,49.6 172.8,49.0 171.4,48.6 170.0,48.3 168.5,48.1 167.0,48.0 165.5,48.1 164.0,48.3 162.6,48.6 161.2,49.0 159.8,49.6 158.5,50.3 157.2,51.1 156.1,52.0 155.0,53.0 154.0,54.1 153.1,55.2 152.3,56.5 151.6,57.8 151.0,59.2 150.6,60.6 150.3,62.0 150.1,63.5 150.0,65.0 150.1,66.5 150.3,68.0 150.6,69.4 151.0,70.8 151.6,72.2 152.3,73.5 153.1,74.8 154.0,75.9 155.0,77.0 156.1,78.0 157.2,78.9 158.5,79.7 159.8,80.4 161.2,81.0 162.6,81.4 164.0,81.7 165.5,81.9 167.0,82.0 168.5,81.9 170.0,81.7 171.4,81.4 172.8,81.0 174.2,80.4 175.5,79.7 176.8,78.9 177.9,78.0"/><line class="curve" x1="167" y1="65" x2="178.4" y2="65.0"/><polygon class="dot" points="184.0,65.0 177.6,67.9 177.6,62.1"/><line class="curve2" x1="167" y1="65" x2="167.0" y2="53.6"/><polygon class="dot2" points="167.0,48.0 169.9,54.4 164.1,54.4"/><text class="ink" x="167.0" y="134" font-size="11" text-anchor="middle">Vᵀ: döndür</text><text class="dim" x="221" y="69.0" font-size="12" text-anchor="middle">→</text><line class="grid" x1="224" y1="116" x2="224" y2="14"/><line class="grid" x1="241" y1="116" x2="241" y2="14"/><line class="grid" x1="258" y1="116" x2="258" y2="14"/><line class="line" x1="275" y1="116" x2="275" y2="14"/><line class="grid" x1="292" y1="116" x2="292" y2="14"/><line class="grid" x1="309" y1="116" x2="309" y2="14"/><line class="grid" x1="326" y1="116" x2="326" y2="14"/><line class="grid" x1="224" y1="116" x2="326" y2="116"/><line class="grid" x1="224" y1="99" x2="326" y2="99"/><line class="grid" x1="224" y1="82" x2="326" y2="82"/><line class="line" x1="224" y1="65" x2="326" y2="65"/><line class="grid" x1="224" y1="48" x2="326" y2="48"/><line class="grid" x1="224" y1="31" x2="326" y2="31"/><line class="grid" x1="224" y1="14" x2="326" y2="14"/><polygon class="dot" opacity="0.14" points="299.0,74.6 301.0,73.7 302.9,72.8 304.4,71.8 305.8,70.7 306.9,69.7 307.8,68.5 308.5,67.4 308.9,66.2 309.0,65.0 308.9,63.8 308.5,62.6 307.8,61.5 306.9,60.3 305.8,59.3 304.4,58.2 302.9,57.2 301.0,56.3 299.0,55.4 296.9,54.6 294.5,53.9 292.0,53.2 289.4,52.7 286.6,52.2 283.8,51.9 280.9,51.6 278.0,51.5 275.0,51.4 272.0,51.5 269.1,51.6 266.2,51.9 263.4,52.2 260.6,52.7 258.0,53.2 255.5,53.9 253.1,54.6 251.0,55.4 249.0,56.3 247.1,57.2 245.6,58.2 244.2,59.3 243.1,60.3 242.2,61.5 241.5,62.6 241.1,63.8 241.0,65.0 241.1,66.2 241.5,67.4 242.2,68.5 243.1,69.7 244.2,70.7 245.6,71.8 247.1,72.8 249.0,73.7 251.0,74.6 253.1,75.4 255.5,76.1 258.0,76.8 260.6,77.3 263.4,77.8 266.2,78.1 269.1,78.4 272.0,78.5 275.0,78.6 278.0,78.5 280.9,78.4 283.8,78.1 286.6,77.8 289.4,77.3 292.0,76.8 294.5,76.1 296.9,75.4"/><polygon class="curve3" points="299.0,74.6 301.0,73.7 302.9,72.8 304.4,71.8 305.8,70.7 306.9,69.7 307.8,68.5 308.5,67.4 308.9,66.2 309.0,65.0 308.9,63.8 308.5,62.6 307.8,61.5 306.9,60.3 305.8,59.3 304.4,58.2 302.9,57.2 301.0,56.3 299.0,55.4 296.9,54.6 294.5,53.9 292.0,53.2 289.4,52.7 286.6,52.2 283.8,51.9 280.9,51.6 278.0,51.5 275.0,51.4 272.0,51.5 269.1,51.6 266.2,51.9 263.4,52.2 260.6,52.7 258.0,53.2 255.5,53.9 253.1,54.6 251.0,55.4 249.0,56.3 247.1,57.2 245.6,58.2 244.2,59.3 243.1,60.3 242.2,61.5 241.5,62.6 241.1,63.8 241.0,65.0 241.1,66.2 241.5,67.4 242.2,68.5 243.1,69.7 244.2,70.7 245.6,71.8 247.1,72.8 249.0,73.7 251.0,74.6 253.1,75.4 255.5,76.1 258.0,76.8 260.6,77.3 263.4,77.8 266.2,78.1 269.1,78.4 272.0,78.5 275.0,78.6 278.0,78.5 280.9,78.4 283.8,78.1 286.6,77.8 289.4,77.3 292.0,76.8 294.5,76.1 296.9,75.4"/><line class="curve" x1="275" y1="65" x2="303.4" y2="65.0"/><polygon class="dot" points="309.0,65.0 302.6,67.9 302.6,62.1"/><line class="curve2" x1="275" y1="65" x2="275.0" y2="57.0"/><polygon class="dot2" points="275.0,51.4 277.9,57.8 272.1,57.8"/><text class="ink" x="275.0" y="134" font-size="11" text-anchor="middle">Σ: esnet</text><text class="dim" x="329" y="69.0" font-size="12" text-anchor="middle">→</text><line class="grid" x1="332" y1="116" x2="332" y2="14"/><line class="grid" x1="349" y1="116" x2="349" y2="14"/><line class="grid" x1="366" y1="116" x2="366" y2="14"/><line class="line" x1="383" y1="116" x2="383" y2="14"/><line class="grid" x1="400" y1="116" x2="400" y2="14"/><line class="grid" x1="417" y1="116" x2="417" y2="14"/><line class="grid" x1="434" y1="116" x2="434" y2="14"/><line class="grid" x1="332" y1="116" x2="434" y2="116"/><line class="grid" x1="332" y1="99" x2="434" y2="99"/><line class="grid" x1="332" y1="82" x2="434" y2="82"/><line class="line" x1="332" y1="65" x2="434" y2="65"/><line class="grid" x1="332" y1="48" x2="434" y2="48"/><line class="grid" x1="332" y1="31" x2="434" y2="31"/><line class="grid" x1="332" y1="14" x2="434" y2="14"/><polygon class="dot" opacity="0.14" points="408.6,61.3 409.9,59.5 411.0,57.8 411.9,56.2 412.6,54.6 413.0,53.1 413.2,51.6 413.2,50.3 412.9,49.1 412.4,48.0 411.7,47.0 410.8,46.2 409.7,45.5 408.3,45.0 406.8,44.6 405.1,44.4 403.2,44.3 401.2,44.4 399.0,44.7 396.7,45.1 394.3,45.6 391.8,46.3 389.3,47.1 386.7,48.1 384.1,49.2 381.4,50.4 378.8,51.8 376.2,53.2 373.7,54.7 371.2,56.4 368.8,58.0 366.5,59.7 364.4,61.5 362.4,63.3 360.5,65.1 358.9,66.9 357.4,68.7 356.1,70.5 355.0,72.2 354.1,73.8 353.4,75.4 353.0,76.9 352.8,78.4 352.8,79.7 353.1,80.9 353.6,82.0 354.3,83.0 355.2,83.8 356.3,84.5 357.7,85.0 359.2,85.4 360.9,85.6 362.8,85.7 364.8,85.6 367.0,85.3 369.3,84.9 371.7,84.4 374.2,83.7 376.7,82.9 379.3,81.9 381.9,80.8 384.6,79.6 387.2,78.2 389.8,76.8 392.3,75.3 394.8,73.6 397.2,72.0 399.5,70.3 401.6,68.5 403.6,66.7 405.5,64.9 407.1,63.1"/><polygon class="curve3" points="408.6,61.3 409.9,59.5 411.0,57.8 411.9,56.2 412.6,54.6 413.0,53.1 413.2,51.6 413.2,50.3 412.9,49.1 412.4,48.0 411.7,47.0 410.8,46.2 409.7,45.5 408.3,45.0 406.8,44.6 405.1,44.4 403.2,44.3 401.2,44.4 399.0,44.7 396.7,45.1 394.3,45.6 391.8,46.3 389.3,47.1 386.7,48.1 384.1,49.2 381.4,50.4 378.8,51.8 376.2,53.2 373.7,54.7 371.2,56.4 368.8,58.0 366.5,59.7 364.4,61.5 362.4,63.3 360.5,65.1 358.9,66.9 357.4,68.7 356.1,70.5 355.0,72.2 354.1,73.8 353.4,75.4 353.0,76.9 352.8,78.4 352.8,79.7 353.1,80.9 353.6,82.0 354.3,83.0 355.2,83.8 356.3,84.5 357.7,85.0 359.2,85.4 360.9,85.6 362.8,85.7 364.8,85.6 367.0,85.3 369.3,84.9 371.7,84.4 374.2,83.7 376.7,82.9 379.3,81.9 381.9,80.8 384.6,79.6 387.2,78.2 389.8,76.8 392.3,75.3 394.8,73.6 397.2,72.0 399.5,70.3 401.6,68.5 403.6,66.7 405.5,64.9 407.1,63.1"/><line class="curve" x1="383" y1="65" x2="407.6" y2="50.8"/><polygon class="dot" points="412.4,48.0 408.3,53.7 405.4,48.7"/><line class="curve2" x1="383" y1="65" x2="379.0" y2="58.1"/><polygon class="dot2" points="376.2,53.2 381.9,57.3 376.9,60.2"/><text class="ink" x="383.0" y="134" font-size="11" text-anchor="middle">U: döndür</text></svg>
  <figcaption>Bir matrisin çembere yaptığı: önce $V^\mathsf{T}$ çemberi döndürüp mor ve turuncu yönleri eksenlere oturtuyor, sonra $\Sigma$ eksenler boyunca esnetiyor (burada 2 ve 0.8 kat), en son $U$ ortaya çıkan elipsi yerine döndürüyor.</figcaption>
</figure>

Anlamı çok güçlü: **en karmaşık görünen doğrusal dönüşüm bile bir
döndürme, eksenler boyunca bir esnetme ve bir döndürme daha.** Bütün
"asıl iş" ortadaki $\Sigma$'da; öteki iki matris yalnızca yön
değiştiriyor.

## Geometri: çember elipse dönüşür

Bir matris birim çemberi her zaman bir **elipse** götürür (ya da ezilirse
bir doğru parçasına). SVD bu elipsi tam olarak anlatır:

- Elipsin yarı eksen uzunlukları tekil değerler: $\sigma_1$ (en uzun),
  $\sigma_2$, …
- Eksenlerin yönleri $U$'nun sütunları: $\mathbf{u}_1, \mathbf{u}_2, \dots$
  (**sol tekil vektörler**)
- Çemberde bu eksenlere giden noktalar $V$'nin sütunları: $\mathbf{v}_1,
  \mathbf{v}_2, \dots$ (**sağ tekil vektörler**)

Kısacası:

$$
A\mathbf{v}_i = \sigma_i \mathbf{u}_i
$$

Özdeğer denklemine ($A\mathbf{v} = \lambda\mathbf{v}$) benziyor ama bir fark
var: girdi yönü ($\mathbf{v}_i$) ile çıktı yönü ($\mathbf{u}_i$) farklı
olabilir. Bu esneklik sayesinde SVD her matriste çalışıyor.

<figure class="fig">
<svg viewBox="0 0 360 270" width="360"><line class="grid" x1="20" y1="214" x2="20" y2="70"/><line class="grid" x1="56" y1="214" x2="56" y2="70"/><line class="line" x1="92" y1="214" x2="92" y2="70"/><line class="grid" x1="128" y1="214" x2="128" y2="70"/><line class="grid" x1="164" y1="214" x2="164" y2="70"/><line class="grid" x1="20" y1="214" x2="164" y2="214"/><line class="grid" x1="20" y1="178" x2="164" y2="178"/><line class="line" x1="20" y1="142" x2="164" y2="142"/><line class="grid" x1="20" y1="106" x2="164" y2="106"/><line class="grid" x1="20" y1="70" x2="164" y2="70"/><polygon class="dot" opacity="0.14" points="128.0,142.0 127.9,138.9 127.5,135.7 126.8,132.7 125.8,129.7 124.6,126.8 123.2,124.0 121.5,121.4 119.6,118.9 117.5,116.5 115.1,114.4 112.6,112.5 110.0,110.8 107.2,109.4 104.3,108.2 101.3,107.2 98.3,106.5 95.1,106.1 92.0,106.0 88.9,106.1 85.7,106.5 82.7,107.2 79.7,108.2 76.8,109.4 74.0,110.8 71.4,112.5 68.9,114.4 66.5,116.5 64.4,118.9 62.5,121.4 60.8,124.0 59.4,126.8 58.2,129.7 57.2,132.7 56.5,135.7 56.1,138.9 56.0,142.0 56.1,145.1 56.5,148.3 57.2,151.3 58.2,154.3 59.4,157.2 60.8,160.0 62.5,162.6 64.4,165.1 66.5,167.5 68.9,169.6 71.4,171.5 74.0,173.2 76.8,174.6 79.7,175.8 82.7,176.8 85.7,177.5 88.9,177.9 92.0,178.0 95.1,177.9 98.3,177.5 101.3,176.8 104.3,175.8 107.2,174.6 110.0,173.2 112.6,171.5 115.1,169.6 117.5,167.5 119.6,165.1 121.5,162.6 123.2,160.0 124.6,157.2 125.8,154.3 126.8,151.3 127.5,148.3 127.9,145.1"/><polygon class="curve3" points="128.0,142.0 127.9,138.9 127.5,135.7 126.8,132.7 125.8,129.7 124.6,126.8 123.2,124.0 121.5,121.4 119.6,118.9 117.5,116.5 115.1,114.4 112.6,112.5 110.0,110.8 107.2,109.4 104.3,108.2 101.3,107.2 98.3,106.5 95.1,106.1 92.0,106.0 88.9,106.1 85.7,106.5 82.7,107.2 79.7,108.2 76.8,109.4 74.0,110.8 71.4,112.5 68.9,114.4 66.5,116.5 64.4,118.9 62.5,121.4 60.8,124.0 59.4,126.8 58.2,129.7 57.2,132.7 56.5,135.7 56.1,138.9 56.0,142.0 56.1,145.1 56.5,148.3 57.2,151.3 58.2,154.3 59.4,157.2 60.8,160.0 62.5,162.6 64.4,165.1 66.5,167.5 68.9,169.6 71.4,171.5 74.0,173.2 76.8,174.6 79.7,175.8 82.7,176.8 85.7,177.5 88.9,177.9 92.0,178.0 95.1,177.9 98.3,177.5 101.3,176.8 104.3,175.8 107.2,174.6 110.0,173.2 112.6,171.5 115.1,169.6 117.5,167.5 119.6,165.1 121.5,162.6 123.2,160.0 124.6,157.2 125.8,154.3 126.8,151.3 127.5,148.3 127.9,145.1"/><line class="curve" x1="92" y1="142" x2="112.4" y2="121.6"/><polygon class="dot" points="117.5,116.5 114.3,124.9 109.1,119.7"/><line class="curve2" x1="92" y1="142" x2="112.4" y2="162.4"/><polygon class="dot2" points="117.5,167.5 109.1,164.3 114.3,159.1"/><text class="ink" x="121.5" y="114.5" font-size="12" text-anchor="start">v₁</text><text class="ink" x="121.5" y="179.5" font-size="12" text-anchor="start">v₂</text><text class="ink" x="92.0" y="234" font-size="12" text-anchor="middle">Birim çember</text><line class="grid" x1="214" y1="238" x2="214" y2="14"/><line class="grid" x1="230" y1="238" x2="230" y2="14"/><line class="grid" x1="246" y1="238" x2="246" y2="14"/><line class="grid" x1="262" y1="238" x2="262" y2="14"/><line class="line" x1="278" y1="238" x2="278" y2="14"/><line class="grid" x1="294" y1="238" x2="294" y2="14"/><line class="grid" x1="310" y1="238" x2="310" y2="14"/><line class="grid" x1="326" y1="238" x2="326" y2="14"/><line class="grid" x1="342" y1="238" x2="342" y2="14"/><line class="grid" x1="214" y1="238" x2="342" y2="238"/><line class="grid" x1="214" y1="222" x2="342" y2="222"/><line class="grid" x1="214" y1="206" x2="342" y2="206"/><line class="grid" x1="214" y1="190" x2="342" y2="190"/><line class="grid" x1="214" y1="174" x2="342" y2="174"/><line class="grid" x1="214" y1="158" x2="342" y2="158"/><line class="grid" x1="214" y1="142" x2="342" y2="142"/><line class="line" x1="214" y1="126" x2="342" y2="126"/><line class="grid" x1="214" y1="110" x2="342" y2="110"/><line class="grid" x1="214" y1="94" x2="342" y2="94"/><line class="grid" x1="214" y1="78" x2="342" y2="78"/><line class="grid" x1="214" y1="62" x2="342" y2="62"/><line class="grid" x1="214" y1="46" x2="342" y2="46"/><line class="grid" x1="214" y1="30" x2="342" y2="30"/><line class="grid" x1="214" y1="14" x2="342" y2="14"/><polygon class="dot" opacity="0.14" points="326.0,62.0 325.8,55.3 325.3,49.1 324.4,43.5 323.1,38.5 321.5,34.2 319.6,30.6 317.3,27.7 314.8,25.6 311.9,24.2 308.9,23.6 305.5,23.8 302.0,24.7 298.3,26.4 294.4,28.9 290.4,32.2 286.3,36.1 282.2,40.7 278.0,46.0 273.8,51.9 269.7,58.3 265.6,65.3 261.6,72.7 257.7,80.5 254.0,88.7 250.5,97.2 247.1,105.9 244.1,114.7 241.2,123.6 238.7,132.5 236.4,141.4 234.5,150.2 232.9,158.8 231.6,167.1 230.7,175.1 230.2,182.8 230.0,190.0 230.2,196.7 230.7,202.9 231.6,208.5 232.9,213.5 234.5,217.8 236.4,221.4 238.7,224.3 241.2,226.4 244.1,227.8 247.1,228.4 250.5,228.2 254.0,227.3 257.7,225.6 261.6,223.1 265.6,219.8 269.7,215.9 273.8,211.3 278.0,206.0 282.2,200.1 286.3,193.7 290.4,186.7 294.4,179.3 298.3,171.5 302.0,163.3 305.5,154.8 308.9,146.1 311.9,137.3 314.8,128.4 317.3,119.5 319.6,110.6 321.5,101.8 323.1,93.2 324.4,84.9 325.3,76.9 325.8,69.2"/><polygon class="curve3" points="326.0,62.0 325.8,55.3 325.3,49.1 324.4,43.5 323.1,38.5 321.5,34.2 319.6,30.6 317.3,27.7 314.8,25.6 311.9,24.2 308.9,23.6 305.5,23.8 302.0,24.7 298.3,26.4 294.4,28.9 290.4,32.2 286.3,36.1 282.2,40.7 278.0,46.0 273.8,51.9 269.7,58.3 265.6,65.3 261.6,72.7 257.7,80.5 254.0,88.7 250.5,97.2 247.1,105.9 244.1,114.7 241.2,123.6 238.7,132.5 236.4,141.4 234.5,150.2 232.9,158.8 231.6,167.1 230.7,175.1 230.2,182.8 230.0,190.0 230.2,196.7 230.7,202.9 231.6,208.5 232.9,213.5 234.5,217.8 236.4,221.4 238.7,224.3 241.2,226.4 244.1,227.8 247.1,228.4 250.5,228.2 254.0,227.3 257.7,225.6 261.6,223.1 265.6,219.8 269.7,215.9 273.8,211.3 278.0,206.0 282.2,200.1 286.3,193.7 290.4,186.7 294.4,179.3 298.3,171.5 302.0,163.3 305.5,154.8 308.9,146.1 311.9,137.3 314.8,128.4 317.3,119.5 319.6,110.6 321.5,101.8 323.1,93.2 324.4,84.9 325.3,76.9 325.8,69.2"/><line class="curve" x1="278" y1="126" x2="309.6" y2="31.0"/><polygon class="dot" points="311.9,24.2 312.8,33.2 305.8,30.8"/><line class="curve2" x1="278" y1="126" x2="305.1" y2="135.0"/><polygon class="dot2" points="311.9,137.3 302.9,138.2 305.3,131.2"/><text class="ink" x="317.9" y="30.2" font-size="12" text-anchor="start">σ₁u₁</text><text class="ink" x="317.9" y="147.3" font-size="12" text-anchor="start">σ₂u₂</text><text class="ink" x="278.0" y="258" font-size="12" text-anchor="middle">A ile: elips</text></svg>
  <figcaption>$A = \begin{bmatrix} 3 & 0 \\ 4 & 5 \end{bmatrix}$ birim çemberi elipse götürüyor. Çemberdeki $\mathbf{v}_1$ (mor) elipsin en uzun eksenine, $\sigma_1\mathbf{u}_1$'e gidiyor; $\mathbf{v}_2$ (turuncu) en kısa eksenine. İki eksen birbirine dik; tekil değerler $\sigma_1 \approx 6.71$ ve $\sigma_2 \approx 2.24$.</figcaption>
</figure>

$\sigma_1$, $A$'nın bir birim vektörü **en fazla** kaç katına çıkarabileceği;
$\sigma_n$ en az kaç katına. Bu yüzden $\sigma_1$'e matrisin **normu** da
denir: $\|A\| = \sigma_1$.

## Tekil değerleri bulmak

SVD'yi elle bulmanın yolu $A^\mathsf{T}A$'dan geçiyor. $A = U\Sigma V^\mathsf{T}$
ise:

$$
A^\mathsf{T}A = V\Sigma^\mathsf{T}U^\mathsf{T}U\Sigma V^\mathsf{T} = V (\Sigma^\mathsf{T}\Sigma) V^\mathsf{T}
$$

($U^\mathsf{T}U = I$.) Bu, simetrik $A^\mathsf{T}A$ matrisinin
köşegenleştirmesi! Öyleyse:

- $A^\mathsf{T}A$'nın **özdeğerleri** tekil değerlerin **kareleri**: $\sigma_i^2$.
- $A^\mathsf{T}A$'nın **özvektörleri** sağ tekil vektörler $\mathbf{v}_i$.
- Sol tekil vektörler: $\mathbf{u}_i = \dfrac{A\mathbf{v}_i}{\sigma_i}$.

$A^\mathsf{T}A$ her zaman simetrik ve özdeğerleri hiç negatif değil
($\mathbf{v}^\mathsf{T}A^\mathsf{T}A\mathbf{v} = \|A\mathbf{v}\|^2 \ge 0$);
bu yüzden karekökleri alınabiliyor.

### Bir örnek

$$
A = \begin{bmatrix} 3 & 0 \\ 4 & 5 \end{bmatrix}
$$

**Adım 1 — $A^\mathsf{T}A$.**

$$
A^\mathsf{T}A = \begin{bmatrix} 3 & 4 \\ 0 & 5 \end{bmatrix} \begin{bmatrix} 3 & 0 \\ 4 & 5 \end{bmatrix} = \begin{bmatrix} 25 & 20 \\ 20 & 25 \end{bmatrix}
$$

**Adım 2 — Özdeğerleri.** İz $50$, determinant $625 - 400 = 225$:
$\lambda^2 - 50\lambda + 225 = (\lambda - 45)(\lambda - 5) = 0$.

$$
\sigma_1 = \sqrt{45} = 3\sqrt{5} \approx 6.71
\qquad
\sigma_2 = \sqrt{5} \approx 2.24
$$

**Adım 3 — Sağ tekil vektörler.** $A^\mathsf{T}A - 45I = \begin{bmatrix} -20 & 20 \\ 20 & -20 \end{bmatrix}$:
$y = x$. $A^\mathsf{T}A - 5I = \begin{bmatrix} 20 & 20 \\ 20 & 20 \end{bmatrix}$: $y = -x$.
Birim uzunluğa indirince:

$$
\mathbf{v}_1 = \tfrac{1}{\sqrt{2}}(1, 1)
\qquad
\mathbf{v}_2 = \tfrac{1}{\sqrt{2}}(1, -1)
$$

**Adım 4 — Sol tekil vektörler.** $A\mathbf{v}_1 = \tfrac{1}{\sqrt{2}}(3, 9)$;
$\sigma_1 = 3\sqrt{5}$'e bölünce $\mathbf{u}_1 = \tfrac{1}{\sqrt{10}}(1, 3)$.
$A\mathbf{v}_2 = \tfrac{1}{\sqrt{2}}(3, -1)$; $\sqrt{5}$'e bölünce
$\mathbf{u}_2 = \tfrac{1}{\sqrt{10}}(3, -1)$.

Sağlama: $\mathbf{u}_1 \cdot \mathbf{u}_2 = \tfrac{1}{10}(3 - 3) = 0$ (dik) ✓;
$\sigma_1\sigma_2 = \sqrt{45 \cdot 5} = 15 = |\det A|$ ✓.

## Tekil değerlerin söyledikleri

| Özellik | Tekil değerlerle |
|---|---|
| Rank | Sıfır olmayan tekil değer sayısı |
| Norm (en büyük esneme) | $\sigma_1$ |
| Kare matriste $\lvert\det A\rvert$ | $\sigma_1 \sigma_2 \cdots \sigma_n$ |
| Bütün elemanların kareleri toplamı | $\sigma_1^2 + \sigma_2^2 + \cdots$ |
| Tersinirlik (kare) | hepsi sıfırdan farklı |
| Koşul sayısı | $\sigma_1 / \sigma_n$ |

**Koşul sayısı** özellikle önemli: bir yönü çok esnetip başka bir yönü
çok az esneten bir matris ($\sigma_1 / \sigma_n$ büyük), elipsi iğne gibi
ince yapar. Böyle bir matrisle denklem çözmek, girdideki küçük bir
hatayı büyük bir hataya çeviriyor. Önceki bölümlerde "neredeyse tekil"
dediğimiz durum buydu.

**Özdeğerle ilişkisi.** Simetrik ve özdeğerleri negatif olmayan bir
matriste (kovaryans matrisleri böyle) SVD ile özdeğer ayrışımı aynı şey:
tekil değerler özdeğerler, $U = V$. Genel matrislerde ikisi farklı.

## Toplam olarak SVD: katmanlar

$U\Sigma V^\mathsf{T}$ çarpımını açınca $A$, **rankı 1 olan** basit
matrislerin toplamı olarak çıkıyor:

$$
A = \sigma_1 \mathbf{u}_1 \mathbf{v}_1^\mathsf{T} + \sigma_2 \mathbf{u}_2 \mathbf{v}_2^\mathsf{T} + \cdots + \sigma_r \mathbf{u}_r \mathbf{v}_r^\mathsf{T}
$$

Her $\mathbf{u}_i\mathbf{v}_i^\mathsf{T}$ bir sütun çarpı bir satır: bütün
satırları aynı vektörün katı olan bir matris (bir "katman"). Tekil değer o
katmanın ne kadar önemli olduğunu söylüyor. Katmanlar önem sırasına göre
dizili: ilk katman matrisin en büyük yapısını, sonrakiler giderek daha
küçük ayrıntıları taşıyor.

## Düşük ranklı yaklaşım

İlk $k$ katmanı alıp gerisini atarsak:

$$
A_k = \sigma_1 \mathbf{u}_1 \mathbf{v}_1^\mathsf{T} + \cdots + \sigma_k \mathbf{u}_k \mathbf{v}_k^\mathsf{T}
$$

**Eckart–Young teoremi:** Rankı $k$ olan bütün matrisler içinde $A$'ya
**en yakın** olanı $A_k$. Hata, atılan tekil değerlerle ölçülüyor
(elemanların farklarının kareleri toplamı):

$$
\|A - A_k\|^2 = \sigma_{k+1}^2 + \sigma_{k+2}^2 + \cdots
$$

Bu yüzden tekil değerlerin **karelerine** "enerji" denir. İlk $k$
katmanın taşıdığı pay:

$$
\frac{\sigma_1^2 + \cdots + \sigma_k^2}{\sigma_1^2 + \cdots + \sigma_r^2}
$$

<figure class="fig">
<svg viewBox="0 0 380 226" width="380"><rect class="dot" opacity="0.85" x="60" y="20.0" width="44" height="150.0" rx="3"/><text class="ink" x="82" y="14.0" font-size="12" text-anchor="middle">12</text><text class="ink" x="82" y="188" font-size="13" text-anchor="middle">σ₁</text><rect class="dot" opacity="0.85" x="130" y="107.5" width="44" height="62.5" rx="3"/><text class="ink" x="152" y="101.5" font-size="12" text-anchor="middle">5</text><text class="ink" x="152" y="188" font-size="13" text-anchor="middle">σ₂</text><rect class="dim" opacity="0.45" x="200" y="132.5" width="44" height="37.5" rx="3"/><text class="ink" x="222" y="126.5" font-size="12" text-anchor="middle">3</text><text class="ink" x="222" y="188" font-size="13" text-anchor="middle">σ₃</text><rect class="dim" opacity="0.45" x="270" y="157.5" width="44" height="12.5" rx="3"/><text class="ink" x="292" y="151.5" font-size="12" text-anchor="middle">1</text><text class="ink" x="292" y="188" font-size="13" text-anchor="middle">σ₄</text><line class="line" x1="40" y1="170" x2="340" y2="170"/><text class="ink" x="190" y="214" font-size="12" text-anchor="middle">İlk ikisi enerjinin %94'ü: (144 + 25) / 179</text></svg>
  <figcaption>Tekil değerleri 12, 5, 3 ve 1 olan bir matriste ilk iki katman karelerin toplamının (179) 169'unu taşıyor: rankı 2 olan yaklaşım matrisin %94'ünü koruyor, atılan kısmın hatası $\sqrt{9 + 1} \approx 3.16$.</figcaption>
</figure>

### Görüntü sıkıştırma

Gri tonlu bir fotoğraf $m \times n$ bir matris. Tamamını saklamak
$m \cdot n$ sayı gerektiriyor. İlk $k$ katmanı saklamak için her katmanda
bir $\mathbf{u}_i$ ($m$ sayı), bir $\mathbf{v}_i$ ($n$ sayı) ve bir
$\sigma_i$ yeterli:

$$
k\,(m + n + 1) \text{ sayı}
$$

$1000 \times 1000$ bir fotoğrafta $k = 50$ için $50 \cdot 2001 = 100\,050$
sayı; orijinalin yaklaşık onda biri. Gerçek fotoğraflarda tekil değerler
hızla küçüldüğü için ($\sigma_{50}$, $\sigma_1$'in yanında çok küçük) göz
farkı zor seçiyor.

## Makine öğrenmesinde SVD

**PCA.** Ortalaması çıkarılmış veri matrisi $X$'in SVD'si doğrudan PCA'yı
veriyor: $\mathbf{v}_i$'ler verinin temel yönleri (bileşenleri),
$\sigma_i^2 / (n - 1)$ o yöndeki varyans. Kütüphaneler PCA'yı kovaryans
matrisinin özdeğerleriyle değil, SVD ile hesaplıyor; sayısal olarak daha
kararlı.

**Öneri sistemleri.** Kullanıcı × film puan matrisinin düşük ranklı
yaklaşımı: her kullanıcı ve her film birkaç "gizli özellikle" (aksiyon
yoğunluğu, romantizm, …) anlatılıyor. $\mathbf{u}_i$'ler kullanıcıların,
$\mathbf{v}_i$'ler filmlerin bu özelliklerdeki ağırlıkları. Boş hücreler
(izlenmemiş filmler) bu yaklaşımla tahmin ediliyor.

**Metinlerde anlam.** Belge × kelime sıklık matrisinin SVD'si (gizli
anlamsal analiz): "araba" ile "otomobil" gibi aynı katmanda birlikte
geçen kelimeler yakın vektörlere düşüyor.

**Gürültü temizleme.** Veride gerçek yapı büyük tekil değerlerde,
rastgele gürültü ise çok sayıda küçük tekil değere yayılmış olur. Küçük
katmanları atmak gürültünün çoğunu siliyor.

**Sayısal rank.** Gerçek verilerde tekil değerler tam sıfır çıkmaz;
$10^{-12}$ gibi çok küçük değerler "aslında sıfır" sayılır. Kütüphanelerin
`matrix_rank` fonksiyonları rankı böyle, tekil değerlere bakarak buluyor.

## Sık yapılan hatalar

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Yanlış</h4>
      <p>Tekil değerler = $A$'nın özdeğerleri</p>
      <p>SVD yalnızca kare matriste var</p>
      <p>Tekil değer negatif olabilir</p>
      <p>$\sigma_i$ = $A^\mathsf{T}A$'nın özdeğerleri</p>
    </div>
    <div class="ok">
      <h4>Doğru</h4>
      <p>Tekil değerler = $A^\mathsf{T}A$'nın özdeğerlerinin karekökleri</p>
      <p>Her $m \times n$ matrisin SVD'si var</p>
      <p>$\sigma_i \ge 0$, büyükten küçüğe sıralı</p>
      <p>$\sigma_i^2$ = $A^\mathsf{T}A$'nın özdeğerleri</p>
    </div>
  </div>
  <figcaption>Tekil değer ile özdeğer yalnızca simetrik ve özdeğerleri negatif olmayan matrislerde çakışır.</figcaption>
</figure>

- **Karekökü unutmak.** $A^\mathsf{T}A$'nın özdeğerleri tekil değerlerin
  karesi; $\sigma$ için karekök alınır.
- **$\mathbf{u}_i$'yi bölmeden bırakmak.** $A\mathbf{v}_i$'nin uzunluğu
  $\sigma_i$; $\mathbf{u}_i$ birim vektör olmalı.
- **Düşük ranklı yaklaşımda en küçük tekil değerleri tutmak.** Önemli
  olan büyükler; atılanlar küçükler.

## Özet

- Her matris için $A = U\Sigma V^\mathsf{T}$: döndür ($V^\mathsf{T}$), eksenler boyunca esnet ($\Sigma$), döndür ($U$).
- $A\mathbf{v}_i = \sigma_i\mathbf{u}_i$; birim çember, yarı eksenleri $\sigma_i$ olan bir elipse gider.
- Hesap: $A^\mathsf{T}A$'nın özdeğerleri $\sigma_i^2$, özvektörleri $\mathbf{v}_i$; $\mathbf{u}_i = A\mathbf{v}_i / \sigma_i$.
- Rank = sıfır olmayan $\sigma$ sayısı; $\|A\| = \sigma_1$; kare matriste $|\det A| = \prod \sigma_i$; koşul sayısı $\sigma_1 / \sigma_n$.
- $A = \sum \sigma_i \mathbf{u}_i\mathbf{v}_i^\mathsf{T}$: önem sırasına göre rank-1 katmanlar.
- İlk $k$ katman en iyi rank-$k$ yaklaşım (Eckart–Young); hata $\sqrt{\sigma_{k+1}^2 + \cdots}$; enerji payı $\sum_{i \le k} \sigma_i^2 / \sum \sigma_i^2$.
- Saklama: $k(m + n + 1)$ sayı.
- ML: PCA, öneri sistemleri, metinlerde anlam, gürültü temizleme, sayısal rank.
