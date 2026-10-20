Sonucu oynatan şey, nasıl sabitlenir:

| Kaynak | Ne yapıyor | Nasıl sabitlenir |
|---|---|---|
| `train_test_split` | Bölmeden önce satırları karıştırıyor | `random_state=0` |
| `RandomForestClassifier` | Her ağaçta rastgele satır ve sütun seçiyor | `random_state=0` |
| `KFold(shuffle=True)` | Katlara bölmeden önce karıştırıyor | `random_state=0` |
| `KMeans` | Başlangıç merkezlerini rastgele seçiyor | `random_state=0` |
| Python `random` | Ortak üreteç | Kendi üretecin: `rng = random.Random(0)` |
| NumPy | Ortak üreteç | Kendi üretecin: `rng = np.random.default_rng(0)` |
| Veri | İçeriği sessizce değişebiliyor | Parmak izi: içeriğin SHA-256 özeti |
| Kütüphaneler | Sürüm değişince sonuç değişebiliyor | `requirements.txt`'te `==` ile sabitle |

## Kurallar

- Tohumu **her rastgele adıma ayrı** ver; programın başına tek bir
  `random.seed(0)` yazmakla yetinme.
- Tohum eğitimden **önce** seçilir; sonuca göre değiştirilmez.
- İki modeli **aynı bölmede** karşılaştır; tek bölmenin şansından
  kurtulmak için çapraz doğrulama kullan.
- `json.dumps(..., sort_keys=True)`: aynı sözlük, anahtar sırası farklı
  diye farklı özet vermesin.
- Tekrarlanabilirliği **test et**: aynı ayarla iki eğitim, aynı
  tahminler (`predict_proba` karşılaştırması).

## Terimler

- **Tekrarlanabilir** (reproducible): aynı girdilerle yeniden
  çalıştırınca aynı sonucu veren.
- **Sözde rastgele** (pseudo-random): bir tohumdan hesaplanan, rastgele
  görünen sayı dizisi.
- **Tohum** (seed): bu dizinin başlangıç sayısı.
- **Özet** (hash): veriden hesaplanan sabit uzunlukta metin; tek değer
  değişince tamamı değişir.
