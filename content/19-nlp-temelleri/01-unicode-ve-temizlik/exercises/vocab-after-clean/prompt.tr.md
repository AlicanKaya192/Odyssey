Başlangıç kodunda `vocabulary` ve `vocab_sizes` hazır; `clean` ise metni
olduğu gibi döndürüyor. `clean(text)` dersteki temizleme hattını sırasıyla
uygulasın:

1. `html.unescape`
2. etiketleri boşluğa çevir: `re.sub(r"<[^>]+>", " ", text)`
3. `unicodedata.normalize("NFKC", text)`
4. tırnakları düzle: `text.translate(QUOTES)`
5. sıfır genişlikli boşluğu sil: `chr(0x200B)`
6. boşlukları teke indir

Çıktı `[temizlemeden, temizledikten sonra]` kelime sayısı.

**Beklenen çıktı:**

```
[2225, 362]
```
