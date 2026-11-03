## Kavramlar

| Kavram | Anlamı |
|---|---|
| 3-2-1 | 3 kopya, 2 farklı ortam, 1 dışarıda |
| Çevrimdışı / değiştirilemez yedek | Ağdan ulaşılamayan ya da yazıldıktan sonra değiştirilemeyen kopya |
| RPO | Kabul edilebilir en uzun veri kaybı |
| RTO | Kabul edilebilir en uzun kesinti |
| Tam yedek | Bütün verinin kopyası |
| Artımlı yedek | Son yedekten bu yana değişenler |
| Dede-baba-oğul | Günlük, haftalık, aylık yedekleri farklı sürelerle saklamak |

## Yedek türleri

| Tür | Yedekleme | Geri yükleme |
|---|---|---|
| Tam | Yavaş, çok yer | Hızlı: tek kopya yeter |
| Artımlı | Hızlı, az yer | Yavaş: son tam + bütün artımlılar |
| Fark (differential) | Orta | Son tam + son fark |

## Python kalıpları

- En uzun boşluk: `max((b - a) for a, b in zip(zamanlar, zamanlar[1:]))`.
- Saat: `fark.total_seconds() / 3600`.
- Geri yükleme süresi: `hazirlik + boyut / hiz`.
- Karşılaştırma: `sha256(geri_yuklenen) == sha256(asil)`.
- Pazar mı: `d.weekday() == 6`; ayın ilk günü mü: `d.day == 1`.

## Akılda tutulacak

- Ağdan ulaşılabilen yedek fidye yazılımına karşı korumaz.
- RPO yedek sıklığını, RTO geri yükleme hızını belirler.
- Geri yüklemesi denenmemiş yedeğe güvenilmez.
- Yedekler de şifrelenir ve erişimi en az yetkiyle sınırlanır: yedek,
  verinin bir kopyasıdır ve aynı korumayı ister.
