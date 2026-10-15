**Yayın günü, adım adım**

1. `main` yeşil mi? Son çalışmada `ci-ok` geçmiş olmalı.
2. `pyproject.toml`'da sürümü yükselt (`0.3.0` → `0.4.0`, onuncu bölümdeki
   kurala göre).
3. `CHANGELOG.md`'ye yeni sürümün bölümünü yaz: `## [0.4.0]`.
4. Bu ikisini bir PR ile `main`'e al.
5. `main`'in o commit'ine etiket koy ve gönder:

```text
git tag v0.4.0
git push origin v0.4.0
```

6. Etiketin çalışmasını izle: `release` işi sürüm sayfasını açar.
7. Sürüm sayfasında `dist` dosyalarını ve notları kontrol et.

**Bir şey ters giderse**

| Durum | Ne yapılır |
|---|---|
| `check_version.py` düştü (etiket ≠ sürüm) | Yayın olmadı. Etiketi sil, sürümü düzelt, yeniden etiketle |
| Testler etikette düştü | Yayın olmadı. Düzeltmeyi `main`'e al, **yeni** sürüm numarasıyla etiketle |
| Yayın çıktı ama paket hatalı | Yayını geri çekme; düzeltmeyle yeni bir küçük sürüm (`0.4.1`) |

```text
git tag -d v0.4.0
git push origin --delete v0.4.0
```

**Yapılmayacaklar**

- Yayınlanmış bir etiketi başka bir commit'e taşımak: o sürümü indiren
  herkes başka bir kod görür.
- Yayını hattı atlayıp elle yapmak: test edilen paket ile yayınlanan
  paket ayrışır.
- Etiketi `main` dışındaki bir dala koymak.

**Sürüm notunu dosyadan almak**

`--generate-notes` PR başlıklarından not üretir. Elle yazılmış notlar
isteniyorsa `CHANGELOG.md`'deki `## [0.4.0]` bölümü bir dosyaya çıkarılıp
`gh release create ... --notes-file notes.md` ile verilir.
