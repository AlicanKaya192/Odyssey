`final_answer(text)` metinde tek başına duran `Answer: <sayı>` satırını
bulsun ve sayıyı `float` olarak döndürsün; satır yoksa ya da satırda
sayıdan başka bir şey varsa `None`. Satırın başında ve sonunda boşluk
olabilir: `re.search(r"^Answer:\s*(\d+(?:\.\d+)?)\s*$", text,
flags=re.M)`.

**Beklenen çıktı:**

```
5.0
12.5
None
```
