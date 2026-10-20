İki eğitim kaydı (`a`, `b`) sözlük olarak veriliyor: `config`, `data` (parmak izi), `library` (sürüm) ve `accuracy`.

`compare_runs(a, b)` fonksiyonunu yaz:

- `config`, `data` ve `library` alanlarından değişenleri **bu sırayla** bul.
- Değişen varsa `"changed: "` ve aralarında virgül ve boşluk olan adlarını döndür: `"changed: data, library"`.
- Hiçbiri değişmediyse doğruluk aynıysa `"reproducible"`, farklıysa `"not reproducible"` döndür: girdiler aynıyken sonuç değiştiyse eğitim tekrarlanabilir değildir.

**Beklenen çıktı:**

```
reproducible
not reproducible
changed: data
changed: config, library
```
