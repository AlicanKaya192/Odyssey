Adımlı cevap isteyen bir talimat ve onu kullanan program şöyle kurulur.

**Talimat:**

```text
Work out the answer step by step, one operation per line,
in the form "a + b = c". The last line must be
"Answer: <number>" with no other text.
```

**Program:**

| Adım | Ne yapılır? | Düşerse |
|---|---|---|
| 1 | Son satırı ayrıştır (`^Answer:\s*sayı$`) | Yeniden sor ya da insana gönder |
| 2 | Adımlardaki işlemleri yeniden hesapla | Hesap hatası: cevabı kullanma |
| 3 | Sonuç kodla hesaplanabiliyorsa karşılaştır | Akıl yürütme hatası: kodun sonucunu kullan |
| 4 | Müşteriye yalnızca son cevabı göster | — |

**Ne zaman kullanılmaz?**

- Tek adımlı işlerde (kategori seçmek, kısa bir bilgi çıkarmak).
- Sonuç kodla kesin hesaplanabiliyorsa: o zaman modelden yalnızca
  sayıları iste, hesabı kod yapsın.
- Token bütçesi dar ve hatanın bedeli küçükse.

**Sık hatalar:**

- **Son cevabı metnin herhangi bir yerinden almak.** Adımlardaki ara
  sonuçlardan biri cevap sanılabilir.
- **Adımlar doğru görünüyor diye cevaba güvenmek.** Derste doğru
  hesaplanmış ama eksik bir adım yanlış tutar verdi.
- **Çoğunluğu doğruluk sanmak.** Aynı hatayı tekrarlayan bir modelde
  çoğunluk da yanlış olur.
- **Adımları müşteriye göstermek.** Yanlış ara sonuçlar ve iç kurallar
  görünür.
