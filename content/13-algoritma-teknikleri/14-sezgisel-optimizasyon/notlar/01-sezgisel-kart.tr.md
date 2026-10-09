## Üç aile

| Aile | Ne yapar | Örnek |
|---|---|---|
| Kurucu (constructive) | çözümü adım adım kurar | en yakın komşu, açgözlü sırt çantası |
| Yerel arama | elindeki çözümü küçük değişikliklerle iyileştirir | 2-opt, tepe tırmanma |
| Üst-sezgisel (metaheuristic) | yerel en iyiden kaçmak için kural ekler | tavlama benzetimi, genetik algoritma, tabu arama |

Sık kullanılan düzen: **önce kur, sonra iyileştir** (en yakın komşu + 2-opt).

## Tavlama benzetiminin ayarları

| Ayar | Etkisi |
|---|---|
| Başlangıç sıcaklığı | yüksekse başta neredeyse her adım kabul |
| Soğuma oranı | `0.99`–`0.999`; yavaş soğuma daha iyi, daha uzun |
| Adım boyu | çukurlar arası mesafeyi aşabilecek kadar olmalı |
| Adım sayısı | sıcaklık sıfıra yaklaşana kadar |

Dersteki tavlama, öteki ayarlar aynı kalıp adım boyu `±1` yapılınca 20
başlangıçtan yalnızca 6'sında en iyiyi buluyor; `±3` ile 20'sinde. Ayar
problemin ölçeğine bağlı.

## Sık hatalar

- Sezgiselin bulduğuna "en iyi" demek: yalnızca "bulunan en iyi".
- Tek bir rastgele koşuya güvenmek: birkaç tohum dene, en iyisini al ve
  dağılıma bak.
- En iyi bilinen çözümü kaydetmeyi unutmak: tavlama kötü adımları kabul ettiği
  için son durum en iyi durum olmayabilir (`best` ayrı tutulur).
- Değerlendirmeyi pahalı yapmak: 2-opt'ta her adımda bütün turu yeniden
  ölçmek yerine yalnızca değişen iki kenarı hesaplamak çok daha hızlı.
