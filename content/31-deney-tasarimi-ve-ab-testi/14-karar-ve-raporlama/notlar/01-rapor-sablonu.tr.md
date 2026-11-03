## Sonucu tek satırda yazmak

```python
def report(rate_a, rate_b, low, high, decision):
    diff = (rate_b - rate_a) * 100
    return (f"A {rate_a:.2%} -> B {rate_b:.2%}: {diff:+.2f} pts "
            f"(95% CI {low * 100:.2f} to {high * 100:.2f}); {decision}")


print(report(0.1199, 0.1376, 0.0101, 0.0253, "ship"))
```

```text
A 11.99% -> B 13.76%: +1.77 pts (95% CI 1.01 to 2.53); ship
```

İki oran, mutlak fark, aralık ve karar tek satırda. Göreli fark ("%15
artış") yazılacaksa mutlak farkın **yanına** yazılır, yerine değil.

## Bir sayfalık rapor

| Bölüm | İçerik |
|---|---|
| Soru | ne değişti, hangi birincil metrik, hangi pratik eşik |
| Plan | örneklem büyüklüğü, süre, karar kuralı (testten önceki hâli) |
| Güven | SRM p'si, A/A sonucu, denge |
| Sonuç | iki oran, fark, %95 aralık, p |
| Koruma | iade, hata, hız: bozulma var mı |
| Karar | uygula / zararlı / belirsiz / değmez ve gerekçesi |
| Sınırlar | süre, yenilik etkisi, segmentler, karışma |

## Dört kararın cümleleri

- **Uygula:** "B satın almayı en az eşik kadar artırıyor."
- **Zararlı:** "B satın almayı düşürüyor; uygulanmıyor."
- **Belirsiz:** "Bu testle etkiyi ölçemedik; aralık −x ile +y."
- **Değmez:** "Etki büyük olasılıkla gerçek ama eşiğin altında."
