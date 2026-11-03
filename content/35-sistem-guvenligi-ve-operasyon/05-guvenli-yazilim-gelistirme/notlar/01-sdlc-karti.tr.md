## Adım adım güvenlik işi

| Adım | İş | Çıktı |
|---|---|---|
| Gereksinim | Güvenlik gereksinimleri | "Yalnızca sahibi siler" gibi sınanabilir cümleler |
| Tasarım | Tehdit modeli, güvenli varsayılanlar | Tehdit listesi, önlem kararları |
| Kodlama | Güvenli kodlama, kod inceleme | İncelenmiş değişiklikler |
| Doğrulama | Güvenlik testleri, statik analiz, bağımlılık taraması | Test ve tarama raporları |
| Yayın ve bakım | Yayın kapısı, yama, izleme | Kapıdan geçmiş sürüm, olay kayıtları |

## Dört ilke

| İlke | Kısaca |
|---|---|
| Güvenli başarısız ol | Hata olunca reddet (fail closed) |
| Güvenli varsayılanlar | Tehlikeli ayar ancak açıkça istenince |
| Girdiyi doğrula | İzin listesi: iyiyi tarif et |
| Derinlemesine savunma | Tek bir denetime güvenme |

## Python kalıpları

- Yalnızca beklenen hatayı yakala: `except KeyError: return False`.
- Varsayılanların üstüne yalnızca tanınan anahtarlar:
  `if key in DEFAULTS: config[key] = value`.
- Sayı doğrulama: `text.isdigit()` ve aralık `1 <= value <= 100`.
- Yayın kapısı: `[item for item, done in checklist.items() if not done]`.

## Akılda tutulacak

- `except Exception: return True` bir güvenlik denetiminde en tehlikeli
  iki satırdır.
- Güvenlik testinin değeri "olmamalı" durumlarındadır.
- Kara liste unutulur; izin listesi kendiliğinden reddeder.
- Kapı "bu seferlik" geçilmez.
