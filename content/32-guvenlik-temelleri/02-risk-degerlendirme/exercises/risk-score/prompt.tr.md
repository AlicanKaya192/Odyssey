`risk_score(likelihood, impact)` iki puanın çarpımını döndürmeli. Ama
puanlardan biri 1 ile 5 arasında (ikisi de dahil) değilse hesap anlamsızdır:
o zaman `None` döndür.

**Beklenen çıktı:**

```
12
25
None
None
```
