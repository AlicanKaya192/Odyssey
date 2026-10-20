Bir eğitimi altı ay sonra yeniden üretebilmek için kaydında şunlar
olmalı:

| Alan | Örnek | Neden |
|---|---|---|
| Yapılandırma | `{"rows": 2000, "split_seed": 0, ...}` | Bütün ayarlar ve tohumlar |
| Verinin parmak izi | `"a91a352912da"` | Tam olarak hangi veri |
| Kodun sürümü | Git commit kimliği | Hangi eğitim kodu |
| Ortam | Python ve kütüphane sürümleri | Aynı hesap yöntemleri |
| Sonuç | `"accuracy": 0.768` | Yeniden üretince karşılaştırmak için |
| Tarih | `"2026-10-20"` | Ne zaman |

Kodun sürümü bu bölümde yazılmadı, çünkü alıştırmalar bir Git deposunda
çalışmıyor. Gerçek bir projede `git rev-parse HEAD` komutunun verdiği
commit kimliği kayda eklenir (Git patikası).

## Kayıt örneği

```text
{
  "config": {"rows": 2000, "data_seed": 7, "split_seed": 0,
             "n_estimators": 50, "model_seed": 0},
  "data": "a91a352912da",
  "python": "3.14.7",
  "scikit-learn": "1.9.1",
  "accuracy": 0.768
}
```

## Kontrol listesi

- Eğitim tek bir fonksiyonda ve yalnızca yapılandırmaya bakıyor mu?
- Her rastgele adımın kendi tohumu var mı?
- Kütüphane sürümleri `==` ile sabit mi?
- Kayıt modelin yanında saklanıyor mu?
- Aynı yapılandırmayla iki eğitimin aynı tahminleri verdiğini sınayan
  bir test var mı?

## Yapma

- Tohumları deneyip en iyi sonucu vereni seçme.
- Ayarı kodun içinde değiştirip kayda yazmadan bırakma: değişen her ayar
  yapılandırmadan geçmeli.
- Veriyi dosya adıyla tanıma; içerik değişmiş olabilir.
