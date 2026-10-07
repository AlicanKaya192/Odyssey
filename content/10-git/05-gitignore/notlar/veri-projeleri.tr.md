Veri bilimi ve makine öğrenmesi projelerinde Git'in en sık karşılaştığı
sorun büyük dosyalar ve gizli anahtarlar. Bu notta neyin depoya girip neyin
girmemesi gerektiği var.

## Depoya girsin

- Kod: `.py`, not defterleri (`.ipynb`; çıktıları temizlenmişse daha iyi).
- Küçük örnek veri: testlerin ve derslerin kullandığı birkaç yüz satırlık
  `sample.csv`.
- Ortamın tarifi: `requirements.txt` ya da `environment.yml`.
- Belgeler: `README.md`, ayar **örneği** (`.env.example`).

## Depoya girmesin

| Ne | Neden | Desen |
|---|---|---|
| Ham veri | Büyük; her değişimde depo şişer. | `data/raw/` |
| Ara çıktılar | Koddan yeniden üretilir. | `data/processed/`, `*.parquet` |
| Eğitilmiş modeller | Yüzlerce MB olabilir. | `models/`, `*.pkl`, `*.joblib` |
| Sanal ortam | Her bilgisayarda yeniden kurulur. | `.venv/`, `venv/` |
| Önbellek | Python ve Jupyter'in kendi dosyaları. | `__pycache__/`, `.ipynb_checkpoints/` |
| Gizli bilgiler | Şifre, API anahtarı. | `.env`, `*.key`, `credentials.json` |

## `.env` ve `.env.example`

Gizli ayarlar `.env`'de durur ve **görmezden gelinir**. Hangi ayarların
gerektiğini anlatmak için değerleri boş bir örnek commit'lenir:

```text
# .env.example (commit'lenir)
DATABASE_URL=
API_KEY=

# .env (görmezden gelinir; gerçek değerler burada)
DATABASE_URL=postgres://...
API_KEY=sk-...
```

Projeyi alan kişi `.env.example`'ı `.env` olarak kopyalayıp kendi
değerlerini yazar.

## Büyük dosya yine de gerekiyorsa

GitHub tek dosyada 100 MB'ın üstünü kabul etmiyor (50 MB'tan büyüklerde
uyarıyor). Büyük dosyalar için **Git LFS** (*Large File Storage*) adında bir
eklenti var: dosyanın kendisi ayrı bir yerde durur, depoda yalnızca ona işaret
eden küçük bir metin olur. Veri setleri için çoğu zaman daha iyisi veriyi
depoya hiç koymamak ve README'de nereden indirileceğini yazmaktır.
