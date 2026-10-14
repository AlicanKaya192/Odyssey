| Terim | Anlamı |
|---|---|
| **Şablon** (template) | Değişkenleri yerine konarak her çağrıda prompt kuran sabit metin |
| **Yer tutucu** (placeholder) | Şablonda değişkenin konacağı işaret: `{message}`, `$name`, `{{order_id}}` |
| **Kaçırma** | Şablon işaretiyle karışan karakteri ikiye katlamak: `{{` ve `}}` |
| **Gürültülü hata** | Sorunu çalışmadan önce bildiren hata (`substitute`, `KeyError`) |
| **Sessiz hata** | Sorunu söylemeden devam eden davranış (`safe_substitute`) |
| **Tek geçişte doldurma** | Yerleştirilen değerin bir daha taranmaması |
| **Şablon sürümü** | Şablonun her değişikliğinde artan numara; kayda yazılır |

**Akılda tut:**

- `str.format` JSON örneğindeki `{"category": ...}` kısmını değişken sandı
  ve `KeyError` verdi.
- `safe_substitute` eksik `$order_id`'yi prompt'ta bıraktı ve hiçbir şey
  söylemedi.
- Sırayla `replace` yapan sürüm müşterinin mesajındaki `{{order_id}}`'yi
  doldurdu; tek geçişli `render` mesajı olduğu gibi bıraktı.
- 62 kelimelik mesajı 24 kelimeye baştan kesince asıl istek kayboldu;
  ortadan kesince kaldı.
