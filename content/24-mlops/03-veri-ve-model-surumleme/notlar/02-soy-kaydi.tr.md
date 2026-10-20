Soy (lineage), bir modelden geriye doğru onu üreten her şeye giden
zincirdir:

<figure class="fig">
  <div class="flow">
    <span class="node acc">Model</span>
    <span class="arrow">→</span>
    <span class="node">Eğitim verisi</span>
    <span class="arrow">→</span>
    <span class="node">Ham veri</span>
  </div>
  <figcaption>Her ok "şundan üretildi" demek. Zincirin her halkası bir özetle tanınır.</figcaption>
</figure>

## Soy kaydında ne olur?

| Alan | Örnek | Neden |
|---|---|---|
| Modelin özeti | `"model": "dd0ba2458f51"` | Hangi model dosyası |
| Verinin özeti | `"data": "fd8e64e44454"` | Hangi veriyle eğitildi |
| Ayarlar | `{"n_estimators": 50, "random_state": 0}` | Nasıl eğitildi |
| Kütüphane sürümü | `"scikit-learn": "1.9.1"` | Hangi ortamda |
| Kodun sürümü | Git commit kimliği | Hangi eğitim kodu |
| Üst veri | Verinin türetildiği eski sürümün özeti | Verinin kendi soyu |

## Sorular ve cevabın yeri

| Soru | Cevap |
|---|---|
| Bu model hangi veriyle eğitildi? | Soy kaydındaki veri özeti → depodan `get` |
| Veride ne değişti? | İki sürümün kimlik sütunuyla farkı |
| Bu veriyle eğitilmiş başka model var mı? | Soy kayıtlarında aynı veri özetini ara |
| Aynı modeli yeniden üretebilir miyim? | Aynı veri + ayar + ortam; model özeti aynı çıkmalı ya da tahminler aynı olmalı |

## Kontrol listesi

- Veri ve model dosyaları `.gitignore`'da, işaret dosyaları Git'te mi?
- Depo başka bir yerde de duruyor mu? Tek diskte duran depo, disk
  bozulunca bütün sürümleri birlikte götürür.
- Geri getirilen dosyanın özeti denetleniyor mu?
- Her modelin bir soy kaydı var mı?

## Yapma

- Veri dosyasının yerinde değiştirilip aynı adla bırakılmasına izin
  verme; yeni içerik yeni sürüm demek.
- Depodan dosya silme; eski bir modelin verisi bir gün gerekecek.
- Tanımadığın bir kaynaktan gelen `pickle` dosyasını açma.
