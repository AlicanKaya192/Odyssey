**Üç dal stratejisi**

| | Gövde tabanlı | GitHub flow | GitFlow |
|---|---|---|---|
| Dal ömrü | Saatler, bir-iki gün | Günler | Haftalar olabilir |
| Uzun yaşayan dallar | Yalnızca `main` | Yalnızca `main` | `main` + `develop` |
| Sürüm | Sürekli | `main`'den, istenince | Sürüm dalından |
| Gerektirdiği | Çok güçlü testler | PR ve CI | Daha çok elle iş |

**`main` için kurallar (Settings › Rules)**

| Kural | Ne engeller |
|---|---|
| PR zorunlu | `main`'e doğrudan gönderim |
| Onay zorunlu | İncelenmemiş kodun girmesi |
| Zorunlu kontroller | Testleri geçmeyen kodun girmesi |
| Dal güncel olmalı | Ayrı ayrı geçen iki PR'ın birlikte bozması |
| Zorla gönderim ve silme yasak | Geçmişin yeniden yazılması |
| Birleştirme kuyruğu | "Güncelle, yeniden sına" yorgunluğu |

**Zorunlu kontrolün adı**

- İş akışının değil **işin** adı: `lint`, `test`.
- `name:` verilmişse o ad.
- Matriste her kopya ayrı: `test (3.12)`, `test (3.13)`.
- Ad değişince kural güncellenmezse PR sonsuza kadar bekler.

**PR'ı bekleten durumlar**

| Durum | Neden |
|---|---|
| İşin adı değişti | Kuraldaki adla sonuç gelmiyor |
| Yol süzgeci iş akışını başlatmadı | Başlamayan iş akışı sonuç bildirmez |
| `[skip ci]` | Aynı: çalışma yok, sonuç yok |
| Kuyrukta takıldı | İş akışı `merge_group`'u dinlemiyor |

**Atlanan iş**

`if:` ile atlanan iş (skipped) zorunlu kontrol için **başarılı** sayılır.
Kapı işinin `if: always()` taşıması bu yüzden şart.
