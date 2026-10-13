Sayımlar hazır: `counts[sınıf][kelime]` kelimenin o sınıftaki kaç yorumda
geçtiği, `sizes[sınıf]` o sınıfın yorum sayısı, `common` iki sınıfın toplamı.

- `log_odds(word)`: `log(((pos + 1) / (n_pos + 2)) / ((neg + 1) / (n_neg + 2)))`.
- `top_words(label, k)`: toplamda **en az 5** yorumda geçen kelimeleri log
  orana göre sıralasın; `"negative"` için en küçük, `"positive"` için en
  büyük `k` kelimeyi döndürsün (en uçtaki başta).

**Beklenen çıktı:**

```
['hate', 'honest', 'worse', 'stopped']
['love', 'expected', 'totally', 'packed']
```
