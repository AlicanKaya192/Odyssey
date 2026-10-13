Dikkat ağırlıklarına bakıp "model şu kelimeye baktı, kararı ondan verdi"
demek çekici. Ama derste "the boy smiled and" cümlesinde ağırlık dağınıktı ve
karar yine doğruydu. Dersteki `attend` ile kelimeleri çıkararak deneyelim:

```python
for prefix in [["the", "queen", "smiled", "and"], ["the", "smiled", "and"],
               ["the", "boy", "smiled", "and"], ["smiled", "and"]]:
    _, a, _, p = attend(prefix)
    print(" ".join(prefix), round(float(p), 3))
```

```text
the queen smiled and 1.0
the smiled and 0.0
the boy smiled and 0.0
smiled and 0.0
```

- "queen"i çıkarınca karar "kadın"dan "erkek"e dönüyor: "queen" gerçekten
  kararı veriyor.
- Hiç kişi kelimesi olmayan cümlede de karar "erkek". Model şunu öğrenmiş:
  "kadın kelimesi varsa she, yoksa he". "the boy smiled and" cümlesinde
  "boy" kararı değiştirmiyor; dağınık ağırlıklar da kararı açıklamıyor.
- Ders: dikkat ağırlıkları modelin nereye baktığını gösterir, kararı **neden**
  verdiğini her zaman göstermez. Jain ve Wallace (2019) gerçek modellerde
  farklı dikkat dağılımlarının aynı kararı verebildiğini gösterdi. Bir
  açıklamayı sınamanın sağlam yolu buradaki gibi müdahaledir: girdiyi
  değiştir, karar değişiyor mu bak.
