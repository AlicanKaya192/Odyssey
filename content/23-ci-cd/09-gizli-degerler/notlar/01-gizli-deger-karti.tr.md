**Nerede ne durur?**

| Ne | Nerede | İş akışında | Kayıtta |
|---|---|---|---|
| Şifre, API anahtarı | Settings › Secrets and variables › Actions › Secrets | `${{ secrets.AD }}` | `***` (birebir değer) |
| Gizli olmayan ayar | Aynı sayfa › Variables | `${{ vars.AD }}` | Açık |
| Çalışmanın geçici anahtarı | GitHub kendiliğinden verir | `${{ secrets.GITHUB_TOKEN }}` | `***` |

**Gizli değeri kullanmak**

```yaml
      - run: python send_report.py
        env:
          REPORT_API_KEY: ${{ secrets.REPORT_API_KEY }}
```

```python
import os

key = os.environ["REPORT_API_KEY"]
```

**Ad kuralları**

- Harf, rakam, alt çizgi. Boşluk yok.
- Rakamla başlamaz; `GITHUB_` ile başlamaz.
- Değer kaydedildikten sonra sayfada gösterilmez; yalnızca değiştirilir.

**Maskeleme ne yapar, ne yapamaz?**

| Durum | Kayıtta |
|---|---|
| Değer birebir yazdırıldı | `***` |
| Değer base64'e, JSON'a ya da başka biçime çevrildi | Açıkça görünür |
| Değerin bir parçası yazdırıldı | Açıkça görünür |
| Türetilen değer `::add-mask::` ile eklendi | `***` |

```yaml
      - run: echo "::add-mask::$DERIVED"
```

**Ne zaman gelmez?**

- Fork'tan açılan PR'da gizli değerler boş gelir (`GITHUB_TOKEN` yalnızca
  okuma yetkisiyle gelir).
- Gizli değer isteyen adımlar `main`'e gönderimde ya da etiket gelince
  çalışır, PR'da değil.

**Anahtar sızdıysa**

1. Servisten eski anahtarı **iptal et**.
2. Yeni anahtar al, kasaya yaz.
3. Satırı silmek tek başına yetmez: git geçmişi saklar.
